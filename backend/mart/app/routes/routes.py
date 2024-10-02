from ..controllers.user import UserController
from ..controllers.inventory import InventoryController
from ..controllers.login import auth_router
from ..controllers.order import OrderController
from ..controllers.product import ProductController

user_router = UserController().router
auth_router = auth_router
product_router = ProductController().router
inventory_router = InventoryController().router
order_router = OrderController().router

routes_list = [
    user_router,
    auth_router,
    product_router,
    inventory_router,
    order_router
]