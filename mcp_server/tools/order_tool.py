import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../database/orders.json")


def load_orders():
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_orders(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)


def get_order_status(order_id):
    order_id = str(order_id)
    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id:
            return {
                "status": "success",
                "message": f"Order {order_id} is {order['status']}"
            }

    return {
        "status": "error",
        "message": "Order not found"
    }


def cancel_order(order_id):
    order_id = str(order_id)
    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "Cancelled"
            save_orders(orders)

            return {
                "status": "success",
                "message": f"Order {order_id} has been cancelled"
            }

    return {
        "status": "error",
        "message": "Order not found"
    }