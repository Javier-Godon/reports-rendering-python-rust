import io

import pandas as pd

import app.usecases.render_full_xlsx.single_reports.report_1 as report_1
import app.usecases.render_full_xlsx.single_reports.report_2 as report_2
import app.usecases.render_full_xlsx.single_reports.report_3 as report_3
import pyo3_rust

from app.usecases.render_full_xlsx.merger import merge_reports

def render_full_xlsx():
    final_excel = pyo3_rust.render_parallel_xlsx()

    if not isinstance(final_excel, bytes):
        raise TypeError("Expected bytes from Rust function, got {}".format(type(final_excel)))

    with open("final_report.xlsx", "wb") as f:
        f.write(final_excel)

    print("✅ Merged Excel report saved as 'final_report.xlsx'")



