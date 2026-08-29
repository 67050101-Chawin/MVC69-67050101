from enum import Enum


class RoleType(Enum):
    PRODUCER = "PRODUCER"
    FINANCE = "FINANCE"
    EDITOR = "EDITOR"
    CREATOR = "CREATOR"


class RequestStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


class VoteChoice(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"


class Member:
    def __init__(self, member_id, name, role, active=True):
        self.id = member_id
        self.name = name
        self.role = RoleType(role)
        self.active = active

    def change_role(self, new_role):
        self.role = RoleType(new_role)


class Vote:
    def __init__(self, choice, voter):
        self.choice = VoteChoice(choice)
        self.voter = voter


class RoleChangeRequest:
    def __init__(self, request_id, proposer, target, new_role):
        self.id = request_id
        self.proposer = proposer
        self.target = target
        self.new_role = RoleType(new_role)

        self.status = RequestStatus.PENDING
        self.comments = []
        self.votes = []

    def add_comment(self, comment):
        self.comments.append(comment)

    def approve_count(self):
        count = 0

        for vote in self.votes:
            if vote.choice == VoteChoice.APPROVE:
                count += 1

        return count

    def reject_count(self):
        count = 0

        for vote in self.votes:
            if vote.choice == VoteChoice.REJECT:
                count += 1

        return count

    def has_voted(self, member_id):
        for vote in self.votes:
            if vote.voter.id == member_id:
                return True

        return False

    def is_finished(self):
        return self.status != RequestStatus.PENDING