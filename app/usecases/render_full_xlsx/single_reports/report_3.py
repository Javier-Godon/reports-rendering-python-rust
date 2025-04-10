import io
import time

from xlsxwriter import Workbook

def render(date_from: int, date_to: int):
    output = io.BytesIO()
    workbook = Workbook(output, {"in_memory": True})
    worksheet = workbook.add_worksheet("Report_3")

    worksheet.set_column("A:A", 20)
    bold = workbook.add_format({"bold": True})

    worksheet.write("A1", "Report 3 Details")
    worksheet.write("A2", f"From {date_from} to {date_to}", bold)
    worksheet.write(3, 0, 111)
    worksheet.write(4, 0, 222.333)

    workbook.close()
    output.seek(0)
    return output.getvalue()
