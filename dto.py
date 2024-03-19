import json

class LogRecord:
    def __init__(self, body, flags, observed_time_unix_nano, severity_number, severity_text, span_id, time_unix_nano, trace_id):
        self.body = body
        self.flags = flags
        self.observed_time_unix_nano = observed_time_unix_nano
        self.severity_number = severity_number
        self.severity_text = severity_text
        self.span_id = span_id
        self.time_unix_nano = time_unix_nano
        self.trace_id = trace_id

class ScopeLog:
    def __init__(self, log_records, scope_name):
        self.log_records = log_records
        self.scope_name = scope_name

class LogDTO:
    def __init__(self, created_time, scope_logs, service_name, severity_text, span_id, trace_id):
        self.created_time = created_time
        self.scope_logs = scope_logs
        self.service_name = service_name
        self.severity_text = severity_text
        self.span_id = span_id
        self.trace_id = trace_id

def dto_to_json(log_dto):
    json_data = {
        "createdTime": {"$date": log_dto.created_time},
        "scopeLogs": [],
        "serviceName": log_dto.service_name,
        "severityText": log_dto.severity_text,
        "spanId": log_dto.span_id,
        "traceId": log_dto.trace_id
    }

    for scope_log in log_dto.scope_logs:
        log_records = []
        for log_record in scope_log.log_records:
            log_records.append({
                "body": {"stringValue": log_record.body},
                "flags": log_record.flags,
                "observedTimeUnixNano": log_record.observed_time_unix_nano,
                "severityNumber": log_record.severity_number,
                "severityText": log_record.severity_text,
                "spanId": log_record.span_id,
                "timeUnixNano": log_record.time_unix_nano,
                "traceId": log_record.trace_id
            })
        json_data["scopeLogs"].append({
            "logRecords": log_records,
            "scope": {"name": scope_log.scope_name}
        })

    return json.dumps(json_data, indent=2)

log_dto = LogDTO(
    "2024-03-14T14:26:19.134Z",
    [ScopeLog([LogRecord("HikariPool-1 - Start completed.", 0, "1710426379134130000", 9, "INFO", "", "1710426379133000000", "")], "com.zaxxer.hikari.HikariDataSource")],
    "vendor-srv-3",
    "INFO",
    "",
    ""
)

json_output = dto_to_json(log_dto)
print(json_output)
