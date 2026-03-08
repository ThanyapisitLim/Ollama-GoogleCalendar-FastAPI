# Calendar AI Agent API

โปรเจกต์นี้เป็น API สำหรับจัดการ Google Calendar โดยทำงานร่วมกับ AI Agent เพื่อรับคำสั่งภาษาธรรมชาติจากผู้ใช้ และดำเนินการผ่าน Google Calendar API โดยอัตโนมัติ

## 🚀 ฟีเจอร์หลัก
* **Calendar Management**: สร้าง, อ่าน, อัปเดต และลบกิจกรรม (CRUD)
* **Smart Free Time**: ค้นหาช่วงเวลาว่างจากปฏิทินด้วย Query อัจฉริยะ
* **AI Integration**: ใช้ AI (Ollama/LLM) ในการวิเคราะห์และแปลคำสั่งภาษาอังกฤษ/ไทย ให้เป็นฟังก์ชันการทำงาน

## 🛠 เทคโนโลยีที่ใช้
* **Framework**: FastAPI
* **AI Engine**: Ollama (แนะนำรุ่น qwen2.5:7b หรือ llama3.2)
* **Google Services**: google-api-python-client
* **Python**: 3.13
