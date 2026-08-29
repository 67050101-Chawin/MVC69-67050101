from dataclasses import dataclass, field
from typing import List
from .models import ChangeRequest, Comment, Decision, InvalidOperationException, Member, RoleType, RequestStatus
from .repository import ChangeRequestRepository, MemberRepository

REQUIRED_VOTES = 2

@dataclass
class SummaryReport:
    pending: List[ChangeRequest] = field(default_factory=list)
    approved: List[ChangeRequest] = field(default_factory=list)
    rejected: List[ChangeRequest] = field(default_factory=list)
    cancelled: List[ChangeRequest] = field(default_factory=list)

class RequestService:
    def __init__(self, member_repo, request_repo: ChangeRequestRepository = None):
        if hasattr(member_repo, "member_repo") and hasattr(member_repo, "request_repo") and request_repo is None:
            self.member_repo = member_repo.member_repo
            self.request_repo = member_repo.request_repo
        else:
            self.member_repo = member_repo
            self.request_repo = request_repo or ChangeRequestRepository(member_repo)

    def create_request(self, proposer_id: str, target_id: str, new_role):
        try:
            proposer = self._require_member(proposer_id)
            target = self._require_member(target_id)
            if proposer.id == target.id:
                raise InvalidOperationException("ผู้เสนอไม่สามารถเป็นสมาชิกเป้าหมายของคำขอตนเองได้")
            if not proposer.is_active() or not target.is_active():
                raise InvalidOperationException("ผู้เสนอและสมาชิกเป้าหมายต้องมีสถานะ Active")
            existing = self.request_repo.find_pending_by_target(target.id)
            if existing:
                raise InvalidOperationException(
                    f"สมาชิกเป้าหมาย {target.id} มีคำขอที่ยัง 'รอพิจารณา' อยู่แล้ว ({existing.id})"
                )
            if isinstance(new_role, str):
                try:
                    new_role = RoleType(new_role)
                except ValueError:
                    raise InvalidOperationException(f"บทบาทใหม่ไม่ถูกต้อง: {new_role}")
            new_id = self.request_repo.generate_next_id()
            request = ChangeRequest(request_id=new_id, proposer=proposer, target=target, new_role=new_role)
            self.request_repo.add(request)
            return True, request
        except InvalidOperationException as e:
            return False, str(e)

    def submit_comment(self, request_id: str, voter_id: str, decision):
        try:
            request = self._require_request(request_id)
            voter = self._require_member(voter_id)
            if request.is_finalized():
                raise InvalidOperationException(
                    f"คำขอ {request.id} สิ้นสุดแล้ว (สถานะ={request.status.value}) ไม่สามารถลงความเห็นเพิ่มได้"
                )
            if not voter.is_active():
                raise InvalidOperationException(f"สมาชิก {voter.id} ไม่ได้อยู่ในสถานะ Active")
            if voter.id == request.proposer.id or voter.id == request.target.id:
                raise InvalidOperationException(
                    f"สมาชิก {voter.id} เป็นผู้เสนอหรือสมาชิกเป้าหมายของคำขอนี้ ไม่มีสิทธิ์ลงความเห็น"
                )
            if request.has_voted(voter.id):
                raise InvalidOperationException(f"สมาชิก {voter.id} เคยลงความเห็นต่อคำขอนี้ไปแล้ว")
            if isinstance(decision, str):
                try:
                    decision = Decision(decision)
                except ValueError:
                    raise InvalidOperationException(f"ความเห็นไม่ถูกต้อง: {decision}")
            comment = Comment(voter=voter, decision=decision, seq_no=request.next_seq_no())
            request.add_comment(comment)
            self._finalize_if_needed(request)
            return True, request
        except InvalidOperationException as e:
            return False, str(e)

  
    add_vote = submit_comment

    def _finalize_if_needed(self, request: ChangeRequest):
        if request.approve_count() >= REQUIRED_VOTES:
            request.status = RequestStatus.APPROVED
            request.target.change_role(request.new_role)
            return
        if request.reject_count() >= REQUIRED_VOTES:
            request.status = RequestStatus.REJECTED

    def cancel_request(self, request_id: str, requester_id: str):
        try:
            request = self._require_request(request_id)
            if request.proposer.id != requester_id:
                raise InvalidOperationException("มีเพียงผู้เสนอคำขอเท่านั้นที่ยกเลิกคำขอนี้ได้")
            if request.status != RequestStatus.PENDING:
                raise InvalidOperationException(
                    f"คำขอ {request.id} ไม่ได้อยู่ในสถานะ 'รอพิจารณา' (ปัจจุบัน={request.status.value})"
                )
            if len(request.comments) > 0:
                raise InvalidOperationException(
                    f"คำขอ {request.id} มีความเห็นถูกบันทึกแล้ว ({len(request.comments)} ความเห็น) ไม่สามารถยกเลิกได้"
                )
            request.status = RequestStatus.CANCELLED
            return True, request
        except InvalidOperationException as e:
            return False, str(e)

    def get_summary(self):
        report = SummaryReport()
        for r in self.request_repo.find_all():
            if r.status == RequestStatus.PENDING:
                report.pending.append(r)
            elif r.status == RequestStatus.APPROVED:
                report.approved.append(r)
            elif r.status == RequestStatus.REJECTED:
                report.rejected.append(r)
            elif r.status == RequestStatus.CANCELLED:
                report.cancelled.append(r)
        return report

    def _require_member(self, member_id: str) -> Member:
        member = self.member_repo.find_by_id(member_id)
        if member is None:
            raise InvalidOperationException(f"ไม่พบสมาชิก {member_id}")
        return member

    def _require_request(self, request_id: str) -> ChangeRequest:
        request = self.request_repo.find_by_id(request_id)
        if request is None:
            raise InvalidOperationException(f"ไม่พบคำขอ {request_id}")
        return request
