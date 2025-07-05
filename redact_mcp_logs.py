import json

input_file = "sample_mcp_logs.jsonl"
output_file = "sample_mcp_logs_redacted.jsonl"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            log_entry = json.loads(line)
            log_entry["input"] = "[REDACTED]"
            log_entry["output"] = "[REDACTED]"
            log_entry["tags"] = "[REDACTED]"
            outfile.write(json.dumps(log_entry) + "\n")
        except:
            continue
