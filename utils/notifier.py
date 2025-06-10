import requests
import datetime
import logging
logger = logging.getLogger(__name__)

class Notifier:
    def __init__(self, webhook_url, default_color = "#cf4867"):
        self.webhook_url = webhook_url
        self.color = int(default_color.lstrip("#"), 16)


    def send_log(self, title, description = None, footer = None, fields = None, color = None):
        embed_color = int(color.lstrip("#"), 16) if isinstance(color, str) else (color or self.color)
        embed = {
            "title": title,
            "color": embed_color,
            # "timestamp": datetime.datetime.utcnow().isoformat()
        }

        if description:
            embed["description"] = description
        if footer:
            embed["footer"] = {"text": footer}
        if fields:
            embed["fields"] = [
                {"name": f["name"], "value": f["value"], "inline": f.get("inline", False)} for f in fields
            ]

        payload = {"embeds": [embed]}
        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 204:
                logger.info("✅ Log đã được gửi thành công đến Discord.")
                return True
            else:
                logger.error(f"❌ Lỗi gửi log: {response.status_code}, {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"🔌 Lỗi kết nối khi gửi log: {e}")
            return False
