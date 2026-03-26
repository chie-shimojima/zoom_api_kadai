print("✅ プログラム開始しました！")
import json
import os
import requests
from dotenv import load_dotenv
from zoom_auth import get_access_token


def create_meeting(topic: str = "APIで作成したZoom会議"):
    """
    Zoomにミーティングを作成して、結果(JSON)を返す
    """
    token = get_access_token()

    url = "https://api.zoom.us/v2/users/me/meetings"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "topic": topic,
        "type": 1,  # 1 = 今すぐミーティング
        "password": os.environ.get("ZOOM_MEETING_PASSWORD", "839201"),
        "settings": {
            "waiting_room": False,
            "join_before_host": True,
        },
    }

    res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)

    if res.status_code not in (200, 201):
        print("❌ ミーティング作成に失敗しました")
        print("status:", res.status_code)
        print("response:", res.text)
        res.raise_for_status()

    return res.json()


if __name__ == "__main__":
    print("✅ プログラム開始しました！")

    # .env を読み込む
    load_dotenv()

    meeting = create_meeting()

    print("✅ Zoom Meeting Created!")
    print("Meeting ID :", meeting.get("id"))
    print("Passcode   :", meeting.get("password"))
    print("Join URL   :", meeting.get("join_url"))

    # 提出用にJSON保存
    with open("meeting_info.json", "w", encoding="utf-8") as f:
        json.dump(meeting, f, ensure_ascii=False, indent=2)

    print("📄 meeting_info.json に保存しました")
