from Model.models import RoleChangeRequest
from Model.models import Vote
from Model.models import RequestStatus


class RequestService:

    def __init__(self, datastore):
        self.datastore = datastore

    # -------------------------
    # สร้างคำขอ
    # -------------------------

    def create_request(self, proposer_id, target_id, new_role):

        proposer = self.datastore.find_member(proposer_id)
        target = self.datastore.find_member(target_id)

        if proposer is None:
            return False, "ไม่พบผู้เสนอ"

        if target is None:
            return False, "ไม่พบสมาชิกเป้าหมาย"

        if not proposer.active:
            return False, "ผู้เสนอไม่ได้เป็นสมาชิก Active"

        if not target.active:
            return False, "สมาชิกเป้าหมายไม่ได้เป็นสมาชิก Active"

        # ผู้เสนอห้ามเป็นเป้าหมาย
        if proposer.id == target.id:
            return False, "ผู้เสนอไม่สามารถเป็นสมาชิกเป้าหมายได้"

        # ห้ามมีคำขอ Pending ของเป้าหมายซ้ำ
        for request in self.datastore.requests:

            if request.target.id == target.id:
                if request.status == RequestStatus.PENDING:
                    return False, "สมาชิกเป้าหมายมีคำขอรอพิจารณาอยู่แล้ว"

        request_id = self.get_next_request_id()

        request = RoleChangeRequest(
            request_id,
            proposer,
            target,
            new_role
        )

        self.datastore.add_request(request)

        return True, request

    # -------------------------
    # สร้าง Request ID
    # -------------------------

    def get_next_request_id(self):

        number = len(self.datastore.requests) + 1

        return "C" + str(number)

    # -------------------------
    # ลงความเห็น
    # -------------------------

    def add_vote(self, request_id, voter_id, choice):

        request = self.datastore.find_request(request_id)
        voter = self.datastore.find_member(voter_id)

        if request is None:
            return False, "ไม่พบคำขอ"

        if voter is None:
            return False, "ไม่พบสมาชิก"

        if not voter.active:
            return False, "สมาชิกไม่ได้อยู่ในสถานะ Active"

        # คำขอจบแล้ว
        if request.is_finished():
            return False, "คำขอนี้จบแล้ว ไม่สามารถลงความเห็นได้"

        # ผู้เสนอห้ามโหวต
        if voter.id == request.proposer.id:
            return False, "ผู้เสนอไม่สามารถลงความเห็นคำขอของตนเองได้"

        # สมาชิกเป้าหมายห้ามโหวต
        if voter.id == request.target.id:
            return False, "สมาชิกเป้าหมายไม่สามารถลงความเห็นคำขอนี้ได้"

        # โหวตซ้ำ
        if request.has_voted(voter.id):
            return False, "สมาชิกคนนี้ลงความเห็นไปแล้ว"

        vote = Vote(choice, voter)

        request.votes.append(vote)

        # ตรวจสอบผลทันที
        self.check_result(request)

        return True, "ลงความเห็นสำเร็จ"

    # -------------------------
    # ตรวจสอบผลการโหวต
    # -------------------------

    def check_result(self, request):

        # APPROVE ครบ 2
        if request.approve_count() >= 2:

            request.status = RequestStatus.APPROVED

            request.target.change_role(
                request.new_role
            )

        # REJECT ครบ 2
        elif request.reject_count() >= 2:

            request.status = RequestStatus.REJECTED

    # -------------------------
    # ยกเลิกคำขอ
    # -------------------------

    def cancel_request(self, request_id, proposer_id):

        request = self.datastore.find_request(request_id)

        if request is None:
            return False, "ไม่พบคำขอ"

        # ต้องเป็นผู้เสนอ
        if request.proposer.id != proposer_id:
            return False, "เฉพาะผู้เสนอเท่านั้นที่ยกเลิกได้"

        # ต้อง Pending
        if request.status != RequestStatus.PENDING:
            return False, "คำขอนี้ไม่อยู่ในสถานะรอพิจารณา"

        # ถ้ามีคนโหวตแล้ว ยกเลิกไม่ได้
        if len(request.votes) > 0:
            return False, "คำขอที่มีความเห็นแล้วไม่สามารถยกเลิกได้"

        request.status = RequestStatus.CANCELLED

        return True, "ยกเลิกคำขอสำเร็จ"

    # -------------------------
    # สรุปผล
    # -------------------------

    def get_request_summary(self, request_id):

        request = self.datastore.find_request(request_id)

        if request is None:
            return None

        summary = {
            "id": request.id,
            "proposer": request.proposer,
            "target": request.target,
            "new_role": request.new_role.value,
            "status": request.status.value,
            "approve": request.approve_count(),
            "reject": request.reject_count(),
            "votes": request.votes,
            "comments": request.comments
        }

        return summary