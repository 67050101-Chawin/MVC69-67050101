from Model.datastore import DataStore
from Model.request_service import RequestService
from Model.models import RequestStatus
from Model.models import RoleType


# ใช้ข้อมูลชุดเดียวกันตลอด T1-T6
datastore = DataStore()
service = RequestService(datastore)


# ==================================
# T1
# M05 สร้างคำขอเปลี่ยนบทบาท M01
# PRODUCER -> EDITOR
# ==================================

print("T1")

success, result = service.create_request(
    "M05",
    "M01",
    "EDITOR"
)

assert success

request = result

assert request.status == RequestStatus.PENDING

print("PASS - สร้างคำขอสำเร็จ")
print("Request ID:", request.id)


# ==================================
# T2
# M03 พยายามสร้างคำขอใหม่ให้ M01
# แต่ M01 มี Pending อยู่แล้ว
# ==================================

print()
print("T2")

success, message = service.create_request(
    "M03",
    "M01",
    "CREATOR"
)

assert success == False

print("PASS - ระบบปฏิเสธคำขอซ้ำ")
print(message)


# ==================================
# T3
# M04 ลง APPROVE ให้ C01
# C01 มี M03 APPROVE อยู่แล้ว
# จึงครบ 2 APPROVE
# M02 เปลี่ยนเป็น EDITOR
# ==================================

print()
print("T3")

success, message = service.add_vote(
    "C01",
    "M04",
    "APPROVE"
)

assert success

request = datastore.find_request("C01")

assert request.approve_count() == 2
assert request.status == RequestStatus.APPROVED

assert request.target.role == RoleType.EDITOR

print("PASS - C01 อนุมัติแล้ว")
print("M02 Role:", request.target.role.value)


# ==================================
# T4
# M05 ลง REJECT ให้ C02
# C02 มี M04 REJECT อยู่แล้ว
# ครบ 2 REJECT
# ==================================

print()
print("T4")

success, message = service.add_vote(
    "C02",
    "M05",
    "REJECT"
)

assert success

request = datastore.find_request("C02")

assert request.reject_count() == 2
assert request.status == RequestStatus.REJECTED

print("PASS - C02 ไม่อนุมัติแล้ว")


# ==================================
# T5
# M03 ยกเลิก C03
# C03 ยังไม่มีคนลงความเห็น
# ==================================

print()
print("T5")

success, message = service.cancel_request(
    "C03",
    "M03"
)

assert success

request = datastore.find_request("C03")

assert request.status == RequestStatus.CANCELLED

print("PASS - C03 ยกเลิกสำเร็จ")


# ==================================
# T6
# M05 พยายามลง APPROVE ให้ C04
# แต่ M05 เป็นสมาชิกเป้าหมาย
# ==================================

print()
print("T6")

success, message = service.add_vote(
    "C04",
    "M05",
    "APPROVE"
)

assert success == False

request = datastore.find_request("C04")

assert request.status == RequestStatus.PENDING

print("PASS - ระบบปฏิเสธเพราะ M05 เป็นเป้าหมาย")


# ==================================
# สรุป
# ==================================

print()
print("==============================")
print("T1 - PASS")
print("T2 - PASS")
print("T3 - PASS")
print("T4 - PASS")
print("T5 - PASS")
print("T6 - PASS")
print("==============================")
print("ทดสอบผ่านทั้งหมด 6/6")