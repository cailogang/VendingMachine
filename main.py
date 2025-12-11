from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

from enums import NaptienStatus, BuyProductStatus
from storage import VendingMachineStorage
import time

def display_menu(console: Console, vending: VendingMachineStorage):
    """
    In ra màn hình menu của máy bán hàng tự động
    :param console: Class chính của rich.console.Console, chịu trách nhiệm quản lý hệ thống UI / UX
    :param vending: Class quản lý hệ thống bán hàng
    :return: None
    """

    console.clear()

    table = Table(
        title=f"Máy bán hàng tự động - Bạn đang có {vending.money} VND",
        show_lines=True,
    )

    table.add_column("ID sản phẩm", style="cyan")
    table.add_column("Tên sản phẩm", style="red")
    table.add_column("Giá thành (VND)", style="blue")
    table.add_column("Số lượng còn lại", style="magenta")

    for id, item in vending.get_all_products().items():
        table.add_row(str(id), item.name, str(item.price), str(item.stock))

    console.print(table)

def process_buy_product(console: Console, vending: VendingMachineStorage):
    """
    Hàm phục vụ việc mua hàng của người dùng
    :param console: Class chính của rich.console.Console, chịu trách nhiệm quản lý hệ thống UI / UX
    :param vending: Class quản lý hệ thống bán hàng
    :return: None
    """
    id_mon_hang = IntPrompt.ask(
        "Vui lòng chọn ID sản phẩm theo bảng phía trên",
        console=console
    )

    if not vending.has_products(int(id_mon_hang)):
        console.print(f"Sản phẩm với ID {id_mon_hang} không có trong máy")

    else:
        product = vending.get_product(int(id_mon_hang))

        if product.stock < 1:
            console.print(f"Sản phẩm {product.name} đã hết hàng")
            return

        while vending.get_balance() < product.price:
            process_topup(console, vending, f"Vui lòng nạp thêm tiền, bạn còn thiếu {product.price - vending.money} VND để mua mặt hàng này")
        match vending.sell_product(int(id_mon_hang)):

            case BuyProductStatus.SUCCESS:
                console.print(f"Đã mua sản phẩm {product.name} với giá {product.price} VND, Cảm ơn quý khách đã mua hàng", style="green")
                console.print(f"Bạn còn lại {vending.money} VND", style="cyan")

            case BuyProductStatus.NOT_EXISTS:
                console.print(f"Sản phẩm với id {id_mon_hang} không tỒn tại", style="red")

            case BuyProductStatus.NOT_ENOUGH_MONEY:
                console.print("Bạn không đủ tiền để mua sản phẩm này", style="red")

            case BuyProductStatus.NOT_ENOUGH_STOCK:
                console.print(f"Mặt hàng {product.name} đã hết hàng", style="yellow")

            case BuyProductStatus.FAILED:
                console.print("Mua hàng thất bại vì đã xảy ra lỗi không mong muốn", style="red")

            case _:
                console.print("Đã xảy ra lỗi: Hàm trả về dữ liệu bất thường", style="red")

def process_topup(console: Console, vending: VendingMachineStorage, prompt="Vui lòng nhập số tiền muốn nạp"):
    """
    Hàm xử lý việc nạp tiền
    :param console: Class chính của rich.console.Console, chịu trách nhiệm quản lý hệ thống UI / UX
    :param vending: Class quản lý hệ thống bán hàng
    :param prompt: Prompt để hiển thị yêu cầu cho người dùng
    :return: None
    """
    tien_nap = IntPrompt.ask(
        prompt,
        console=console
    )
    match vending.nap_tien(int(tien_nap)):
        case NaptienStatus.SUCCESS:
            console.print(f"Bạn đã nạp {tien_nap} VND vào tài khoản, số tiền hiện tại {vending.money} VND", style="green")
        case NaptienStatus.UNDER_10K:
            console.print("Cần nạp số tiền lớn hơn hoặc bằng 10.000 VND", style="red")
        case NaptienStatus.INVALID:
            console.print("Giá trị nhập vào không hợp lệ", style="red")
        case _:
            console.print("Đã xảy ra lỗi: Hàm đã trả về giá trị không mong muốn", style="red")

def main():
    vending = VendingMachineStorage()
    console = Console()
    try:
        while True:
            display_menu(console, vending)

            selection = Prompt.ask(
                "Bạn muốn làm gì? nhập naptien để nạp tiền, nhập muahang để mua sản phẩm từ máy",
                choices=["naptien", "muahang"]
            )

            if selection == "naptien":
                process_topup(console, vending)
            elif selection == "muahang":
                process_buy_product(console, vending)
            else:
                console.print("Lựa chọn không hợp lý", style="red")

            time.sleep(3)
    except KeyboardInterrupt:
        console.print("Đang tắt...")
    except Exception as err:
        console.print(f"Đã xảy ra lỗi: {err}")

if __name__ == '__main__':
    main()
