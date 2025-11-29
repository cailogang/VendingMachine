from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from storage import VendingMachineStorage
import time

if __name__ == '__main__':
    vending = VendingMachineStorage()
    console = Console()
    try:
        while True:
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

            selection = Prompt.ask(
                "Bạn muốn làm gì? nhập naptien để nạp tiền, nhập muahang để mua sản phẩm từ máy",
                choices=["naptien", "muahang"]
            )

            if selection == "naptien":
                # Xử lý logic nạp tiền
                tien_nap = IntPrompt.ask(
                    "Vui lòng nhập số tiền muốn nạp",
                    console=console
                )
                vending.nap_tien(int(tien_nap))

            elif selection == "muahang":
                id_mon_hang = IntPrompt.ask(
                    "Vui lòng chọn ID sản phẩm theo bảng phía trên",
                    console=console
                )
                if not vending.has_products(int(id_mon_hang)):
                    print(f"Sản phẩm với ID {id_mon_hang} không có trong máy")
                else:
                    product_price = vending.get_product(int(id_mon_hang)).price
                    if vending.get_balance() < product_price:
                        tien_nap = IntPrompt.ask(
                            "Vui lòng nạp thêm tiền"
                        )
                        vending.nap_tien(int(tien_nap))
                    vending.sell_product(int(id_mon_hang))
            else:
                print("Lựa chọn không hợp lý")

            time.sleep(3)
    except KeyboardInterrupt:
        print("Đang tắt...")
    except Exception as err:
        print(f"Đã xảy ra lỗi: {err}")
