import json
from datetime import datetime

LOG_FILE = '../sample_mcp_logs.jsonl' 

def log_mcp(agent, operation, model_used, input_data, output_data, status="success", tags=None):
    log_entry = {
        "agent": agent,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "operation": operation,
        "model_used": model_used,
        "input": input_data,
        "output": output_data,
        "status": status,
        "tags": tags or []
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
