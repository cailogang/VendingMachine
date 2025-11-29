from typing import Dict, Optional


class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def add_stock(self, stock):
        self.stock += stock

    def sell(self):
        if self.stock < 1:
            print("Đã hết hàng")
            return
        self.stock -= 1
        print(f"Đã mua sản phẩm {self.name} với giá {self.price}VND, Cảm ơn quý khách đã mua hàng")


    def __str__(self):
        return f"Sản phẩm: {self.name} | giá {self.price} VND | Còn {self.stock} sản phẩm"


class VendingMachineStorage:
    def __init__(self):
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

        self.money = 0

    def nap_tien(self, money):
        if money < 10_000:
            print("Cần nạp số tiền lớn hơn hoặc bằng 10.000 VND")
            return self.money

        self.money += money
        print(f"Bạn đã nạp {money} VND vào tài khoản, số tiền hiện tại {self.money} VND")

        return self.money

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

    def sell_product(self, id):
        if not self.has_products(id):
            print(f"Sản phẩm với ID: {id} Không tồn tại")
            return

        product = self.get_product(id)

        if not product:
            print(f"Sản phẩm với ID: {id} Không tồn tại")
            return

        if self.money < product.price:
            print("Không đủ tiền để mua sản phẩm này")
            return
        if product.stock < 1:
            print(f"Sản phẩm {product.name} đã hết hàng")
            return

        self.money -= product.price
        product.sell()
        # print(f"Bạn đã mua {product.name} với giá {product.price}, số tiền còn lại của bạn là: {self.money}")

    def restock(self):
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

