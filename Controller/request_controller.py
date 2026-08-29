from Model.models import Decision, InvalidOperationException, RoleType
from Model.request_service import RequestService

class RequestController:
    def __init__(self, service, view):
        self.service = service
        self.view = view

    def _call(self, fn, *args):
        try:
            return fn(*args)
        except InvalidOperationException as e:
            return False, str(e)

    def show_members(self):
        for m in self.service.member_repo.find_all():
            print(m)

    def create_request(self):
        proposer_id=input("รหัสผู้เสนอ: ").strip()
        target_id=input("รหัสสมาชิกเป้าหมาย: ").strip()
        new_role=input("บทบาทใหม่: ").strip().upper()
        ok, result=self._call(self.service.create_request, proposer_id,target_id,new_role)
        print(f"สร้างคำขอสำเร็จ: {result.id}" if ok else f"[ปฏิเสธ] {result}")

    def vote_on_request(self):
        rid=input("รหัสคำขอ: ").strip()
        vid=input("รหัสผู้ลงความเห็น: ").strip()
        decision=input("ความเห็น (APPROVE/REJECT): ").strip().upper()
        ok,result=self._call(self.service.add_vote,rid,vid,decision)
        print(f"บันทึกความเห็นสำเร็จ. คำขอ {rid} สถานะปัจจุบัน={result.status.value}" if ok else f"[ปฏิเสธ] {result}")

    def cancel_request(self):
        rid=input("รหัสคำขอ: ").strip()
        uid=input("รหัสผู้เสนอ: ").strip()
        ok,result=self._call(self.service.cancel_request,rid,uid)
        print(f"ยกเลิกคำขอ {rid} สำเร็จ สถานะ={result.status.value}" if ok else f"[ปฏิเสธ] {result}")

    def show_requests(self):
        for r in self.service.request_repo.find_all():
            print(r)

    def show_summary(self):
        s=self.service.get_summary()
        print(f"รอพิจารณา: {len(s.pending)} รายการ")
        print(f"อนุมัติแล้ว: {len(s.approved)} รายการ")
        print(f"ไม่อนุมัติ: {len(s.rejected)} รายการ")
        print(f"ยกเลิก: {len(s.cancelled)} รายการ")

    # Compatibility names from the older controller implementation.
    show_members_and_requests = show_members
