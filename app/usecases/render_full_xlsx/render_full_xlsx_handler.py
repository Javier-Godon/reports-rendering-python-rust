import pyo3_rust

import app.usecases.render_full_xlsx.single_reports.report_1 as report_1
import app.usecases.render_full_xlsx.single_reports.report_2 as report_2
import app.usecases.render_full_xlsx.single_reports.report_3 as report_3

# import app.grpc_client_impl.grpc_client as grpc_client
from app.grpc_client_impl.grpc_client import GRPCClientSingleton


def render_full_xlsx(date_from: int, date_to: int):
    grpc_client =GRPCClientSingleton.get_instance()
    system_usage = grpc_client.get_cpu_system_usage(date_from=date_from, date_to=date_to)
    user_usage = grpc_client.get_cpu_user_usage(date_from=date_from, date_to=date_to)

    reports = [report_1, report_2, report_3]
    report_paths = [r.__name__ for r in reports]

    final_excel = pyo3_rust.render_parallel_xlsx(reports=report_paths, date_from=date_from, date_to=date_to)

    if not isinstance(final_excel, bytes):
        raise TypeError("Expected bytes from Rust function, got {}".format(type(final_excel)))

    # We can check if the .xlsx file was properly created.
    with open("final_report.xlsx", "wb") as f:
        f.write(final_excel)

    return final_excel
