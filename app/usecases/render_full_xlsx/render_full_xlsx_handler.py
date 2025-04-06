import json
import pyo3_rust
import app.usecases.render_full_xlsx.single_reports.cpu_system_usage as cpu_system_usage
import app.usecases.render_full_xlsx.single_reports.cpu_user_usage as cpu_user_usage
from app.grpc_client_impl.grpc_client import GRPCClientSingleton

def render_full_xlsx(date_from: int, date_to: int):
    grpc_client = GRPCClientSingleton.get_instance()
    system_usage = grpc_client.get_cpu_system_usage(date_from=date_from, date_to=date_to)
    user_usage = grpc_client.get_cpu_user_usage(date_from=date_from, date_to=date_to)

    reports = [cpu_system_usage, cpu_user_usage]
    report_paths = [r.__name__ for r in reports]

    system_usage_json_str = map_get_cpu_system_usage_response_to_json(system_usage)
    user_usage_json_str = map_get_cpu_user_usage_response_to_json(user_usage) # Create JSON for user usage

    # Pass a list of JSON strings corresponding to the report paths
    data_list_json_str = [system_usage_json_str, user_usage_json_str]

    final_excel = pyo3_rust.render_parallel_xlsx(
        module_paths=report_paths,
        date_from=date_from,
        date_to=date_to,
        data=json.dumps(data_list_json_str) # Serialize the list of JSON strings
    )

    if not isinstance(final_excel, bytes):
        raise TypeError("Expected bytes from Rust function, got {}".format(type(final_excel)))

    with open("final_report.xlsx", "wb") as f:
        f.write(final_excel)

    return final_excel

def map_get_cpu_system_usage_response_to_json(system_usage):
    usage_data = []
    for usage in system_usage.usages:
        usage_data.append({
            "cpu": usage.cpu,
            "avg_usage": usage.avg_usage,
            "max_usage": usage.max_usage,
            "min_usage": usage.min_usage,
        })
    return json.dumps(usage_data)

def map_get_cpu_user_usage_response_to_json(user_usage):
    usage_data = []
    for usage in user_usage.usages:
        usage_data.append({
            "cpu": usage.cpu,
            "avg_usage": usage.avg_usage,
            "max_usage": usage.max_usage,
            "min_usage": usage.min_usage,
        })
    return json.dumps(usage_data)