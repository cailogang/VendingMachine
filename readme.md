# Yêu cầu bài đến từ
[LHU elearning](https://learn.lhu.edu.vn/mod/assign/view.php?id=275403&forceview=1)

Đề tài 3: Máy Bán Hàng Quản Lý Tồn Kho 📦(Số nhóm được chọn: 1)

·         Mô tả đề tài: Đây là phiên bản nâng cao của bài toán máy bán hàng tự động. Thay vì chỉ bán hàng, chương trình còn phải quản lý số lượng tồn kho của từng sản phẩm. Thử thách của đề tài là quản lý trạng thái của nhiều đối tượng (sản phẩm) bằng các biến đơn giản và đảm bảo dữ liệu (số lượng, tiền) được cập nhật chính xác sau mỗi giao dịch.

·         Yêu cầu chi tiết:

1.      Khởi tạo ít nhất 3 sản phẩm, mỗi sản phẩm có tên, giá bán, và số lượng tồn kho ban đầu.

2.      Hiển thị menu sản phẩm cho người dùng, kèm theo giá và số lượng còn lại.

3.      Khi người dùng chọn mua một sản phẩm, chương trình phải kiểm tra đồng thời 2 điều kiện: sản phẩm có còn hàng không và người dùng có đủ tiền không.

4.      Nếu giao dịch thành công, chương trình phải: trừ tiền của người dùng, giảm số lượng tồn kho của sản phẩm đi 1, và thông báo thành công.

5.      Nếu sản phẩm đã hết hàng hoặc người dùng không đủ tiền, phải đưa ra thông báo lỗi tương ứng.

6.      Menu phải được cập nhật sau mỗi lần mua để phản ánh đúng số lượng tồn kho mới.


# Cách hoạt động của chương trình này

Chương trình này mô phỏng một máy bán hàng tự động (Vending Machine) chạy trên giao diện dòng lệnh (CLI). Nó bao gồm quản lý kho hàng, xử lý giao dịch mua bán và giao diện người dùng tương tác.

### Yêu cầu cài đặt

Chương trình sử dụng thư viện `rich` để hiển thị giao diện đẹp mắt.

```bash
pip install rich
```

-----

## 1\. Tệp `storage.py` - Xử lý Logic và Dữ liệu

Tệp này chứa các lớp (class) định nghĩa sản phẩm và logic quản lý của máy bán hàng.

### Class `Product`

Đại diện cho một mặt hàng cụ thể trong máy.

#### Hàm khởi tạo `__init__`

Thiết lập các thuộc tính cơ bản: tên, giá và số lượng tồn kho.

```python
def __init__(self, name, price, stock):
    self.name = name
    self.price = price
    self.stock = stock
```

#### Hàm `sell()`

Xử lý logic khi một sản phẩm đơn lẻ được bán ra. Nó kiểm tra xem còn hàng không (`stock < 1`), nếu còn thì trừ đi 1 đơn vị và in thông báo.

```python
def sell(self):
    if self.stock < 1:
        print("Đã hết hàng")
        return
    self.stock -= 1
    print(f"Đã mua sản phẩm {self.name} với giá {self.price}VND, Cảm ơn quý khách đã mua hàng")
```

-----

### Class `VendingMachineStorage`

Đây là lớp quản lý chính, chứa danh sách tất cả sản phẩm và số dư tiền của người dùng.

#### Hàm khởi tạo `__init__`

Khởi tạo danh sách sản phẩm (`self.products`) dưới dạng từ điển (Dictionary) với ID làm khóa và đối tượng `Product` làm giá trị. Đồng thời khởi tạo ví tiền `self.money` bằng 0.

```python
def __init__(self):
    self.products: Dict[int, Product] = {
        1: Product("Coca-Cola", 15000, 10),
        # ... (các sản phẩm khác)
        15: Product("Mirinda Cam", 15000, 5),
    }
    self.money = 0
```

#### Hàm `nap_tien(money)`

Cho phép người dùng nạp tiền vào máy.

  * **Logic:** Kiểm tra số tiền nạp vào có lớn hơn hoặc bằng 10.000 VND hay không. Nếu hợp lệ, cộng dồn vào `self.money`.

<!-- end list -->

```python
def nap_tien(self, money):
    if money < 10_000:
        print("Cần nạp số tiền lớn hơn hoặc bằng 10.000 VND")
        return self.money

    self.money += money
    print(f"Bạn đã nạp {money} VND vào tài khoản, số tiền hiện tại {self.money} VND")

    return self.money
```

#### Hàm `sell_product(id)`

Hàm quan trọng nhất để thực hiện giao dịch mua hàng.

  * **Logic:**
    1.  Kiểm tra ID sản phẩm có tồn tại không.
    2.  Kiểm tra số dư (`self.money`) có đủ để mua không.
    3.  Kiểm tra sản phẩm còn hàng (`stock`) hay không.
    4.  Nếu tất cả đều thỏa mãn: Trừ tiền từ tài khoản và gọi hàm `product.sell()` để trừ kho.

<!-- end list -->

```python
def sell_product(self, id):
    if not self.has_products(id):
        print(f"Sản phẩm với ID: {id} Không tồn tại")
        return

    product = self.get_product(id)
    # ... (kiểm tra tồn tại)

    if self.money < product.price:
        print("Không đủ tiền để mua sản phẩm này")
        return
    if product.stock < 1:
        print(f"Sản phẩm {product.name} đã hết hàng")
        return

    self.money -= product.price
    product.sell()
```

-----

## 2\. Tệp `main.py` - Giao diện người dùng (UI)

Tệp này chịu trách nhiệm hiển thị bảng sản phẩm và nhận tương tác từ người dùng thông qua thư viện `rich`.

### Vòng lặp chính (`while True`)

Chương trình chạy trong một vòng lặp vô hạn để liên tục phục vụ người dùng cho đến khi tắt.

#### Hiển thị bảng sản phẩm

Sử dụng `rich.table.Table` để tạo bảng. Dữ liệu được lấy từ `vending.get_all_products()` và duyệt qua vòng lặp để thêm từng dòng vào bảng hiển thị.

```python
table = Table(
    title=f"Máy bán hàng tự động - Bạn đang có {vending.money} VND",
    show_lines=True,
)
# ... (Thêm cột)
for id, item in vending.get_all_products().items():
    table.add_row(str(id), item.name, str(item.price), str(item.stock))
console.print(table)
```

#### Xử lý lựa chọn người dùng

Sử dụng `Prompt.ask` để người dùng chọn hành động: `naptien` hoặc `muahang`.

**Trường hợp 1: Nạp tiền**
Yêu cầu người dùng nhập số tiền và gọi hàm `vending.nap_tien()`.

```python
if selection == "naptien":
    tien_nap = IntPrompt.ask("Vui lòng nhập số tiền muốn nạp", console=console)
    vending.nap_tien(int(tien_nap))
```

**Trường hợp 2: Mua hàng**

  * Yêu cầu nhập ID sản phẩm.
  * Kiểm tra tiền: Nếu số dư hiện tại (`vending.get_balance()`) nhỏ hơn giá sản phẩm, hệ thống sẽ yêu cầu nạp thêm tiền ngay lập tức.
  * Cuối cùng gọi `vending.sell_product()` để hoàn tất.

<!-- end list -->

```python
elif selection == "muahang":
    id_mon_hang = IntPrompt.ask("Vui lòng chọn ID sản phẩm theo bảng phía trên", console=console)
    # ... (Kiểm tra tồn tại ID)
    product_price = vending.get_product(int(id_mon_hang)).price
    if vending.get_balance() < product_price:
        tien_nap = IntPrompt.ask("Vui lòng nạp thêm tiền")
        vending.nap_tien(int(tien_nap))
    vending.sell_product(int(id_mon_hang))
```

#### Thời gian chờ

Sau mỗi hành động, chương trình dùng `time.sleep(3)` để dừng màn hình trong 3 giây cho người dùng đọc thông báo trước khi xóa màn hình và vẽ lại bảng.
