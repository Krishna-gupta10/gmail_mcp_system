# Gmail MCP Server & Email Categorization Agent  
**Fetch, classify, and log Gmail emails with AI-powered automation using FastAPI and Gemini 2.5 Flash**

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

Make sure you have Python 3.9 or higher installed. Then, install the required dependencies:

```bash
pip install fastapi uvicorn google-api-python-client google-auth google-auth-oauthlib requests
```

### Gmail API Configuration
Enable Gmail API  
Go to Google Cloud Console.  
Create a new project or select an existing one.  
Navigate to APIs & Services > Library, search for Gmail API, and enable it.  
Create OAuth 2.0 Credentials  
Navigate to APIs & Services > Credentials.  
Click + Create Credentials > OAuth client ID.  
Select Desktop App as the application type.  
Download the JSON file and save it as credentials.json inside the gmail_mcp_server/ folder.  

### Gemini API Configuration
Get a free API Key from Google AI Studio.  
Open email_agent/classify.py and replace the API_KEY placeholder with your actual Gemini API key.  

### Running the MCP Server
```bash
cd gmail_mcp_server  
uvicorn main:app --reload
```

### 3️⃣ Running the Email Categorization Agent
```bash
cd email_agent  
python call_gmail_api.py  
```

### 4️⃣ Accessing the MCP Server
Open your browser and navigate to http://localhost:8000/view. You should see the UI where you can log emails and view the logs.
