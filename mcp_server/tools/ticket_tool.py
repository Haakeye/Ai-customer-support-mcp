import uuid

tickets = []

def create_ticket(issue, customer_name="Unknown"):
    ticket_id = str(uuid.uuid4())[:8]

    ticket = {
        "ticket_id": ticket_id,
        "issue": issue,
        "customer_name": customer_name,
        "status": "Open"
    }

    tickets.append(ticket)

    return {
        "status": "success",
        "message": f"Ticket created with ID {ticket_id}",
        "ticket": ticket
    }