import logging

logging.basicConfig(
    filename="arena_tickets.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def calculate_total_revenue(ticket_list):
    total = 0.0
    for ticket in ticket_list:
        try:
            if ticket.get("status") == "Booked":
                total += ticket["price"]
        except KeyError as e:
            logging.error(f"Missing key while calculating revenue: {e}")
            return 0.0
    return total


def display_tickets(tickets):
    if not tickets:
        print("Hiện chưa có vé nào trong hệ thống.")
        return

    print("\n--- DANH SÁCH VÉ ---")
    print("Mã Vé | Tên Khách Hàng | Giá Vé | Chỗ Ngồi | Trạng Thái")
    print("-" * 60)

    try:
        for t in tickets:
            ticket_id = t["ticket_id"]
            name = t["buyer_name"]
            price = t["price"]
            seat = t["seat"]
            status = t["status"]

            seat_str = f"{seat[0]}-{seat[1]}"
            status_str = status + (" [ĐÃ HỦY]" if status == "Cancelled" else "")

            print(
                f"{ticket_id:<5} | {name:<15} | {price:<6} | {seat_str:<6} | {status_str}"
            )

        logging.info("User viewed ticket list.")

    except KeyError as e:
        print("Lỗi: Một vé đang bị thiếu dữ liệu, vui lòng kiểm tra lại.")
        logging.error(f"Missing key while displaying ticket: {e}")
        print("-" * 60)


def book_ticket(tickets):
    print("\n--- ĐẶT VÉ MỚI ---")
    ticket_id = input("Nhập mã vé: ").strip().upper()
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            print(f"Lỗi: Mã vé {ticket_id} đã tồn tại.")
            logging.warning(f"Duplicate ticket ID entered: {ticket_id}")
            return

    name = input("Nhập tên khách hàng: ").strip().title()
    while True:
        price_input = input("Nhập giá vé: ").strip()
        try:
            price = float(price_input)
            if price <= 0:
                print("Giá vé phải lớn hơn 0. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Giá vé phải là số. Vui lòng nhập lại.")
            logging.warning("Invalid price input while booking ticket")

    row = input("Nhập khu vực ghế: ").strip().upper()

    while True:
        seat_input = input("Nhập số ghế: ").strip()
        try:
            seat_number = int(seat_input)
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    new_ticket = {
        "ticket_id": ticket_id,
        "buyer_name": name,
        "price": price,
        "status": "Booked",
        "seat": (row, seat_number),
    }

    tickets.append(new_ticket)
    print(f"\nThành công: Đã đặt vé {ticket_id} cho khách hàng {name}.")
    logging.info(f"Booked new ticket {ticket_id} for {name}")


def change_seat(tickets):
    print("\n--- ĐỔI CHỖ NGỒI ---")
    ticket_id = input("Nhập mã vé cần đổi chỗ: ").strip().upper()

    ticket = None

    for t in tickets:
        if t["ticket_id"] == ticket_id:
            ticket = t
            break

    if ticket is None:
        print(f"\nKhông tìm thấy vé mang mã {ticket_id}.")
        logging.warning(f"Change seat failed - Ticket {ticket_id} not found")
        return

    new_row = input("Nhập khu vực ghế mới: ").strip().upper()

    while True:
        new_seat_input = input("Nhập số ghế mới: ").strip()
        try:
            new_seat_number = int(new_seat_input)
            break
        except ValueError:
            print("Số ghế phải là số nguyên. Vui lòng nhập lại.")

    ticket["seat"] = (new_row, new_seat_number)

    print(f"\nThành công: Đã đổi chỗ vé {ticket_id} sang {new_row}-{new_seat_number}.")
    logging.info(f"Seat changed for ticket {ticket_id} to {new_row}-{new_seat_number}")


def cancel_ticket(tickets):
    print("\n--- HỦY VÉ ---")
    ticket_id = input("Nhập mã vé cần hủy: ").strip().upper()

    ticket = None

    for t in tickets:
        if t["ticket_id"] == ticket_id:
            ticket = t
            break

    if ticket is None:
        print(f"\nKhông tìm thấy vé mang mã {ticket_id}.")
        logging.warning(f"Cancel ticket failed - Ticket {ticket_id} not found")
        return

    if ticket["status"] == "Cancelled":
        print(f"\nVé {ticket_id} đã ở trạng thái Cancelled trước đó.")
        return

    ticket["status"] = "Cancelled"
    print(f"\nThành công: Vé {ticket_id} đã được hủy.")
    logging.warning(f"Ticket {ticket_id} has been cancelled.")


def calculate_revenue(tickets):
    print("\n--- BÁO CÁO DOANH THU ---")

    booked = sum(1 for t in tickets if t.get("status") == "Booked")
    cancelled = sum(1 for t in tickets if t.get("status") == "Cancelled")

    try:
        total = calculate_total_revenue(tickets)
    except KeyError as e:
        print("Lỗi: Một vé đang bị thiếu dữ liệu doanh thu.")
        logging.error(f"Missing key while calculating revenue: {e}")
        total = 0.0

    print(f"Tổng số vé đã đặt: {booked}")
    print(f"Tổng số vé đã hủy: {cancelled}")
    print(f"Tổng doanh thu hợp lệ: {total}")

    logging.info(f"Revenue report generated. Total: {total}")


ticket_db = [
    {
        "ticket_id": "T01",
        "buyer_name": "Nguyen Van A",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 1),
    },
    {
        "ticket_id": "T02",
        "buyer_name": "Tran Thi B",
        "price": 300.0,
        "status": "Cancelled",
        "seat": ("B", 5),
    },
    {
        "ticket_id": "T03",
        "buyer_name": "Le Van C",
        "price": 500.0,
        "status": "Booked",
        "seat": ("A", 2),
    },
]


def main():
    while True:
        print("""
=== HỆ THỐNG QUẢN LÝ VÉ RIKKEI ESPORTS ===
1. Xem danh sách vé đã bán
2. Đặt vé mới
3. Đổi chỗ ngồi
4. Hủy vé
5. Báo cáo doanh thu
6. Thoát chương trình
========================================
""")

        choice = input("Chọn chức năng (1-6): ").strip()
        match choice:
            case "1":
                display_tickets(ticket_db)

            case "2":
                book_ticket(ticket_db)

            case "3":
                change_seat(ticket_db)

            case "4":
                cancel_ticket(ticket_db)

            case "5":
                calculate_revenue(ticket_db)

            case "6":
                print("Cảm ơn bạn đã sử dụng hệ thống quản lý vé Rikkei Esports.")
                logging.info("Ticket management system closed.")
                break
            case _:
                print("Lựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 6.")


if __name__ == "__main__":
    main()
