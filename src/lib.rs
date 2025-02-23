use base64::Engine as _;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;
use std::io::{Read, Write};
use std::process::{Command, Stdio};
use std::sync::mpsc;
use std::thread;

#[pymodule]
fn pyo3_rust(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(render_parallel_xlsx, m)?)?;
    Ok(())
}

fn render_report(report_script: &str, date_from: i64, date_to: i64) -> Vec<u8> {
    let output = Command::new("python3")
        .arg("-c")
        .arg(format!(
            r#"
import importlib
import sys
sys.path.insert(0, '.')
module = importlib.import_module('{0}')
try:
    data = module.render('{1}', '{2}')
    sys.stdout.buffer.write(data)  # Write binary data directly to stdout
except Exception as e:
    print(f"❌ Python error in {0}: {{e}}", file=sys.stderr)
    sys.exit(1)
"#,
            report_script, date_from, date_to
        ))
        .output()
        .expect("Failed to execute Python script");

    if !output.status.success() {
        eprintln!("❌ Python script execution failed!");
        eprintln!("Stdout: {}", String::from_utf8_lossy(&output.stdout));
        eprintln!("Stderr: {}", String::from_utf8_lossy(&output.stderr));
        panic!("Python execution failed");
    }

    println!(
        "✅ Generated report '{}', size: {} bytes",
        report_script,
        output.stdout.len()
    );

    output.stdout // Return bytes directly (no file writing)
}

fn merge_reports(reports: Vec<Vec<u8>>) -> Vec<u8> {
    println!("🔄 Merging {} reports...", reports.len());

    let mut child = Command::new("python3")
        .arg("-c")
        .arg(
            r#"
import pandas as pd
from io import BytesIO
import sys
import base64

def merge_reports(report_files):
    if not report_files:
        return b''  # No reports, return empty bytes
    output_io = BytesIO()
    with pd.ExcelWriter(output_io, engine='openpyxl') as writer:
        for idx, report_data in enumerate(report_files):
            with pd.ExcelFile(BytesIO(report_data)) as xls:
                for sheet_name in xls.sheet_names:
                    df = xls.parse(sheet_name)
                    df.to_excel(writer, sheet_name=f"Sheet{idx+1}", index=False)
    return output_io.getvalue()

data = sys.stdin.buffer.read()
reports = [base64.b64decode(chunk) for chunk in data.split(b'|') if chunk]

if not reports:
    sys.stderr.write("⚠️ No reports received for merging!\n")
    sys.stdout.buffer.write(b'')  # Return empty bytes
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
        eprintln!("⚠️ Python merge script error: {}", error_output);
    }

    println!("✅ Merged report size: {} bytes", merged_bytes.len());

    merged_bytes
}

#[pyfunction]
fn render_parallel_xlsx(reports: Vec<String>, date_from: i64, date_to: i64) -> PyResult<Vec<u8>> {
    let (sender, receiver) = mpsc::channel();

    let handles: Vec<_> = reports
        .into_iter()
        .map(|report| {
            let sender = sender.clone();
            thread::spawn(move || {
                let data = render_report(&report, date_from, date_to);
                sender.send(data).unwrap();
            })
        })
        .collect();

    // Ensure all threads have finished
    for handle in handles {
        handle.join().expect("❌ Thread panicked!");
    }

    // Collect results from all threads
    drop(sender);
    let results: Vec<Vec<u8>> = receiver.iter().collect();

    // Merge reports into a single Excel file
    let final_report = merge_reports(results);

    Ok(final_report) // Return the merged bytes
}
