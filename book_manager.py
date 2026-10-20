
import json

FILE_NAME = "books.json"


def load_books():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_books(books):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4)


def display_books(books):
    if not books:
        print("\nNo books found.")
        return

    print("\n" + "-" * 100)
    print(f"{'ID':<8}{'TITLE':<28}{'AUTHOR':<28}{'CATEGORY':<22}{'YEAR':<8}{'STATUS'}")
    print("-" * 100)

    for book in books:
        status = "Available" if book["available"] else "Borrowed"
        print(
            f"{book['id']:<8}{book['title']:<28}"
            f"{book['author']:<28}{book['category']:<22}"
            f"{book['year']:<8}{status}"
        )

    print("-" * 100)


def add_book(books):
    try:
        book_id = int(input("Enter book ID: "))

        if any(book["id"] == book_id for book in books):
            print("This book ID already exists.")
            return

        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()
        category = input("Enter category: ").strip()
        year = int(input("Enter publication year: "))

        if not title or not author or not category:
            print("Title, author, and category cannot be empty.")
            return

        books.append({
            "id": book_id,
            "title": title,
            "author": author,
            "category": category,
            "year": year,
            "available": True
        })

        save_books(books)
        print("Book added successfully.")

    except ValueError:
        print("Please enter valid numeric values for ID and year.")


def delete_book(books):
    try:
        book_id = int(input("Enter the ID of the book to delete: "))

        for book in books:
            if book["id"] == book_id:
                books.remove(book)
                save_books(books)
                print("Book deleted successfully.")
                return

        print("Book ID not found.")

    except ValueError:
        print("Please enter a valid book ID.")


def search_books(books):
    print("\n1. Search by title")
    print("2. Search by author")
    print("3. Search by category")
    print("4. Search by ID")

    choice = input("Choose search method: ").strip()

    if choice == "1":
        query = input("Enter title: ").strip().lower()
        results = [b for b in books if query in b["title"].lower()]

    elif choice == "2":
        query = input("Enter author: ").strip().lower()
        results = [b for b in books if query in b["author"].lower()]

    elif choice == "3":
        query = input("Enter category: ").strip().lower()
        results = [b for b in books if query in b["category"].lower()]

    elif choice == "4":
        try:
            book_id = int(input("Enter book ID: "))
            results = [b for b in books if b["id"] == book_id]
        except ValueError:
            print("Please enter a valid book ID.")
            return

    else:
        print("Invalid search choice.")
        return

    display_books(results)


def borrow_book(books):
    try:
        book_id = int(input("Enter book ID to borrow: "))

        for book in books:
            if book["id"] == book_id:
                if book["available"]:
                    book["available"] = False
                    save_books(books)
                    print("Book borrowed successfully.")
                else:
                    print("This book is already borrowed.")
                return

        print("Book ID not found.")

    except ValueError:
        print("Please enter a valid book ID.")


def return_book(books):
    try:
        book_id = int(input("Enter book ID to return: "))

        for book in books:
            if book["id"] == book_id:
                if not book["available"]:
                    book["available"] = True
                    save_books(books)
                    print("Book returned successfully.")
                else:
                    print("This book is already available.")
                return

        print("Book ID not found.")

    except ValueError:
        print("Please enter a valid book ID.")
