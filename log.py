import json
from datetime import datetime

with open("log.json") as file:
    data = json.load(file)

resource_logs = data["resourceLogs"]
for log in resource_logs:
    created_time_nano = log["scopeLogs"][0]["logRecords"][0]["timeUnixNano"]
    created_time_sec = int(created_time_nano) // 10**9
    created_time_utc = datetime.utcfromtimestamp(created_time_sec).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    scope_logs = log["scopeLogs"]
    for scope_log in scope_logs:
        log_records = scope_log["logRecords"]
        for log_record in log_records:
            extracted_data = {
                "createdTime": {"$date": created_time_utc},
                "scopeLogs": [
                    {
                        "logRecords": [
                            {
                                "body": log_record["body"],
                                "flags": log_record["flags"],
                                "observedTimeUnixNano": log_record["observedTimeUnixNano"],
                                "severityNumber": log_record["severityNumber"],
                                "severityText": log_record["severityText"],
                                "spanId": log_record["spanId"],
                                "timeUnixNano": log_record["timeUnixNano"],
                                "traceId": log_record["traceId"]
                            }
                        ],
                        "scope": scope_log["scope"]
                    }
                ],
                "serviceName": log["resource"]["attributes"][8]["value"]["stringValue"],
                "severityText": log_record["severityText"],
                "spanId": log_record["spanId"],
                "traceId": log_record["traceId"]
            }
            print(json.dumps(extracted_data, indent=2))
