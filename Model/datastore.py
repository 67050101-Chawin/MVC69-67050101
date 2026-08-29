import json

from Model.models import Member
from Model.models import RoleChangeRequest
from Model.models import Vote


class datastore:

    def __init__(self):
        self.members = []
        self.requests = []

        self.load_seed_data()

    def load_seed_data(self):

        with open("seed_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # โหลดสมาชิก
        for item in data["members"]:

            member = Member(
                item["id"],
                item["name"],
                item["role"],
                item["active"]
            )

            self.members.append(member)

        # โหลดคำขอ
        for item in data["requests"]:

            proposer = self.find_member(item["proposer"])
            target = self.find_member(item["target"])

            request = RoleChangeRequest(
                item["id"],
                proposer,
                target,
                item["new_role"]
            )

            # กำหนดสถานะ
            request.status = request.status.__class__(
                item["status"]
            )

            # โหลด comment
            for comment in item.get("comments", []):
                request.add_comment(comment)

            # โหลด vote
            for vote_data in item.get("votes", []):

                voter = self.find_member(
                    vote_data["voter"]
                )

                vote = Vote(
                    vote_data["choice"],
                    voter
                )

                request.votes.append(vote)

            self.requests.append(request)

    def find_member(self, member_id):

        for member in self.members:

            if member.id == member_id:
                return member

        return None

    def find_request(self, request_id):

        for request in self.requests:

            if request.id == request_id:
                return request

        return None

    def get_active_members(self):

        members = []

        for member in self.members:

            if member.active:
                members.append(member)

        return members

    def add_request(self, request):
        self.requests.append(request)