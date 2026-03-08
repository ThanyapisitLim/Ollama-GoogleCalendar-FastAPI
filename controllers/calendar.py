from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_service():
    """สร้าง Service Object ครั้งเดียว"""
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("calendar", "v3", credentials=creds)

def format_iso(date_str):
    """ตัวช่วยแปลงวันที่ให้เป็นรูปแบบที่ Google API ยอมรับ (ISO 8601)"""
    try:
        # พยายามแปลงถ้ามีช่องว่างให้ใส่ T ถ้าไม่มีก็ส่งคืนตรงๆ
        if " " in date_str:
            date_str = date_str.replace(" ", "T")
        # ตรวจสอบว่ามี Timezone หรือ Z ต่อท้ายไหม ถ้าไม่มีเติมให้
        if not (date_str.endswith("Z") or "+" in date_str):
            date_str += "+07:00"
        return date_str
    except:
        return date_str

def get_events():
    service = get_service()
    events_result = service.events().list(calendarId="primary", maxResults=10).execute()
    return events_result.get("items", [])

def create_event(summary, start, end):
    service = get_service()
    event = {
        "summary": summary,
        "start": {"dateTime": format_iso(start), "timeZone": "Asia/Bangkok"},
        "end": {"dateTime": format_iso(end), "timeZone": "Asia/Bangkok"},
    }
    return service.events().insert(calendarId="primary", body=event).execute()

def delete_event(event_id):
    service = get_service()
    service.events().delete(calendarId="primary", eventId=event_id).execute()
    return {"message": f"Event {event_id} deleted successfully"}

def update_event(event_id, summary=None, start=None, end=None):
    service = get_service()
    existing_event = service.events().get(calendarId="primary", eventId=event_id).execute()

    if summary: existing_event["summary"] = summary
    if start: existing_event["start"] = {"dateTime": format_iso(start), "timeZone": "Asia/Bangkok"}
    if end: existing_event["end"] = {"dateTime": format_iso(end), "timeZone": "Asia/Bangkok"}

    return service.events().update(calendarId="primary", eventId=event_id, body=existing_event).execute()

def get_free_time(time_min, time_max):
    service = get_service()
    
    # ใช้วันที่ที่ผ่านการจัด format แล้ว
    body = {
        "timeMin": format_iso(time_min),
        "timeMax": format_iso(time_max),
        "items": [{"id": "primary"}]
    }

    # ตรวจสอบ error ถ้า API คืนค่ามาผิดพลาด
    freebusy_result = service.freebusy().query(body=body).execute()
    busy_periods = freebusy_result["calendars"]["primary"].get("busy", [])

    # คำนวณ free slots เหมือนเดิม
    free_slots = []
    current_start = time_min

    for busy in busy_periods:
        if current_start < busy["start"]:
            free_slots.append({"start": current_start, "end": busy["start"]})
        current_start = max(current_start, busy["end"])

    if current_start < time_max:
        free_slots.append({"start": current_start, "end": time_max})

    return free_slots