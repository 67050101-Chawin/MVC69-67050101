from pathlib import Path
from .repository import MemberRepository, ChangeRequestRepository, load_seed_file

class DataStore:
    def __init__(self, seed_path=None):
        if seed_path is None:
            seed_path = Path(__file__).resolve().parent.parent / "seed_data.json"
        data = load_seed_file(seed_path)
        self.member_repo = MemberRepository()
        self.member_repo.load_from_seed(data)
        self.request_repo = ChangeRequestRepository(self.member_repo)
        self.request_repo.load_from_seed(data)

    def find_request(self, request_id):
        return self.request_repo.find_by_id(request_id)

    def find_member(self, member_id):
        return self.member_repo.find_by_id(member_id)

    def all_members(self):
        return self.member_repo.find_all()

    def all_requests(self):
        return self.request_repo.find_all()

# Backward-compatible lowercase name used by the original main.py.
datastore = DataStore
