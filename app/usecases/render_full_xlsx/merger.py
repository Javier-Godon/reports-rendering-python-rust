import io

import pandas as pd


def merge_reports(report_1_bytes: bytes, report_2_bytes: bytes, report_3_bytes: bytes) -> bytes:
    # Read reports into DataFrames
    with io.BytesIO(report_1_bytes) as report_1_io:
        df1 = pd.read_excel(report_1_io)

    with io.BytesIO(report_2_bytes) as report_2_io:
        df2 = pd.read_excel(report_2_io)

    with io.BytesIO(report_3_bytes) as report_3_io:
        df3 = pd.read_excel(report_3_io)

    # Prepare output buffer
    output_io = io.BytesIO()

    # FIX: Seek to beginning before passing it to ExcelWriter
    with pd.ExcelWriter(output_io, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name="Report_1", index=False)
        df2.to_excel(writer, sheet_name="Report_2", index=False)
        df3.to_excel(writer, sheet_name="Report_3", index=False)

    # Move cursor to start before returning bytes
    output_io.seek(0)
    return output_io.getvalue()