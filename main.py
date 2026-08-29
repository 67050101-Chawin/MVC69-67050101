from Model.datastore import datastore
from Model.request_service import RequestService

from View.console_view import ConsoleView

from Controller.request_controller import RequestController


def main():

    # Model
    datastore = datastore()
    service = RequestService(datastore)

    # View
    view = ConsoleView()

    # Controller
    controller = RequestController(
        service,
        view
    )

    # โปรแกรมหลัก
    while True:

        view.show_menu()

        choice = view.read_menu()

        if choice == "1":

            controller.show_members()

        elif choice == "2":

            controller.create_request()

        elif choice == "3":

            controller.vote_on_request()

        elif choice == "4":

            controller.cancel_request()

        elif choice == "5":

            controller.show_requests()

        elif choice == "6":

            controller.show_summary()

        elif choice == "0":

            view.show_exit()
            break

        else:

            view.show_error(
                "กรุณาเลือกเมนู 0-6"
            )


if __name__ == "__main__":
    main()