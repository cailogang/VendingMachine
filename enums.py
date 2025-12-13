# Đây là file định nghĩa các trạng thái để dùng trong chương trình
import enum

class NaptienStatus(enum.Enum):
    INVALID = 0
    SUCCESS = 1
    UNDER_10K = 2

class BuyProductStatus(enum.Enum):
    NOT_ENOUGH_STOCK = 0
    NOT_ENOUGH_MONEY = 1
    NOT_EXISTS = 2
    SUCCESS = 3
    FAILED = 4

class ProductSellStatus(enum.Enum):
    NOT_ENOUGH_STOCK = 0
    SUCCESS = 1
