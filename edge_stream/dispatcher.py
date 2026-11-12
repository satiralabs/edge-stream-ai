"""
EdgeStream Dispatcher: Dispatches motion events to webhooks or stdout.
"""

import json
import time
import urllib.request
from typing import Any, Dict, Optional


class AlertDispatcher:
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url

    def dispatch(self, event_data: Dict[str, Any]) -> bool:
        event_data["timestamp"] = time.time()
        payload = json.dumps(event_data).encode("utf-8")

        if not self.webhook_url:
            return True

        try:
            req = urllib.request.Request(
                self.webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                return resp.status in [200, 201, 202, 204]
        except Exception:
            return False
