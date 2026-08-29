from enum import Enum
from typing import List, Optional

class RoleType(Enum):
    PRODUCER = "PRODUCER"
    FINANCE = "FINANCE"
    EDITOR = "EDITOR"
    CREATOR = "CREATOR"

class RequestStatus(Enum):
    PENDING = "รอพิจารณา"
    APPROVED = "อนุมัติแล้ว"
    REJECTED = "ไม่อนุมัติ"
    CANCELLED = "ยกเลิก"

class Decision(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"

class InvalidOperationException(Exception):
    """ใช้เมื่อ business rule ของระบบไม่อนุญาตให้ดำเนินการ"""
    def __init__(self, reason: str):
        super().__init__(reason)

class Member:
    def __init__(self, member_id: str, name: str, role: RoleType, active: bool = True):
        self.id = member_id
        self.name = name
        self.role = role
        self.active = active

    def change_role(self, new_role: RoleType):
        self.role = new_role

    def is_active(self) -> bool:
        return self.active

    def __repr__(self):
        return f"Member(id={self.id}, name={self.name}, role={self.role.value})"

class Comment:
    def __init__(self, voter: Member, decision: Decision, seq_no: int):
        self.voter = voter
        self.decision = decision
        self.seq_no = seq_no

    def __repr__(self):
        return f"Comment(voter={self.voter.id}, decision={self.decision.value}, seq={self.seq_no})"

class ChangeRequest:
    def __init__(self, request_id: str, proposer: Member, target: Member,
                 new_role: RoleType, comments: Optional[List[Comment]] = None):
        self.id = request_id
        self.proposer = proposer
        self.target = target
        self.new_role = new_role
        self.status = RequestStatus.PENDING
        self.comments = comments if comments is not None else []

    def has_voted(self, member_id: str) -> bool:
        return any(c.voter.id == member_id for c in self.comments)

    def approve_count(self) -> int:
        return sum(c.decision == Decision.APPROVE for c in self.comments)

    def reject_count(self) -> int:
        return sum(c.decision == Decision.REJECT for c in self.comments)

    def is_finalized(self) -> bool:
        return self.status in (RequestStatus.APPROVED, RequestStatus.REJECTED, RequestStatus.CANCELLED)

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def next_seq_no(self) -> int:
        return len(self.comments) + 1

    def __repr__(self):
        return (f"ChangeRequest(id={self.id}, {self.proposer.id}->{self.target.id}, "
                f"new_role={self.new_role.value}, status={self.status.value}, comments={self.comments})")
