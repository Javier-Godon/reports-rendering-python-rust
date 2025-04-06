use base64::Engine as _;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;
use std::io::{Read, Write};
use std::process::{Command, Stdio};
use std::sync::mpsc;
use std::thread;
use tempfile::NamedTempFile; //  Add `tempfile = "3"` to Cargo.toml

#[pymodule]
fn pyo3_rust(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(render_parallel_xlsx, m)?)?;
    Ok(())
}

fn render_report(
    module_path: &str,
    class_name: &str,
    date_from: i64,
    date_to: i64,
    data_json: &str, // This is still the JSON string for the *specific* report
) -> Vec<u8> {
    // Save data to temp file
    let mut temp_file = NamedTempFile::new().expect("Failed to create temp file");
    temp_file
        .write_all(data_json.as_bytes())
        .expect("Failed to write temp data");

    let temp_path = temp_file.path().to_str().unwrap();

    let output = Command::new("python3")
        .arg("-c")
        .arg(format!(
            r#"
import importlib, sys, json

sys.path.insert(0, '.')

module = importlib.import_module('{0}')
cls = getattr(module, '{1}')

with open('{4}', 'r') as f:
    data = json.load(f)

instance = cls({2}, {3}, data)
result = instance.render()

sys.stdout.buffer.write(result)
"#,
            module_path, class_name, date_from, date_to, temp_path
        ))
        .output()
        .expect("Failed to execute Python script");

    if !output.status.success() {
        eprintln!("❌ Python script execution failed for '{}'!", module_path);
        eprintln!("Stdout: {}", String::from_utf8_lossy(&output.stdout));
        eprintln!("Stderr: {}", String::from_utf8_lossy(&output.stderr));
        panic!("Python execution failed");
    }

    println!(
        "✅ Report generated '{}', size: {} bytes",
        module_path,
        output.stdout.len()
    );

    output.stdout
}

fn merge_reports(reports: Vec<Vec<u8>>) -> Vec<u8> {
    println!("🔄 Merging {} reports...", reports.len());

    let mut child = Command::new("python3")
        .arg("-c")
        .arg(
            r#"
import sys
import base64
from io import BytesIO
from openpyxl import Workbook, load_workbook
from copy import copy

def merge_reports(report_files):
    if not report_files:
        return b''
    final_workbook = Workbook()
    del final_workbook['Sheet']

    for idx, report_data in enumerate(report_files):
        try:
            # Load the xlsxwriter-generated data with openpyxl
            wb = load_workbook(BytesIO(report_data))
            for sheet_name in wb.sheetnames:
                source_sheet = wb[sheet_name]
                target_sheet = final_workbook.create_sheet(f"Report_{idx+1}_{sheet_name}")

                # Copy cell values and styles
                for row in source_sheet.iter_rows():
                    for cell in row:
                        new_cell = target_sheet.cell(row=cell.row, column=cell.column, value=cell.value)
                        if cell.has_style:
                            new_cell.font = copy(cell.font)
                            new_cell.border = copy(cell.border)
                            new_cell.fill = copy(cell.fill)
                            new_cell.number_format = copy(cell.number_format)
                            new_cell.protection = copy(cell.protection)
                            new_cell.alignment = copy(cell.alignment)

                # --- Handling Drawings/Charts (More Complex) ---
                if hasattr(source_sheet, '_charts'): # Check if xlsxwriter stores charts this way (unlikely)
                    for chart in source_sheet._charts:
                        try:
                            target_sheet.add_chart(copy(chart), chart.anchor) # Might not work directly
                        except Exception as e:
                            sys.stderr.write(f"Warning: Could not copy chart (method 1) from Report {idx+1}, Sheet '{sheet_name}': {e}\n")
                elif hasattr(source_sheet, '_drawing_objects'): # Check for openpyxl-style drawings
                    for drawing in source_sheet._drawing_objects:
                        try:
                            target_sheet._drawing_objects.append(copy(drawing)) # Might not work directly
                        except Exception as e:
                            sys.stderr.write(f"Warning: Could not copy drawing (chart?) (method 2) from Report {idx+1}, Sheet '{sheet_name}': {e}\n")
                else:
                    sys.stderr.write(f"Warning: No drawing objects found in Report {idx+1}, Sheet '{sheet_name}'\n")

        except Exception as e:
            sys.stderr.write(f"Error reading report {idx + 1}: {e}\n")
            continue

    output_io = BytesIO()
    final_workbook.save(output_io)
    return output_io.getvalue()

data = sys.stdin.buffer.read()
reports = [base64.b64decode(chunk) for chunk in data.split(b'|') if chunk]

if not reports:
    sys.stderr.write("⚠️ No reports received for merging!\n")
    sys.stdout.buffer.write(b'')
else:
    sys.stdout.buffer.write(merge_reports(reports))
"#,
        )
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped()) // Capture Python errors
        .spawn()
        .expect("Failed to start merge process");

    let mut child_stdin = child.stdin.take().unwrap();
    for (i, report) in reports.iter().enumerate() {
        if i > 0 {
            child_stdin.write_all(b"|").unwrap();
        }
        child_stdin
            .write_all(
                &base64::engine::general_purpose::STANDARD
                    .encode(report)
                    .into_bytes(),
            )
            .unwrap();
    }
    drop(child_stdin); // Close stdin so Python can proceed

    let mut merged_bytes = Vec::new();
    let mut output = child.stdout.take().unwrap();
    let mut stderr = child.stderr.take().unwrap();

    let mut error_output = String::new();
    stderr
        .read_to_string(&mut error_output)
        .expect("Failed to read error output");

    output
        .read_to_end(&mut merged_bytes)
        .expect("Failed to read merged output");

    if !error_output.is_empty() {
        println!("⚠️ Python merge script error: {}", error_output);
    }

    println!("✅ Merged report size: {} bytes", merged_bytes.len());

    merged_bytes
}

#[pyfunction]
fn render_parallel_xlsx(
    module_paths: Vec<String>,
    date_from: i64,
    date_to: i64,
    data: String, // Expecting a JSON string of a list of JSON strings
) -> PyResult<Vec<u8>> {
    let (sender, receiver) = mpsc::channel();

    let data_list: Vec<String> = serde_json::from_str(&data).expect("Failed to parse data list JSON");

    if module_paths.len() != data_list.len() {
        return Err(pyo3::exceptions::PyValueError::new_err(
            "Number of module paths must match the number of data JSON strings",
        ));
    }

    let handles: Vec<_> = module_paths
        .into_iter()
        .zip(data_list.into_iter())
        .map(|(module_path, data_json)| {
            let sender = sender.clone();
            let class_name = extract_class_name(&module_path);
            let module_path = module_path.clone(); // Clone to move into the thread
            let data_json = data_json.clone();     // Clone to move into the thread

            thread::spawn(move || {
                let result =
                    render_report(&module_path, &class_name, date_from, date_to, &data_json);
                sender
                    .send(result)
                    .expect("❌ Failed to send result from thread");
            })
        })
        .collect();

    // Ensure all threads have finished
    for handle in handles {
        handle.join().expect("❌ Thread panicked!");
    }

    drop(sender);
    let results: Vec<Vec<u8>> = receiver.iter().collect();

    for (i, result) in results.iter().enumerate() {
    let filename = format!("debug_report_{}.xlsx", i);
    std::fs::write(&filename, result).expect("Failed to write debug report");
    println!("✅ Debug report saved: {}", filename);
    }

    let final_report = merge_reports(results);

    Ok(final_report)
}

fn extract_class_name(module_path: &str) -> String {
    let parts: Vec<&str> = module_path.split('.').collect();
    let module_name = parts.last().expect("Invalid module path");

    // Convert snake_case to CamelCase
    module_name
        .split('_')
        .map(|word| {
            let mut chars = word.chars();
            match chars.next() {
                Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
                None => String::new(),
            }
        })
        .collect()
}
