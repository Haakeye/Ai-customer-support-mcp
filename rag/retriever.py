def retrieve_context(query):
    query = query.lower()

    if "refund" in query:
        return "Refund Policy: Customers can request a refund within 7 days of delivery."

    if "delivery" in query:
        return "Delivery Time: Orders are delivered within 3-5 business days."

    if "cancel" in query:
        return "Cancellation Policy: Orders can be cancelled before shipping."

    return "General Support: You can raise a support ticket for any issue."