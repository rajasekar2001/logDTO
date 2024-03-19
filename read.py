import json
from datetime import datetime

with open("log.json") as file:
    data = json.load(file)

resource_logs = data["resourceLogs"]
if resource_logs:
    first_resource_log = resource_logs[0]
    created_time_nano = first_resource_log["scopeLogs"][0]["logRecords"][0]["timeUnixNano"]
    created_time_sec = int(created_time_nano) // 10**9
    created_time_utc = datetime.utcfromtimestamp(created_time_sec).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    scope_logs = first_resource_log["scopeLogs"]
    if scope_logs:
        log_records = scope_logs[0]["logRecords"]
        if log_records:
            log_record = log_records[0]
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
                        "scope": scope_logs[0]["scope"]
                    }
                ],
                "serviceName": first_resource_log["resource"]["attributes"][8]["value"]["stringValue"],
                "severityText": log_record["severityText"],
                "spanId": log_record["spanId"],
                "traceId": log_record["traceId"]
            }
            
            
# Printing the extracted data
            print(json.dumps(extracted_data, indent=2))
        else:
            print("No log records found.")
    else:
        print("No scope logs found.")
else:
    print("No resource logs found.")
