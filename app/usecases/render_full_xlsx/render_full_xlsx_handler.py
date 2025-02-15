import app.usecases.render_full_xlsx.single_reports.report_1 as report_1
import app.usecases.render_full_xlsx.single_reports.report_2 as report_2
import app.usecases.render_full_xlsx.single_reports.report_3 as report_3

async def render_full_xlsx(date_from: int, date_to: int):
    import xlsxwriter

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook("demo.xlsx", {'in_memory': True})
    await report_1.render(workbook=workbook,date_from=date_from,date_to=date_to)
    await report_2.render(workbook=workbook, date_from=date_from, date_to=date_to)
    await report_3.render(workbook=workbook, date_from=date_from, date_to=date_to)

    workbook.close()