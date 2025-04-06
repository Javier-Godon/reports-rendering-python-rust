import io
import xlsxwriter  # Import at the module level
from xlsxwriter import Workbook

class CpuSystemUsage:
    def __init__(self, date_from: int, date_to: int, data):
        self.date_from = date_from
        self.date_to = date_to
        self.data = data

    def render(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("CPU Usage")

        # --- Formatting ---
        bold = workbook.add_format({"bold": True})
        number_format = workbook.add_format({'num_format': '0.00'})

        # --- Set Column Widths ---
        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:D", 18)

        # --- Headers ---
        headers = ["CPU", "Average Usage (%)", "Max Usage (%)", "Min Usage (%)"]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, bold)

        # --- Write Data ---
        for row_num, usage in enumerate(self.data):
            row = row_num + 1
            worksheet.write(row, 0, usage['cpu'])
            worksheet.write(row, 1, usage['avg_usage'], number_format)
            worksheet.write(row, 2, usage['max_usage'], number_format)
            worksheet.write(row, 3, usage['min_usage'], number_format)

        # --- Optional Bar Chart ---
        if self.data:
            chart = workbook.add_chart({'type': 'column'})
            chart.add_series({
                'name':       '=CPU Usage!$B$1',
                'categories': '=CPU Usage!$A$2:$A$' + str(len(self.data) + 1),
                'values':     '=CPU Usage!$B$2:$B$' + str(len(self.data) + 1),
            })
            chart.set_title({'name': 'CPU Average Usage'})
            chart.set_x_axis({'name': 'CPU'})
            chart.set_y_axis({'name': 'Average Usage (%)'})
            insert_row = len(self.data) + 3
            worksheet.insert_chart(f'E{insert_row}', chart)

        workbook.close()
        output.seek(0)
        return output.getvalue()

if __name__ == "__main__":
    # Example usage for testing
    test_data = [
        {'cpu': 'cpu0', 'avg_usage': 11.71, 'max_usage': 45.34, 'min_usage': 2.83},
        {'cpu': 'cpu1', 'avg_usage': 12.31, 'max_usage': 37.98, 'min_usage': 1.00},
    ]
    report = CpuSystemUsage(1708023223, 1739645623, test_data)
    excel_bytes = report.render()
    with open("cpu_usage_report_formatted.xlsx", "wb") as f:
        f.write(excel_bytes)
    print("Test report generated: cpu_usage_report_formatted.xlsx")