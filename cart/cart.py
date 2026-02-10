from decimal import Decimal
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    # -------------------------------------------------
    # ADD ITEM
    # -------------------------------------------------
    def add(self, product, quantity=1, override_quantity=False, size=None, color=None):
        """
        key format:
        productId_size_color
        Examples:
        5_M_Red
        3_None_None
        """

        size = size or "None"
        color = color or "None"

        key = f"{product.id}_{size}_{color}"

        if key not in self.cart:
            self.cart[key] = {
                "product_id": product.id,
                "quantity": 0,
                "price": str(product.price),
                "size": None if size == "None" else size,
                "color": None if color == "None" else color,
            }

        if override_quantity:
            self.cart[key]["quantity"] = quantity
        else:
            self.cart[key]["quantity"] += quantity

        if self.cart[key]["quantity"] <= 0:
            self.remove(key)
        else:
            self.save()

    # -------------------------------------------------
    # SAVE SESSION
    # -------------------------------------------------
    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    # -------------------------------------------------
    # REMOVE ITEM
    # -------------------------------------------------
    def remove(self, key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    # -------------------------------------------------
    # ITERATE CART
    # -------------------------------------------------
    def __iter__(self):
        cart_copy = self.cart.copy()

        product_ids = [item["product_id"] for item in cart_copy.values()]
        products = Product.objects.filter(id__in=product_ids)

        product_map = {product.id: product for product in products}

        for key, item in cart_copy.items():
            product = product_map.get(item["product_id"])

            if not product:
                continue

            # Create a shallow copy of the item to yield
            item_to_yield = item.copy()
            item_to_yield["product"] = product
            item_to_yield["total_price"] = Decimal(item["price"]) * item["quantity"]
            item_to_yield["key"] = key

            yield item_to_yield

    # -------------------------------------------------
    # TOTAL QUANTITY
    # -------------------------------------------------
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    # -------------------------------------------------
    # TOTAL PRICE
    # -------------------------------------------------
    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    # -------------------------------------------------
    # CLEAR CART
    # -------------------------------------------------
    def clear(self):
        self.cart = {}
        self.session["cart"] = {}
        self.save()
