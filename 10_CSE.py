"""
INTEGRATED PYTHON HELPDESK & DATA PROCESSING SUITE
Group 10 | IT Workshop (Python Programming)
Budge Budge Institute of Technology, Kolkata

Run:
    python 10_CSE.py

The program uses only Python's standard library.
It creates helpdesk_tickets.csv and processed_data.csv in the
same folder from which the program is run.
"""

import csv
import os
from datetime import datetime

TICKET_FILE = "helpdesk_tickets.csv"
PROCESSED_FILE = "processed_data.csv"

TICKET_FIELDS = [
    "ticket_id",
    "name",
    "category",
    "priority",
    "description",
    "status",
    "created_at",
]

PROCESSED_FIELDS = [
    "original_text",
    "cleaned_text",
    "character_count",
    "word_count",
    "processed_at",
]

STATUSES = ("Open", "In Progress", "Resolved")
PRIORITIES = ("Low", "Medium", "High")


def read_int(prompt, minimum=None, maximum=None):
    """Read an integer and keep asking until it is within the allowed range."""
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                print(f"Please enter a number greater than or equal to {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Please enter a number less than or equal to {maximum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def read_nonempty(prompt):
    """Read text and reject blank input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be blank. Please try again.")


def load_tickets():
    """Load all ticket records from the CSV file."""
    if not os.path.exists(TICKET_FILE):
        return []

    try:
        with open(TICKET_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except (OSError, csv.Error) as error:
        print(f"Error reading ticket file: {error}")
        return []


def save_tickets(tickets):
    """Save all ticket records to the CSV file."""
    try:
        with open(TICKET_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=TICKET_FIELDS)
            writer.writeheader()
            writer.writerows(tickets)
        return True
    except (OSError, csv.Error) as error:
        print(f"Error saving tickets: {error}")
        return False


def next_ticket_id(tickets):
    """Return the next numeric ticket ID, beginning at 1001."""
    numeric_ids = []
    for ticket in tickets:
        try:
            numeric_ids.append(int(ticket.get("ticket_id", "")))
        except (TypeError, ValueError):
            continue
    return str(max(numeric_ids, default=1000) + 1)


def create_ticket():
    """Collect details, create a ticket and save it."""
    print("\n--- CREATE HELPDESK TICKET ---")
    tickets = load_tickets()

    name = read_nonempty("Enter your name: ")
    category = read_nonempty("Enter issue category (e.g. Network/Software/Login): ")
    print("Priority: 1. Low   2. Medium   3. High")
    priority_number = read_int("Choose priority (1-3): ", 1, 3)
    priority = {1: "Low", 2: "Medium", 3: "High"}[priority_number]
    description = read_nonempty("Describe the issue: ")

    ticket = {
        "ticket_id": next_ticket_id(tickets),
        "name": name,
        "category": category,
        "priority": priority,
        "description": description,
        "status": "Open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    tickets.append(ticket)
    if save_tickets(tickets):
        print("\nTicket created successfully!")
        print(f"Your Ticket ID is: {ticket['ticket_id']}")
        print(f"Status: {ticket['status']}")
    else:
        print("Ticket could not be saved.")


def view_tickets():
    """Display every saved ticket."""
    print("\n--- ALL HELPDESK TICKETS ---")
    tickets = load_tickets()

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print("-" * 60)
        print(f"Ticket ID   : {ticket.get('ticket_id', '')}")
        print(f"Name        : {ticket.get('name', '')}")
        print(f"Category    : {ticket.get('category', '')}")
        print(f"Priority    : {ticket.get('priority', '')}")
        print(f"Description : {ticket.get('description', '')}")
        print(f"Status      : {ticket.get('status', '')}")
        print(f"Created at  : {ticket.get('created_at', '')}")
    print("-" * 60)
    print(f"Total tickets: {len(tickets)}")


def update_ticket_status():
    """Find a ticket by ID and update its status."""
    print("\n--- UPDATE TICKET STATUS ---")
    tickets = load_tickets()

    if not tickets:
        print("No tickets available to update.")
        return

    ticket_id = read_nonempty("Enter Ticket ID: ")
    selected_ticket = None

    for ticket in tickets:
        if ticket.get("ticket_id") == ticket_id:
            selected_ticket = ticket
            break

    if selected_ticket is None:
        print("Ticket ID not found.")
        return

    print("Choose new status:")
    for number, status in enumerate(STATUSES, start=1):
        print(f"{number}. {status}")

    choice = read_int("Enter choice (1-3): ", 1, 3)
    selected_ticket["status"] = STATUSES[choice - 1]

    if save_tickets(tickets):
        print(f"Ticket {ticket_id} status updated to {selected_ticket['status']}.")
    else:
        print("Status update could not be saved.")


def search_tickets():
    """Search ticket fields using a case-insensitive keyword."""
    print("\n--- SEARCH TICKETS ---")
    tickets = load_tickets()

    if not tickets:
        print("No tickets found.")
        return

    keyword = read_nonempty("Enter Ticket ID, name, category or keyword: ").casefold()
    matches = [
        ticket for ticket in tickets
        if any(keyword in str(value).casefold() for value in ticket.values())
    ]

    if not matches:
        print("No matching tickets found.")
        return

    print(f"\nFound {len(matches)} matching ticket(s):")
    for ticket in matches:
        print("-" * 60)
        print(
            f"ID: {ticket.get('ticket_id', '')} | "
            f"Name: {ticket.get('name', '')} | "
            f"Category: {ticket.get('category', '')}"
        )
        print(
            f"Priority: {ticket.get('priority', '')} | "
            f"Status: {ticket.get('status', '')}"
        )
        print(f"Description: {ticket.get('description', '')}")
        print(f"Created at: {ticket.get('created_at', '')}")


def process_text_data():
    """Clean whitespace, count words/characters and save a summary."""
    print("\n--- TEXT DATA PROCESSING ---")
    original_text = read_nonempty("Enter text to clean and analyse: ")

    cleaned_text = " ".join(original_text.split())
    words = cleaned_text.split()
    character_count = len(cleaned_text)
    word_count = len(words)

    record = {
        "original_text": original_text,
        "cleaned_text": cleaned_text,
        "character_count": character_count,
        "word_count": word_count,
        "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    file_exists_and_has_content = (
        os.path.exists(PROCESSED_FILE) and os.path.getsize(PROCESSED_FILE) > 0
    )

    try:
        with open(PROCESSED_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=PROCESSED_FIELDS)
            if not file_exists_and_has_content:
                writer.writeheader()
            writer.writerow(record)

        print("\nText processed successfully!")
        print(f"Cleaned text     : {cleaned_text}")
        print(f"Word count       : {word_count}")
        print(f"Character count  : {character_count}")
        print(f"Saved to         : {PROCESSED_FILE}")
    except (OSError, csv.Error) as error:
        print(f"Error saving processed text: {error}")


def show_report():
    """Display total tickets and counts grouped by status and priority."""
    print("\n--- SUMMARY REPORT ---")
    tickets = load_tickets()

    if not tickets:
        print("No tickets found. Create a ticket to generate a report.")
        return

    print(f"Total tickets: {len(tickets)}")

    print("\nTickets by status:")
    for status in STATUSES:
        count = sum(1 for ticket in tickets if ticket.get("status") == status)
        print(f"  {status:<12}: {count}")

    print("\nTickets by priority:")
    for priority in PRIORITIES:
        count = sum(1 for ticket in tickets if ticket.get("priority") == priority)
        print(f"  {priority:<12}: {count}")


def display_menu():
    """Print the main application menu."""
    print("\n" + "=" * 58)
    print(" INTEGRATED PYTHON HELPDESK & DATA PROCESSING SUITE")
    print("                     GROUP 10")
    print("=" * 58)
    print("1. Create helpdesk ticket")
    print("2. View all tickets")
    print("3. Update ticket status")
    print("4. Search tickets")
    print("5. Process text data")
    print("6. Summary report")
    print("0. Exit")
    print("-" * 58)


def main():
    """Run the menu until the user chooses Exit."""
    actions = {
        1: create_ticket,
        2: view_tickets,
        3: update_ticket_status,
        4: search_tickets,
        5: process_text_data,
        6: show_report,
    }

    while True:
        display_menu()
        choice = read_int("Enter your choice (0-6): ", 0, 6)

        if choice == 0:
            print("\nThank you for using the Integrated Python Helpdesk!")
            print("Goodbye.")
            break

        actions[choice]()
        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    main()
