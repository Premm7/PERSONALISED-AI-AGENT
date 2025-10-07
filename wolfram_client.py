# wolfram_client.py
import wolframalpha

class WolframClient:
    def __init__(self, appid):
        if not appid:
            raise ValueError("No WolframAlpha APPID provided.")
        self.client = wolframalpha.Client(appid)

    def query(self, text):
        res = self.client.query(text)
        # take first pod that has 'plaintext'
        pod_texts = []
        for pod in res.pods:
            for sub in pod.subpods:
                if getattr(sub, 'plaintext', None):
                    pod_texts.append(sub.plaintext)
        if pod_texts:
            return pod_texts[0]
        return None
