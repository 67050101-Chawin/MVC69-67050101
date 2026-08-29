class RequestController:

    def __init__(self, service, view):

        self.service = service
        self.view = view

    # -------------------------
    # ดูสมาชิก
    # -------------------------

    def show_members(self):

        members = self.service.datastore.get_active_members()

        self.view.show_members(members)

    # -------------------------
    # สร้างคำขอ
    # -------------------------

    def create_request(self):

        self.view.show_create_request()

        proposer_id, target_id, new_role = \
            self.view.read_request_input()

        success, result = \
            self.service.create_request(
                proposer_id,
                target_id,
                new_role
            )

        if success:

            self.view.show_success(
                "สร้างคำขอ " + result.id + " สำเร็จ"
            )

        else:

            self.view.show_error(result)

    # -------------------------
    # ลงความเห็น
    # -------------------------

    def vote_on_request(self):

        request_id = self.view.read_request_id(
            "ลงความเห็น"
        )

        voter_id, choice = \
            self.view.read_vote_input()

        success, message = \
            self.service.add_vote(
                request_id,
                voter_id,
                choice
            )

        if success:

            self.view.show_success(message)

        else:

            self.view.show_error(message)

    # -------------------------
    # ยกเลิก
    # -------------------------

    def cancel_request(self):

        request_id = self.view.read_request_id(
            "ยกเลิก"
        )

        proposer_id = self.view.read_member_id()

        success, message = \
            self.service.cancel_request(
                request_id,
                proposer_id
            )

        if success:

            self.view.show_success(message)

        else:

            self.view.show_error(message)

    # -------------------------
    # ดูคำขอทั้งหมด
    # -------------------------

    def show_requests(self):

        requests = self.service.datastore.requests

        self.view.show_requests(requests)

    # -------------------------
    # ดูสรุป
    # -------------------------

    def show_summary(self):

        request_id = self.view.read_request_id(
            "ดูสรุป"
        )

        summary = \
            self.service.get_request_summary(
                request_id
            )

        if summary is None:

            self.view.show_error(
                "ไม่พบคำขอ"
            )

        else:

            self.view.show_summary(summary)