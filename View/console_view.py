class ConsoleView:
    def show_menu(self):
        print("\n=== ระบบจัดการคำขอเปลี่ยนบทบาทสมาชิก ===")
        print("1) ดูสมาชิกและคำขอ")
        print("2) สร้างคำขอเปลี่ยนบทบาท")
        print("3) ลงความเห็นต่อคำขอ")
        print("4) ยกเลิกคำขอ")
        print("5) ดูคำขอทั้งหมด")
        print("6) ดูสรุปผล")
        print("0) ออกจากโปรแกรม")

    def read_menu(self):
        return input("เลือกเมนู: ").strip()

    def show_exit(self):
        print("ออกจากโปรแกรม")

    def show_error(self, message):
        print(f"[ปฏิเสธ] {message}")
