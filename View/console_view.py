class ConsoleView:

    def show_menu(self):

        print()
        print("================================")
        print("   Friends Forever System")
        print("================================")
        print("1. ดูสมาชิก")
        print("2. สร้างคำขอเปลี่ยนบทบาท")
        print("3. ลงความเห็น")
        print("4. ยกเลิกคำขอ")
        print("5. ดูคำขอทั้งหมด")
        print("6. ดูสรุปคำขอ")
        print("0. ออกจากโปรแกรม")
        print("================================")

    def read_menu(self):

        return input("เลือกเมนู: ")

    # -------------------------

    def show_members(self, members):

        print()
        print("----------- สมาชิก -----------")

        for member in members:

            print(
                member.id,
                "|",
                member.name,
                "|",
                member.role.value,
                "| Active"
            )

    # -------------------------

    def show_create_request(self):

        print()
        print("------ สร้างคำขอเปลี่ยนบทบาท ------")

    def read_request_input(self):

        proposer_id = input(
            "รหัสผู้เสนอ: "
        )

        target_id = input(
            "รหัสสมาชิกเป้าหมาย: "
        )

        new_role = input(
            "บทบาทใหม่: "
        ).upper()

        return proposer_id, target_id, new_role

    # -------------------------

    def read_request_id(self, text):

        return input(
            "รหัสคำขอที่ต้องการ" + text + ": "
        )

    # -------------------------

    def read_member_id(self):

        return input(
            "รหัสสมาชิก: "
        )

    # -------------------------

    def read_vote_input(self):

        voter_id = input(
            "รหัสผู้ลงความเห็น: "
        )

        choice = input(
            "ลงความเห็น APPROVE/REJECT: "
        ).upper()

        return voter_id, choice

    # -------------------------

    def show_requests(self, requests):

        print()
        print("----------- คำขอทั้งหมด -----------")

        if len(requests) == 0:
            print("ยังไม่มีคำขอ")
            return

        for request in requests:

            print(
                request.id,
                "| ผู้เสนอ:", request.proposer.id,
                "| เป้าหมาย:", request.target.id,
                "| บทบาท:", request.new_role.value,
                "| สถานะ:", request.status.value,
                "| A:", request.approve_count(),
                "| R:", request.reject_count()
            )

    # -------------------------

    def show_summary(self, summary):

        print()
        print("----------- สรุปคำขอ -----------")

        print(
            "Request:",
            summary["id"]
        )

        print(
            "ผู้เสนอ:",
            summary["proposer"].id,
            summary["proposer"].name
        )

        print(
            "เป้าหมาย:",
            summary["target"].id,
            summary["target"].name
        )

        print(
            "บทบาทใหม่:",
            summary["new_role"]
        )

        print(
            "สถานะ:",
            summary["status"]
        )

        print(
            "Approve:",
            summary["approve"]
        )

        print(
            "Reject:",
            summary["reject"]
        )

        if len(summary["votes"]) > 0:

            print("ผู้ลงความเห็น:")

            for vote in summary["votes"]:

                print(
                    "-",
                    vote.voter.id,
                    vote.voter.name,
                    ":",
                    vote.choice.value
                )

    # -------------------------

    def show_success(self, message):

        print()
        print("[สำเร็จ]", message)

    def show_error(self, message):

        print()
        print("[ผิดพลาด]", message)

    def show_exit(self):

        print("ออกจากโปรแกรม")