# assistant_core.py
import os
from datetime import datetime
from nlp import NlpEngine
from utils import safe_eval, format_time
from wolfram_client import WolframClient
from search_client import search_web
from reminder_db import add_reminder
from dotenv import load_dotenv

load_dotenv()

class Assistant:
    def __init__(self):
        self.nlp = NlpEngine()
        wolfram_appid = os.getenv("WOLFRAM_APPID")
        self.wolfram = WolframClient(wolfram_appid) if wolfram_appid else None

    def handle(self, text):
        """
        Main entry: accept text string, return dict { 'text': ..., 'type': ... }
        """
        text = text.strip()
        if not text:
            return {"text": "I didn't catch that. Please say or type something.", "type": "error"}
        intent_info = self.nlp.detect_intent(text)

        intent = intent_info.get("intent")
        entities = intent_info.get("entities", {})

        # Time intent
        if intent == "time":
            now = datetime.now()
            return {"text": f"The current time is {format_time(now)}.", "type": "time"}

        # Math intent
        if intent == "math":
            expr = entities.get("expression") or text
            # Try wolfram first then safe eval
            if self.wolfram:
                try:
                    r = self.wolfram.query(expr)
                    if r:
                        return {"text": r, "type": "math"}
                except Exception:
                    pass
            try:
                result = safe_eval(expr)
                return {"text": f"The result is {result}.", "type": "math"}
            except Exception as e:
                return {"text": f"Sorry, I couldn't compute that: {e}", "type": "error"}

        # Search intent
        if intent == "search":
            query = entities.get("query") or text
            try:
                snippet = search_web(query)
                return {"text": snippet or "No concise result found.", "type": "search"}
            except Exception as e:
                return {"text": f"Search failed: {e}", "type": "error"}

        # Reminder intent
        if intent == "reminder":
            when = entities.get("datetime")
            note = entities.get("note") or text
            if when:
                # add in DB
                add_reminder(note, when)
                return {"text": f"Okay — I will remind you at {when}.", "type": "reminder"}
            else:
                return {"text": "When should I remind you? Please say a time (e.g., 'at 3 PM' or 'today 15:00').", "type": "reminder"}

        # Open browser intent
        if intent == "open_browser":
            return {"text": "I can't open a browser from the server, but I can give you a link or instructions.", "type": "action"}

        # Fallback: small talk or unknown
        return {"text": "Sorry, I don't know how to do that yet. Try asking the time, a math question, or to set a reminder.", "type": "unknown"}
