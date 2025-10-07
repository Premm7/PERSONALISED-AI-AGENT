# nlp.py
import spacy
from datetime import datetime, timedelta
import re

class NlpEngine:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def detect_intent(self, text: str):
        doc = self.nlp(text.lower())
        lemmas = [tok.lemma_ for tok in doc]

        # Basic rules - expand as needed
        if any(word in lemmas for word in ["time", "clock", "what's the time", "what time"]):
            return {"intent": "time"}

        if any(word in lemmas for word in ["calculate", "what", "plus", "minus", "times", "divide", "multiplied", "add", "subtract", "sum", "product", "evaluate"]):
            # try to extract pure math expression
            expr = self._extract_expression(text)
            return {"intent": "math", "entities": {"expression": expr}}

        if any(word in lemmas for word in ["search", "find", "look"]):
            # get query part
            query = self._extract_after_keyword(text, ["search", "find", "look for"])
            return {"intent": "search", "entities": {"query": query}}

        if any(word in lemmas for word in ["remind", "reminder", "remindme", "remember"]):
            # parse time if present
            dt = self._extract_datetime(text)
            note = self._extract_after_keyword(text, ["remind me to", "remind me", "remind"])
            return {"intent": "reminder", "entities": {"datetime": dt, "note": note}}

        if any(word in lemmas for word in ["open", "launch"]):
            return {"intent": "open_browser"}

        return {"intent": "unknown"}

    def _extract_expression(self, text):
        # crude: take digits and operators
        allowed = re.findall(r"[\d\.\+\-\*\/\^\(\)\%]+", text)
        if allowed:
            return " ".join(allowed)
        # fallback to text
        return text

    def _extract_after_keyword(self, text, keywords):
        for kw in keywords:
            if kw in text:
                return text.split(kw, 1)[1].strip()
        return text

    def _extract_datetime(self, text):
        # Very basic datetime parsing: 'at 3 PM', 'at 15:30', 'tomorrow at 9'
        text = text.lower()
        # 'tomorrow'
        if "tomorrow" in text:
            base = datetime.now().date() + timedelta(days=1)
            # try time hh:mm or h PM
            m = re.search(r"(\d{1,2}:\d{2})", text)
            if m:
                t = m.group(1)
                return f"{base} {t}"
            m = re.search(r"(\d{1,2})\s?(am|pm)", text)
            if m:
                h = int(m.group(1))
                ampm = m.group(2)
                if ampm == "pm" and h != 12:
                    h += 12
                return f"{base} {h:02d}:00"
            return str(base)

        # today
        m = re.search(r"at\s+(\d{1,2}:\d{2})", text)
        if m:
            return f"{datetime.now().date()} {m.group(1)}"
        m = re.search(r"at\s+(\d{1,2})\s?(am|pm)?", text)
        if m:
            h = int(m.group(1))
            ampm = m.group(2)
            if ampm == "pm" and h != 12:
                h += 12
            return f"{datetime.now().date()} {h:02d}:00"
        return None
