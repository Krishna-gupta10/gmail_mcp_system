import requests
from classify import classify_email
from mcp_logger import log_mcp
import time  

MCP_SERVER_URL = "http://127.0.0.1:8000/fetch-emails"

def fetch_emails(days=7, max_results=50):
    try:
        response = requests.get(MCP_SERVER_URL, params={"days": days, "max_results": max_results})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch emails: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def classify_all_emails():
    emails = fetch_emails()

    for email in emails:
        subject = email.get("subject", "")
        snippet = email.get("snippet", "")

        category, confidence, prompt = classify_email(subject, snippet)

        # MCP Log
        log_mcp(
            agent="EmailClassifierAgent",
            operation="classify_email",
            model_used="Gemini 2.5 Flash",
            input_data={"subject": subject, "snippet": snippet},
            output_data={"category": category, "confidence": confidence},
            tags=["classification", "mcp"]
        )

        print(f"Email: {subject} --> {category} ({confidence*100:.0f}%)")

        time.sleep(1.5)

if __name__ == "__main__":
    classify_all_emails()
