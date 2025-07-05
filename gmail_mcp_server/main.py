from fastapi import FastAPI
from fastapi.responses import JSONResponse

import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

from mcp_logger import log_mcp 
import json

from fastapi import FastAPI, Request as FastAPIRequest
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from google.auth.transport.requests import Request as GoogleRequest

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/view", response_class=HTMLResponse)
def view_ui(request: FastAPIRequest):
    return templates.TemplateResponse("ui.html", {"request": request})

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    token_path = './token.json'  
    credentials_path = './credentials.json'
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES) 
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        
    service = build('gmail', 'v1', credentials=creds)
    return service

@app.get("/fetch-emails")
def fetch_emails(days: int = 7, max_results: int = 50):
    service = get_gmail_service()
    
    after_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y/%m/%d")
    
    results = service.users().messages().list(
        userId = 'me',
        q = f'after:{after_date}',
        maxResults = max_results
    ).execute()
    
    messages = results.get('messages', [])
    emails = []
    
    for msg in messages:
        msg_detail = service.users().messages().get(userId = 'me', id = msg['id']).execute()
        
        headers = msg_detail.get('payload', {}).get('headers', [])
        snippet = msg_detail.get('snippet', '')
        
        email_data = {
            "message_id": msg['id'],
            "date": "",
            "from": "",
            "subject": "",
            "snippet": snippet
        }
        
        for header in headers:
            if header['name'].lower() == 'date':
                email_data["date"] = header['value']
            if header['name'].lower() == 'from':
                email_data["from"] = header['value']
            if header['name'].lower() == 'subject':
                email_data["subject"] = header['value']
        
        emails.append(email_data)

    log_mcp(
        agent="GmailMCPServer-v1",
        operation="fetch_last_{}_days".format(days),
        model_used="Gmail API v1",
        input_data={"user": "me", "date_range": f"{after_date} to {datetime.utcnow().strftime('%Y/%m/%d')}"},
        output_data={"email_count": len(emails)},
        tags=["fetch", "gmail", "mcp"]
    )

    return JSONResponse(content=emails)

@app.get("/logs")
def get_logs():
    log_file = '../sample_mcp_logs.jsonl' 

    if not os.path.exists(log_file):
        return JSONResponse(content={"message": "Log file not found"}, status_code=404)

    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            try:
                logs.append(json.loads(line.strip()))
            except:
                continue  

    return JSONResponse(content=logs)

@app.get("/categorized-emails")
def get_categorized_emails():
    try:
        with open("../sample_mcp_logs.jsonl", "r") as f:
            emails = []
            for line in f:
                entry = json.loads(line)
                
                if entry.get("operation") == "classify_email":
                    subject = entry.get("input", {}).get("subject", "N/A")
                    category = entry.get("output", {}).get("category", "Others")

                    emails.append({"subject": subject, "category": category})

        return JSONResponse(content=emails)
    except Exception as e:
        print(f"Error reading logs: {e}")
        return JSONResponse(content=[], status_code=500)


@app.get("/")
def root():
    return {"message": "Welcome to the Gmail MCP server!"}
