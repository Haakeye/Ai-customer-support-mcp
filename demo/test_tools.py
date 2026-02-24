import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mcp_server.tools.order_tool import get_order_status, cancel_order
from mcp_server.tools.ticket_tool import create_ticket


def run_tests():
    print("---- Testing Order Status ----")
    print(get_order_status("101"))

    print("\n---- Testing Cancel Order ----")
    print(cancel_order("102"))

    print("\n---- Testing Ticket Creation ----")
    print(create_ticket("Payment issue", "Hari"))


if __name__ == "__main__":
    run_tests()