
from book_manager import (
    load_books,
    save_books,
    display_books,
    add_book,
    delete_book,
    search_books,
    borrow_book,
    return_book
)


def main():
    books = load_books()

    while True:
        print("\n===== SMART LIBRARY & BOOK RECOMMENDATION SYSTEM =====")
        print("1. View All Books")
        print("2. Add a Book")
        print("3. Search Books")
        print("4. Delete a Book")
        print("5. Borrow a Book")
        print("6. Return a Book")
        print("7. Save and Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_books(books)
        elif choice == "2":
            add_book(books)
        elif choice == "3":
            search_books(books)
        elif choice == "4":
            delete_book(books)
        elif choice == "5":
            borrow_book(books)
        elif choice == "6":
            return_book(books)
        elif choice == "7":
            save_books(books)
            print("Data saved successfully. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
