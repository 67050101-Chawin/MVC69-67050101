# SUBMISSION - Exit Exam MVC 1/2569 (เสาร์บ่าย)

## 1. วิธีเปิดโปรแกรม
- ภาษา/เฟรมเวิร์ก: Python 3 / MVC
- Entry point / คำสั่งเปิดโปรแกรม: เปิด Terminal ที่โฟลเดอร์โปรเจกต์ แล้วรัน `python main.py` และ test_scenarios.py ด้วย ` test_scenarios.py`
- หมายเหตุที่จำเป็น (ถ้ามี): ระบบเป็นConsoleต้องมีไฟล์ `seed_data.json` 

## 2. ตารางเชื่อมโยง Requirements

| Requirement | Model / Domain | Controller / Action | View / Screen |
|---|---|---|---|
| R1 | `Member`, `RoleType`, `RequestStatus` | `RequestController.show_members()` | เมนู 1: ดูสมาชิกและคำขอ |
| R2 | `ChangeRequest`, `RequestService.create_request()` | `RequestController.create_request()` | เมนู 2: สร้างคำขอเปลี่ยนบทบาท |
| R3 | `Comment`, `Decision`, `RequestService.submit_comment()` / `add_vote()` | `RequestController.vote_on_request()` | เมนู 3: ลงความเห็นต่อคำขอ |
| R4 | `ChangeRequest.status`, `RequestService.cancel_request()` | `RequestController.cancel_request()` | เมนู 4: ยกเลิกคำขอ |
| R5 | `SummaryReport`, `RequestService.get_summary()` | `RequestController.show_summary()` | เมนู 6: ดูสรุปผล |
## 3. ผลการทดสอบ
| กรณี | ผ่าน/ไม่ผ่าน | หมายเหตุ (เฉพาะที่จำเป็น) |
|T1	|ผ่าน|สร้างคำขอสำเร็จ
|T2	|ผ่าน|ระบบไม่อนุญาตให้สร้างคำขอซ้ำ
|T3	|ผ่าน|C01 อนุมัติหลังได้รับ 2 APPROVE และ M02 เปลี่ยนเป็น EDITOR
|T4	|ผ่าน|C02 ไม่อนุมัติหลังได้รับ 2 REJECT
|T5	|ผ่าน|ยกเลิก C03 ได้สำเร็จ
|T6	|ผ่าน|ระบบไม่อนุญาตให้สมาชิกเป้าหมายลงความเห็นในคำขอของตนเอง
 ผ่านทั้งหมด 6/6 กรณี

## 4. ความแตกต่างระหว่างแบบที่ออกกับโปรแกรมจริง (ถ้ามี)
ระบุไม่เกิน 3 ข้อ
1. โปรแกรมจริงเป็น Console Application ตามเมนู 0-6 ไม่มี GUI
2. ชื่อเมธอดภายในบางส่วนใช้aliasเพื่อรองรับโค้ด/แบบทดสอบเดิม เช่น `add_vote = submit_comment`
3. ไฟล์ Requirements ต้นฉบับไม่ได้อยู่ในชุดไฟล์ที่ตรวจสอบ จึงไม่สามารถยืนยันความแตกต่างของ R1-R5 กับข้อสอบต้นฉบับได้โดยตรง

## 5. บันทึกการใช้ Generative AI

| เวลาโดยประมาณ | เครื่องมือ | ใช้เพื่ออะไร | นำคำแนะนำไปใช้อย่างไร |

| 13.34 | claude | รวบรวม Requirements |นำไปใช้สร้าง Class Diagram และ Sequence Diagram|
| 14.56 | ChatGPT | หาวิธีดึงข้อมูลจากไฟล์ JSON|นำไปใช้ในการดึงและจัดการข้อมูลจากไฟล์ JSON|
| 15:50 | ChatGPT |ตรวจสอบ Sequence Diagram จาก Class Diagram|นำคำแนะนำไปตรวจสอบ Sequence DiagramกรณีCreate Requestสำเร็จ

