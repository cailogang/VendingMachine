from typing import Dict, Optional
from enums import ProductSellStatus, BuyProductStatus, NaptienStatus

class Product:
    """Đại diện cho mỗi khay hàng trong máy"""
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def add_stock(self, stock):
        self.stock += stock

    def sell(self) -> ProductSellStatus:
        if self.stock < 1:
            return ProductSellStatus.NOT_ENOUGH_STOCK
        self.stock -= 1
        return ProductSellStatus.SUCCESS

    def __str__(self):
        return f"Sản phẩm: {self.name} | giá {self.price} VND | Còn {self.stock} sản phẩm"


class VendingMachineStorage:
    def __init__(self):
        self.products: Dict[int, Product] = {
            1: Product("Coca-Cola", 50_000, 10), # Testcase: Số tiền lớn
            2: Product("Pepsi", 15_000, 0), # Testcase: Hết hàng
            3: Product("Sting Dâu", 10_000, 5),
            4: Product("Red Bull", 20_000, 2),
            5: Product("Nước Suối", 5000, 20),
            6: Product("Trà Xanh Không Độ", 10_000, 7),
            7: Product("Café lon", 20_000, 0),
            8: Product("Olong Tea", 10_000, 9),
            9: Product("Sữa Bắp", 10_000, 3),
            10: Product("Nước Cam Ép", 10_000, 12),
            11: Product("Revive", 10_000, 4),
            12: Product("Aquafina", 10_000, 15),
            13: Product("Trà Sữa Đóng Chai", 20_000, 6),
            14: Product("7Up", 20_000, 8),
            15: Product("Mirinda Cam", 20_000, 5),
            # ID 16 and more: TestCase: hàng không tồn tại
        }

        self.money = 0

    def nap_tien(self, money: int) -> NaptienStatus:
        if not isinstance(money, int):
            return NaptienStatus.INVALID
        if money < 10_000:
            return NaptienStatus.UNDER_10K

        self.money += money
        return NaptienStatus.SUCCESS

    def get_balance(self):
        return self.money

    def has_products(self, id_mon_hang: int):
        return id_mon_hang in self.products

    def get_all_products(self):
        return self.products

    def get_product(self, id) -> Optional[Product]:
        try:
            return self.products[id]
        except KeyError:
            return None

    def sell_product(self, id) -> BuyProductStatus:
        if not self.has_products(id):
            return BuyProductStatus.NOT_EXISTS

        product = self.get_product(id)

        if not product:
            return BuyProductStatus.NOT_EXISTS

        if self.money < product.price:
            return BuyProductStatus.NOT_ENOUGH_MONEY
        if product.stock < 1:
            return BuyProductStatus.NOT_ENOUGH_STOCK
        if product.sell() == ProductSellStatus.SUCCESS:
            self.money -= product.price
            return BuyProductStatus.SUCCESS

        return BuyProductStatus.FAILED

    def reset(self):
        self.products: Dict[int, Product] = {
            1: Product("Coca-Cola", 15000, 10),
            2: Product("Pepsi", 15000, 0),
            3: Product("Sting Dâu", 12000, 5),
            4: Product("Red Bull", 20000, 2),
            5: Product("Nước Suối", 8000, 20),
            6: Product("Trà Xanh Không Độ", 10000, 7),
            7: Product("Café lon", 18000, 0),
            8: Product("Olong Tea", 13000, 9),
            9: Product("Sữa Bắp", 14000, 3),
            10: Product("Nước Cam Ép", 16000, 12),
            11: Product("Revive", 12000, 4),
            12: Product("Aquafina", 9000, 15),
            13: Product("Trà Sữa Đóng Chai", 18000, 6),
            14: Product("7Up", 15000, 8),
            15: Product("Mirinda Cam", 15000, 5),
        }

        return True

