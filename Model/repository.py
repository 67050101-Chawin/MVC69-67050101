import json
from typing import Dict, List, Optional
from .models import ChangeRequest, Comment, Member, RoleType, Decision

class MemberRepository:
    def __init__(self):
        self._members: Dict[str, Member] = {}

    def load_from_seed(self, data: dict):
        for m in data.get("members", []):
            member = Member(
                member_id=m["id"], name=m["name"],
                role=RoleType(m["role"]), active=m.get("active", True)
            )
            self._members[member.id] = member

    def find_by_id(self, member_id: str) -> Optional[Member]:
        return self._members.get(member_id)

    def find_all(self) -> List[Member]:
        return list(self._members.values())

class ChangeRequestRepository:
    def __init__(self, member_repo: MemberRepository):
        self._member_repo = member_repo
        self._requests: Dict[str, ChangeRequest] = {}
        self._next_auto_id = 1

    def load_from_seed(self, data: dict):
        for r in data.get("requests", []):
            proposer = self._member_repo.find_by_id(r["proposer"])
            target = self._member_repo.find_by_id(r["target"])
            if proposer is None or target is None:
                continue
            comments = []
            for idx, c in enumerate(r.get("comments", []), start=1):
                voter = self._member_repo.find_by_id(c["voter"])
                if voter is not None:
                    comments.append(Comment(voter=voter, decision=Decision(c["decision"]), seq_no=idx))
            req = ChangeRequest(
                request_id=r["id"], proposer=proposer, target=target,
                new_role=RoleType(r["new_role"]), comments=comments
            )
            # Seed may contain a finalized status; otherwise derive it from votes.
            status = r.get("status")
            if status:
                from .models import RequestStatus
                req.status = RequestStatus[status] if status in RequestStatus.__members__ else RequestStatus(status)
            self._requests[req.id] = req

        used_numbers = [
            int(rid[1:]) for rid in self._requests
            if rid.startswith("C") and rid[1:].isdigit()
        ]
        self._next_auto_id = max(used_numbers) + 1 if used_numbers else 1

    def find_by_id(self, request_id: str) -> Optional[ChangeRequest]:
        return self._requests.get(request_id)

    def find_all(self) -> List[ChangeRequest]:
        return list(self._requests.values())

    def find_pending_by_target(self, target_id: str) -> Optional[ChangeRequest]:
        from .models import RequestStatus
        for r in self._requests.values():
            if r.target.id == target_id and r.status == RequestStatus.PENDING:
                return r
        return None

    def add(self, request: ChangeRequest):
        self._requests[request.id] = request

    def generate_next_id(self) -> str:
        new_id = f"C{self._next_auto_id:02d}"
        self._next_auto_id += 1
        return new_id

def load_seed_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
