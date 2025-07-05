import requests
import time

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
CATEGORIES = ["Work", "Personal", "Promotions", "Finance", "Updates", "Spam", "Others"]

def rule_based_classification(subject, snippet):
    text = (subject + " " + snippet).lower()

    if "invoice" in text or "payment" in text or "bill" in text:
        return "Finance", 0.9
    elif "meeting" in text or "interview" in text or "project" in text:
        return "Work", 0.9
    elif "discount" in text or "offer" in text or "deal" in text:
        return "Promotions", 0.9
    elif "spam" in text or "lottery" in text:
        return "Spam", 0.9
    elif "update" in text or "policy" in text:
        return "Updates", 0.9
    elif "friend" in text or "family" in text:
        return "Personal", 0.9
    else:
        return "Others", 0.6

def classify_email(subject, snippet):
    prompt = f"Categorize this email into one category: {', '.join(CATEGORIES)}.\n\nSubject: {subject}\nSnippet: {snippet}\nRespond with just the category."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    category, confidence = "Others", 0.5

    for attempt in range(3):  
        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()

            category = resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
            confidence = 0.9 if category in CATEGORIES else 0.6

            if confidence >= 0.7:
                break  

        except Exception as e:
            print(f"Gemini API failed (Attempt {attempt+1}): {e}")
            time.sleep(1)

    if confidence < 0.7:
        print("⚠️ Falling back to rule-based classification.")
        category, confidence = rule_based_classification(subject, snippet)

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))  
        log_path = os.path.join(current_dir, "..", "prompt_log.md")
        log_path = os.path.normpath(log_path)  

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n### Prompt Used:\n{prompt}\n")
    except Exception as e:
        print(f"Warning: Could not save prompt log — {e}")

    return category, confidence, prompt
