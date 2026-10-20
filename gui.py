import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.linked_list import LinkedList
from algorithms.hashing import HashTable
from algorithms.searching_sorting import merge_sort
from algorithms.trie import Trie
from algorithms.trees import BinarySearchTree
from algorithms.stack_queue import Stack, Queue
from algorithms.graphs import Graph


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOKS_FILE = os.path.join(BASE_DIR, "books.json")

BG = "#FAF7F0"
WHITE = "#FFFFFF"
PEACH = "#F3D4C5"
SAGE = "#C8D8C0"
BLUE = "#C9D8E8"
LAVENDER = "#E9D5E8"
DARK = "#34423A"
MUTED = "#718078"
BORDER = "#E5E3DB"


def load_books():
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as file:
            books = json.load(file)

            if not isinstance(books, list):
                raise ValueError("books.json must contain a list of books.")

            return books

    except (OSError, json.JSONDecodeError, ValueError) as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load books.json.\n\n{error}"
        )
        return []


def save_books(books):
    try:
        with open(BOOKS_FILE, "w", encoding="utf-8") as file:
            json.dump(books, file, indent=2, ensure_ascii=False)

        return True

    except OSError as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save the book database.\n\n{error}"
        )
        return False


class SmartLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Library & Book Recommendation System")
        self.root.geometry("1180x740")
        self.root.minsize(950, 620)
        self.root.configure(bg=BG)

        self.books = load_books()

        # Backward-compatible quantity fields for books saved by older versions.
        # Existing records keep working without requiring manual edits to books.json.
        for book in self.books:
            quantity = max(1, int(book.get("quantity", 1)))
            book["quantity"] = quantity
            if "available_copies" in book:
                book["available_copies"] = max(
                    0, min(quantity, int(book["available_copies"]))
                )
            else:
                book["available_copies"] = quantity if book.get("available", True) else 0
            book["available"] = book["available_copies"] > 0

        self.book_index = HashTable(
            size=max(10, len(self.books) * 2)
        )
        self.rebuild_book_index()

        self.title_trie = Trie()
        self.title_lookup = {}
        self.rebuild_title_trie()

        self.activities = LinkedList()

        # Queue: processes the oldest pending request first (FIFO).
        self.request_queue = Queue()

        # Stack: tracks pending requests for last-added cancellation (LIFO).
        self.request_stack = Stack()

        self.current_page = "Dashboard"

        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All Categories")
        self.status_var = tk.StringVar(value="All Books")

        self.setup_styles()
        self.build_layout()
        self.show_page("Dashboard")

    def rebuild_book_index(self):
        self.book_index = HashTable(
            size=max(10, len(self.books) * 2)
        )

        for book in self.books:
            book_id = book.get("id")

            if book_id is not None:
                self.book_index.insert(str(book_id), book)

    def rebuild_title_trie(self):
        self.title_trie = Trie()
        self.title_lookup = {}

        for book in self.books:
            title = str(book.get("title", "")).strip()

            if title:
                normalized_title = title.lower()

                if normalized_title not in self.title_lookup:
                    self.title_lookup[normalized_title] = title
                    self.title_trie.insert(normalized_title)

    def get_titles_using_bst(self):
        title_tree = BinarySearchTree()

        for book in self.books:
            title = str(book.get("title", "")).strip()

            if title:
                title_tree.insert(title.lower())

        sorted_titles = title_tree.inorder()

        return [
            self.title_lookup.get(title, title)
            for title in sorted_titles
        ]

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=DARK,
            fieldbackground=WHITE,
            rowheight=34,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background=BLUE,
            foreground=DARK,
            font=("Segoe UI", 10, "bold"),
            padding=10,
            borderwidth=0
        )

        style.map(
            "Treeview",
            background=[("selected", SAGE)],
            foreground=[("selected", DARK)]
        )

        style.configure(
            "TCombobox",
            padding=6,
            font=("Segoe UI", 10)
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=WHITE, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="BOOKNEST",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w", padx=22, pady=(28, 2))

        tk.Label(
            self.sidebar,
            text="SMART LIBRARY SYSTEM",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=23, pady=(0, 30))

        navigation = [
            ("Dashboard", "▦", PEACH),
            ("Book Management", "▤", SAGE),
            ("Recommendations", "✧", BLUE),
            ("Activity & Requests", "◷", LAVENDER),
        ]

        self.nav_buttons = {}

        for name, symbol, color in navigation:
            button = tk.Button(
                self.sidebar,
                text=f"  {symbol}   {name}",
                command=lambda page=name: self.show_page(page),
                anchor="w",
                bg=WHITE,
                fg=DARK,
                activebackground=color,
                activeforeground=DARK,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 10),
                padx=15,
                pady=13
            )

            button.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = button

        tk.Frame(
            self.sidebar,
            bg=BORDER,
            height=1
        ).pack(fill="x", padx=20, pady=(25, 12))

        tk.Label(
            self.sidebar,
            text="DSA PROJECT",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=23)

        tk.Label(
            self.sidebar,
            text="Data Structures & Algorithms\nCollege Project",
            bg=WHITE,
            fg=MUTED,
            justify="left",
            font=("Segoe UI", 9),
            pady=7
        ).pack(anchor="w", padx=23)

        self.main_area = tk.Frame(self.root, bg=BG)
        self.main_area.pack(side="left", fill="both", expand=True)

    def clear_page(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def page_header(self, title, subtitle):
        header = tk.Frame(self.main_area, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 18))

        tk.Label(
            header,
            text=title,
            bg=BG,
            fg=DARK,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text=subtitle,
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 0))

    def make_card(self, parent, title, value, color):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(side="left", fill="both", expand=True, padx=6)

        tk.Frame(card, bg=color, height=5).pack(fill="x")

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=16, pady=(15, 5))

        value_label = tk.Label(
            card,
            text=str(value),
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 23, "bold")
        )

        value_label.pack(anchor="w", padx=16, pady=(0, 15))
        return value_label

    def show_page(self, page):
        self.current_page = page
        self.clear_page()

        for name, button in self.nav_buttons.items():
            button.configure(
                bg=BLUE if name == page else WHITE,
                font=("Segoe UI", 10, "bold") if name == page
                else ("Segoe UI", 10)
            )

        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Book Management":
            self.show_books()
        elif page == "Recommendations":
            self.show_recommendations()
        elif page == "Activity & Requests":
            self.show_activity()

    def show_dashboard(self):
        self.page_header(
            "Dashboard",
            "A simple overview of your library."
        )

        total = sum(int(book.get("quantity", 1)) for book in self.books)

        available = sum(
            int(book.get("available_copies", book.get("quantity", 1)))
            for book in self.books
        )

        borrowed = total - available

        categories = len({
            str(book.get("category", "")).strip()
            for book in self.books
            if book.get("category")
        })

        cards = tk.Frame(self.main_area, bg=BG)
        cards.pack(fill="x", padx=24, pady=8)

        self.make_card(cards, "Total Copies", total, PEACH)
        self.make_card(cards, "Available Copies", available, SAGE)
        self.make_card(cards, "Borrowed Copies", borrowed, BLUE)
        self.make_card(cards, "Categories", categories, LAVENDER)

        panel = tk.Frame(
            self.main_area,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(fill="both", expand=True, padx=30, pady=22)

        tk.Label(
            panel,
            text="Welcome to BookNest",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=22, pady=(22, 7))

        tk.Label(
            panel,
            text=(
                "Manage your book collection, find books quickly, "
                "and discover your next read.\n\n"
                "Use the navigation menu to manage books, explore "
                "recommendations, or review your recent activity."
            ),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 11),
            justify="left",
            wraplength=650
        ).pack(anchor="w", padx=22, pady=(0, 20))

        tk.Button(
            panel,
            text="Open Book Management",
            command=lambda: self.show_page("Book Management"),
            bg=SAGE,
            fg=DARK,
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=22, pady=(0, 22))

    def show_books(self):
        self.page_header(
            "Book Management",
            "Search, filter, add, remove, borrow, and return books."
        )

        toolbar = tk.Frame(self.main_area, bg=BG)
        toolbar.pack(fill="x", padx=30, pady=(0, 4))

        search = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=DARK,
            relief="solid",
            bd=1
        )

        search.pack(side="left", fill="x", expand=True, ipady=9)
        search.bind("<KeyRelease>", self.update_search_suggestions)
        search.bind("<Down>", self.focus_suggestion)
        search.bind("<Escape>", self.hide_suggestions)

        categories = sorted({
            str(book.get("category", "")).strip()
            for book in self.books
            if book.get("category")
        })

        category_box = ttk.Combobox(
            toolbar,
            textvariable=self.category_var,
            values=["All Categories"] + categories,
            state="readonly",
            width=19
        )

        category_box.pack(side="left", padx=(10, 0))
        category_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        status_box = ttk.Combobox(
            toolbar,
            textvariable=self.status_var,
            values=["All Books", "Available", "Borrowed"],
            state="readonly",
            width=12
        )

        status_box.pack(side="left", padx=(10, 0))
        status_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        self.suggestion_frame = tk.Frame(
            self.main_area,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.suggestion_list = tk.Listbox(
            self.suggestion_frame,
            height=4,
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=DARK,
            selectbackground=SAGE,
            selectforeground=DARK,
            relief="flat",
            bd=0,
            activestyle="none"
        )

        self.suggestion_list.pack(fill="both", expand=True, padx=4, pady=4)

        self.suggestion_list.bind(
            "<<ListboxSelect>>",
            self.select_search_suggestion
        )

        self.suggestion_list.bind(
            "<Return>",
            self.select_search_suggestion
        )

        table_frame = tk.Frame(self.main_area, bg=WHITE)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(8, 12)
        )

        columns = (
            "id", "title", "author",
            "category", "year", "quantity", "status"
        )

        self.book_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": ("Book ID", 70),
            "title": ("Title", 240),
            "author": ("Author", 170),
            "category": ("Category", 125),
            "year": ("Year", 65),
            "quantity": ("Copies (Available/Total)", 145),
            "status": ("Availability", 100)
        }

        for column, (heading, width) in headings.items():
            self.book_tree.heading(
                column,
                text=heading,
                command=lambda col=column: self.sort_table(col)
            )

            self.book_tree.column(
                column,
                width=width,
                anchor="w"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.book_tree.yview
        )

        self.book_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.book_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = tk.Frame(self.main_area, bg=BG)
        actions.pack(fill="x", padx=30, pady=(0, 24))

        buttons = [
            ("+ Add Book", self.add_book, SAGE),
            ("Delete Selected", self.delete_book, PEACH),
            ("Borrow Selected", self.borrow_book, BLUE),
            ("Return Selected", self.return_book, LAVENDER)
        ]

        for text, command, color in buttons:
            tk.Button(
                actions,
                text=text,
                command=command,
                bg=color,
                fg=DARK,
                relief="flat",
                padx=12,
                pady=10,
                cursor="hand2",
                font=("Segoe UI", 9, "bold")
            ).pack(side="left", padx=(0, 8))

        self.refresh_table()

    def update_search_suggestions(self, event=None):
        self.refresh_table()

        if not hasattr(self, "suggestion_list"):
            return

        if event is not None and event.keysym in (
            "Up", "Down", "Left", "Right",
            "Return", "Escape", "Tab"
        ):
            return

        term = self.search_var.get().strip().lower()

        self.suggestion_list.delete(0, tk.END)

        if len(term) < 2:
            self.hide_suggestions()
            return

        try:
            matches = self.title_trie.autocomplete(term)
        except (AttributeError, TypeError):
            self.hide_suggestions()
            return

        for match in matches[:6]:
            original_title = self.title_lookup.get(
                str(match).lower(),
                str(match)
            )
            self.suggestion_list.insert(tk.END, original_title)

        if self.suggestion_list.size() > 0:
            self.suggestion_frame.pack(
                fill="x",
                padx=30,
                pady=(0, 4),
                before=self.book_tree.master
            )
        else:
            self.hide_suggestions()

    def focus_suggestion(self, event=None):
        if (
            hasattr(self, "suggestion_list")
            and self.suggestion_list.size() > 0
        ):
            self.suggestion_list.focus_set()
            self.suggestion_list.selection_clear(0, tk.END)
            self.suggestion_list.selection_set(0)
            self.suggestion_list.activate(0)

        return "break"

    def select_search_suggestion(self, event=None):
        if not hasattr(self, "suggestion_list"):
            return

        selection = self.suggestion_list.curselection()

        if not selection:
            return

        title = self.suggestion_list.get(selection[0])
        self.search_var.set(title)

        self.hide_suggestions()
        self.refresh_table()

    def hide_suggestions(self, event=None):
        if hasattr(self, "suggestion_frame"):
            self.suggestion_frame.pack_forget()

        return "break" if event is not None else None

    def filtered_books(self):
        term = self.search_var.get().strip().lower()
        category = self.category_var.get()
        status = self.status_var.get()

        results = []

        for book in self.books:
            searchable = " ".join(
                str(book.get(field, ""))
                for field in (
                    "id", "title", "author", "category", "year"
                )
            ).lower()

            if term and term not in searchable:
                continue

            if category != "All Categories":
                if book.get("category", "") != category:
                    continue

            available_copies = int(
                book.get("available_copies", book.get("quantity", 1))
            )
            total_copies = int(book.get("quantity", 1))

            if status == "Available" and available_copies <= 0:
                continue

            if status == "Borrowed" and available_copies >= total_copies:
                continue

            results.append(book)

        return results

    def refresh_table(self):
        if not hasattr(self, "book_tree"):
            return

        for item in self.book_tree.get_children():
            self.book_tree.delete(item)

        for book in self.filtered_books():
            available_copies = int(
                book.get("available_copies", book.get("quantity", 1))
            )
            total_copies = int(book.get("quantity", 1))
            status = "Available" if available_copies > 0 else "Out of Stock"

            self.book_tree.insert(
                "",
                "end",
                values=(
                    book.get("id", ""),
                    book.get("title", ""),
                    book.get("author", ""),
                    book.get("category", ""),
                    book.get("year", ""),
                    f"{available_copies}/{total_copies}",
                    status
                )
            )

    def selected_book(self):
        selection = self.book_tree.selection()

        if not selection:
            messagebox.showwarning(
                "Select a Book",
                "Please select a book from the table first."
            )
            return None

        book_id = str(
            self.book_tree.item(
                selection[0],
                "values"
            )[0]
        )

        book = self.book_index.search(book_id)

        if book is None:
            messagebox.showerror(
                "Book Not Found",
                "The selected book could not be found."
            )
            return None

        return book

    def add_book(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add a Book")
        dialog.geometry("420x530")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Add New Book",
            bg=BG,
            fg=DARK,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=25, pady=(22, 15))

        fields = {}

        for label in (
            "Book ID", "Title", "Author", "Category", "Year", "Quantity"
        ):
            tk.Label(
                dialog,
                text=label,
                bg=BG,
                fg=DARK,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", padx=25, pady=(6, 2))

            entry = tk.Entry(
                dialog,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )

            entry.pack(fill="x", padx=25, ipady=6)
            fields[label] = entry

        def save_new_book():
            try:
                book_id = int(fields["Book ID"].get().strip())
                year = int(fields["Year"].get().strip())
                quantity = int(fields["Quantity"].get().strip())
                title = fields["Title"].get().strip()
                author = fields["Author"].get().strip()
                category = fields["Category"].get().strip()

                if not title or not author or not category:
                    raise ValueError(
                        "Please fill in every field."
                    )

                if any(
                    str(book.get("id")) == str(book_id)
                    for book in self.books
                ):
                    raise ValueError(
                        "This book ID already exists."
                    )

                if any(
                    str(book.get("title", "")).strip().lower()
                    == title.lower()
                    for book in self.books
                ):
                    raise ValueError(
                        "This book title already exists."
                    )

                if year < 0 or year > 2100:
                    raise ValueError(
                        "Please enter a valid year."
                    )

                if quantity < 1 or quantity > 10000:
                    raise ValueError(
                        "Quantity must be a whole number between 1 and 10000."
                    )

            except ValueError as error:
                messagebox.showerror(
                    "Invalid Input",
                    str(error),
                    parent=dialog
                )
                return

            new_book = {
                "id": book_id,
                "title": title,
                "author": author,
                "category": category,
                "year": year,
                "quantity": quantity,
                "available_copies": quantity,
                "available": True
            }

            self.books.append(new_book)

            if save_books(self.books):
                self.rebuild_book_index()
                self.rebuild_title_trie()

                self.log_activity(
                    f"Added book: {title} (ID {book_id})"
                )

                dialog.destroy()
                self.show_page("Book Management")

            else:
                self.books.pop()

        tk.Button(
            dialog,
            text="Save Book",
            command=save_new_book,
            bg=SAGE,
            fg=DARK,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=9,
            cursor="hand2"
        ).pack(anchor="w", padx=25, pady=20)

    def delete_book(self):
        book = self.selected_book()

        if book is None:
            return

        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Delete '{book.get('title', '')}'?\n\n"
            "This action cannot be undone from this screen."
        ):
            return

        original_index = self.books.index(book)
        removed = self.books.pop(original_index)

        if save_books(self.books):
            self.rebuild_book_index()
            self.rebuild_title_trie()

            self.log_activity(
                f"Deleted book: {removed.get('title')} "
                f"(ID {removed.get('id')})"
            )

            self.show_page("Book Management")

        else:
            self.books.insert(original_index, removed)

    def borrow_book(self):
        book = self.selected_book()

        if book is None:
            return

        quantity = int(book.get("quantity", 1))
        available_copies = int(
            book.get("available_copies", quantity if book.get("available", True) else 0)
        )

        if available_copies <= 0:
            messagebox.showinfo(
                "No Copies Available",
                "All copies of this book are currently borrowed."
            )
            return

        book["available_copies"] = available_copies - 1
        book["available"] = book["available_copies"] > 0

        if save_books(self.books):
            self.log_activity(
                f"Borrowed 1 copy: {book.get('title')} "
                f"(ID {book.get('id')}); "
                f"{book['available_copies']}/{quantity} copies remain"
            )
            self.show_page("Book Management")
        else:
            book["available_copies"] = available_copies
            book["available"] = available_copies > 0

    def return_book(self):
        book = self.selected_book()

        if book is None:
            return

        quantity = int(book.get("quantity", 1))
        available_copies = int(
            book.get("available_copies", quantity if book.get("available", True) else 0)
        )

        if available_copies >= quantity:
            messagebox.showinfo(
                "All Copies Available",
                "No borrowed copies of this book need to be returned."
            )
            return

        book["available_copies"] = available_copies + 1
        book["available"] = True

        if save_books(self.books):
            self.log_activity(
                f"Returned 1 copy: {book.get('title')} "
                f"(ID {book.get('id')}); "
                f"{book['available_copies']}/{quantity} copies available"
            )
            self.show_page("Book Management")
        else:
            book["available_copies"] = available_copies
            book["available"] = available_copies > 0

    def sort_table(self, column):
        if not hasattr(self, "book_tree"):
            return

        rows = [
            (self.book_tree.set(item, column), item)
            for item in self.book_tree.get_children("")
        ]

        def sort_key(row):
            value = row[0]

            try:
                return (0, float(value))
            except (ValueError, TypeError):
                return (1, str(value).lower())

        sortable_rows = [
            (sort_key(value), item)
            for value, item in rows
        ]

        sorted_rows = merge_sort(sortable_rows)

        for index, (_, item) in enumerate(sorted_rows):
            self.book_tree.move(item, "", index)

    # ---------------- GRAPH: BFS AND DFS RECOMMENDATIONS ----------------

    def build_book_graph(self):
        graph = Graph()
        book_lookup = {}
        valid_books = []

        for book in self.books:
            title = str(book.get("title", "")).strip()

            if not title:
                continue

            graph.add_vertex(title)
            book_lookup[title] = book
            valid_books.append(book)

        for index, first in enumerate(valid_books):
            first_title = str(first.get("title", "")).strip()
            first_category = str(
                first.get("category", "")
            ).strip().casefold()
            first_author = str(
                first.get("author", "")
            ).strip().casefold()

            for second in valid_books[index + 1:]:
                second_title = str(
                    second.get("title", "")
                ).strip()
                second_category = str(
                    second.get("category", "")
                ).strip().casefold()
                second_author = str(
                    second.get("author", "")
                ).strip().casefold()

                same_category = (
                    bool(first_category)
                    and first_category == second_category
                )

                same_author = (
                    bool(first_author)
                    and first_author == second_author
                )

                if same_category or same_author:
                    graph.add_edge(first_title, second_title)

        return graph, book_lookup

    def show_recommendations(self):
        self.page_header(
            "Recommendations",
            "Discover related books using graph traversal."
        )

        panel = tk.Frame(
            self.main_area,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        tk.Label(
            panel,
            text="Choose a book",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=20, pady=(18, 7))

        titles = self.get_titles_using_bst()
        chosen_title = tk.StringVar()

        title_box = ttk.Combobox(
            panel,
            textvariable=chosen_title,
            values=titles,
            state="readonly",
            width=50
        )

        title_box.pack(anchor="w", padx=20, ipady=5)

        tk.Label(
            panel,
            text=(
                "Book titles are organized alphabetically "
                "using BST inorder traversal."
            ),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20, pady=(5, 10))

        controls = tk.Frame(panel, bg=WHITE)
        controls.pack(fill="x", padx=20, pady=(0, 8))

        tk.Label(
            controls,
            text="Exploration method",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(0, 10))

        algorithm_var = tk.StringVar(value="BFS")

        algorithm_box = ttk.Combobox(
            controls,
            textvariable=algorithm_var,
            values=["BFS", "DFS"],
            state="readonly",
            width=12
        )

        algorithm_box.pack(side="left", ipady=3)

        tk.Label(
            panel,
            text=(
                "BFS explores connected books level by level. "
                "DFS explores one path before trying another.\n"
                "Books are connected when they share a category "
                "or author."
            ),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
            justify="left",
            wraplength=760
        ).pack(anchor="w", padx=20, pady=(2, 8))

        result_frame = tk.Frame(panel, bg=WHITE)
        result_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(5, 8)
        )

        def recommend():
            for widget in result_frame.winfo_children():
                widget.destroy()

            selected_title = chosen_title.get().strip()

            if not selected_title:
                messagebox.showwarning(
                    "Choose a Book",
                    "Please select a book first."
                )
                return

            graph, book_lookup = self.build_book_graph()

            if selected_title not in book_lookup:
                messagebox.showwarning(
                    "Book Not Found",
                    "The selected book could not be found."
                )
                return

            selected = book_lookup[selected_title]
            method = algorithm_var.get()

            if method == "DFS":
                traversal = graph.dfs(selected_title)
                explanation = (
                    "Depth-First Search: follows one connection "
                    "as far as possible before backtracking."
                )
            else:
                traversal = graph.bfs(selected_title)
                explanation = (
                    "Breadth-First Search: explores immediate "
                    "connections before moving to further levels."
                )

            related_titles = [
                title for title in traversal
                if title != selected_title
            ]

            related = [
                book_lookup[title]
                for title in related_titles
                if title in book_lookup
            ]

            self.log_activity(
                f"Viewed {method} recommendations for: "
                f"{selected_title}"
            )

            tk.Label(
                result_frame,
                text=f"Because you selected {selected_title}",
                bg=WHITE,
                fg=DARK,
                font=("Segoe UI", 12, "bold")
            ).pack(anchor="w", pady=(0, 5))

            tk.Label(
                result_frame,
                text=(
                    f"Category: {selected.get('category', 'Unknown')}   "
                    f"|   Author: {selected.get('author', 'Unknown')}"
                ),
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(0, 5))

            tk.Label(
                result_frame,
                text=f"Traversal: {method}",
                bg=BLUE,
                fg=DARK,
                font=("Segoe UI", 10, "bold"),
                padx=8,
                pady=4
            ).pack(anchor="w", pady=(2, 5))

            tk.Label(
                result_frame,
                text=explanation,
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9),
                wraplength=760,
                justify="left"
            ).pack(anchor="w", pady=(0, 8))

            if not related:
                tk.Label(
                    result_frame,
                    text=(
                        "No related books found. Add more books "
                        "with the same category or author to create "
                        "connections in the graph."
                    ),
                    bg=WHITE,
                    fg=MUTED,
                    font=("Segoe UI", 10),
                    wraplength=760,
                    justify="left"
                ).pack(anchor="w", pady=5)
                return

            tk.Label(
                result_frame,
                text=(
                    f"Related books found: {len(related)}"
                ),
                bg=WHITE,
                fg=DARK,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(0, 5))

            results_canvas = tk.Canvas(
                result_frame,
                bg=WHITE,
                highlightthickness=0,
                height=190
            )

            results_scrollbar = ttk.Scrollbar(
                result_frame,
                orient="vertical",
                command=results_canvas.yview
            )

            results_canvas.configure(
                yscrollcommand=results_scrollbar.set
            )

            results_scrollbar.pack(side="right", fill="y")
            results_canvas.pack(
                side="left",
                fill="both",
                expand=True
            )

            results_content = tk.Frame(
                results_canvas,
                bg=WHITE
            )

            results_window = results_canvas.create_window(
                (0, 0),
                window=results_content,
                anchor="nw"
            )

            def update_results_scroll(event=None):
                results_canvas.configure(
                    scrollregion=results_canvas.bbox("all")
                )

            def resize_results_content(event):
                results_canvas.itemconfigure(
                    results_window,
                    width=event.width
                )

            results_content.bind(
                "<Configure>",
                update_results_scroll
            )

            results_canvas.bind(
                "<Configure>",
                resize_results_content
            )

            for index, book in enumerate(related, start=1):
                available_copies = int(
                    book.get("available_copies", book.get("quantity", 1))
                )
                total_copies = int(book.get("quantity", 1))
                status = f"{available_copies}/{total_copies} copies available"

                card = tk.Frame(
                    results_content,
                    bg="#FCFBF8",
                    highlightbackground=BORDER,
                    highlightthickness=1
                )

                card.pack(
                    fill="x",
                    pady=3,
                    padx=(0, 5)
                )

                tk.Label(
                    card,
                    text=f"{index}.  {book.get('title', 'Untitled')}",
                    bg="#FCFBF8",
                    fg=DARK,
                    font=("Segoe UI", 10, "bold"),
                    anchor="w",
                    wraplength=650,
                    justify="left"
                ).pack(
                    anchor="w",
                    fill="x",
                    padx=10,
                    pady=(6, 2)
                )

                tk.Label(
                    card,
                    text=(
                        f"{book.get('author', 'Unknown author')}  "
                        f"•  {book.get('category', 'Uncategorized')}  "
                        f"•  {status}"
                    ),
                    bg="#FCFBF8",
                    fg=MUTED,
                    font=("Segoe UI", 9),
                    anchor="w",
                    wraplength=650,
                    justify="left"
                ).pack(
                    anchor="w",
                    fill="x",
                    padx=10,
                    pady=(0, 6)
                )

        tk.Button(
            panel,
            text="Explore Related Books",
            command=recommend,
            bg=BLUE,
            fg=DARK,
            relief="flat",
            padx=14,
            pady=9,
            cursor="hand2",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 12))

    def log_activity(self, text):
        self.activities.add_front(text)

    # ---------------- QUEUE AND STACK: BOOK REQUESTS ----------------

    def refresh_request_queue(self):
        if not hasattr(self, "request_listbox"):
            return

        self.request_listbox.delete(0, tk.END)

        for position, request in enumerate(
            self.request_queue.items,
            start=1
        ):
            self.request_listbox.insert(
                tk.END,
                f"{position}.  {request['title']}"
            )

        if self.request_queue.is_empty():
            self.request_listbox.insert(
                tk.END,
                "No pending book requests."
            )

        self.refresh_stack_status()

    def refresh_stack_status(self):
        if not hasattr(self, "stack_status_label"):
            return

        if self.request_stack.is_empty():
            status = "Stack is empty — no pending requests to cancel."
        else:
            newest_request = self.request_stack.peek()
            status = (
                f"Stack top (latest request): "
                f"{newest_request['title']}  |  "
                f"Pending requests tracked: "
                f"{len(self.request_stack.items)}"
            )

        self.stack_status_label.configure(text=status)

    def add_book_request(self):
        title = self.request_title_var.get().strip()

        if not title:
            messagebox.showwarning(
                "Select a Book",
                "Please select a book before adding a request."
            )
            return

        for request in self.request_queue.items:
            if request["title"].lower() == title.lower():
                messagebox.showinfo(
                    "Request Already Exists",
                    "This book is already in the request queue."
                )
                return

        book = next(
            (
                item for item in self.books
                if str(item.get("title", "")).strip() == title
            ),
            None
        )

        if book is None:
            messagebox.showerror(
                "Book Not Found",
                "The selected book could not be found."
            )
            return

        request = {
            "id": book.get("id"),
            "title": title
        }

        # Queue: add to the rear for FIFO processing.
        self.request_queue.enqueue(request)

        # Stack: push the same request for LIFO cancellation.
        self.request_stack.push(request)

        self.log_activity(f"Added book request: {title}")

        self.request_title_var.set("")
        self.show_page("Activity & Requests")

    def process_next_request(self):
        if self.request_queue.is_empty():
            messagebox.showinfo(
                "Queue Is Empty",
                "There are no pending book requests to process."
            )
            return

        # Queue removes the oldest request first.
        request = self.request_queue.dequeue()

        # Remove the processed request from the Stack too.
        self.request_stack.items = [
            item for item in self.request_stack.items
            if not (
                str(item.get("id")) == str(request.get("id"))
                and item.get("title", "").lower()
                == request.get("title", "").lower()
            )
        ]

        self.log_activity(
            f"Processed book request: {request['title']}"
        )

        messagebox.showinfo(
            "Request Processed",
            f"The following request was processed:\n\n"
            f"{request['title']}\n\n"
            "It was the oldest request in the queue (FIFO)."
        )

        self.show_page("Activity & Requests")

    def cancel_last_added_request(self):
        if self.request_stack.is_empty():
            messagebox.showinfo(
                "Stack Is Empty",
                "There are no pending requests to cancel."
            )
            return

        latest_request = self.request_stack.peek()

        queue_index = next(
            (
                index
                for index, request in enumerate(
                    self.request_queue.items
                )
                if (
                    str(request.get("id"))
                    == str(latest_request.get("id"))
                    and request.get("title", "").lower()
                    == latest_request.get("title", "").lower()
                )
            ),
            None
        )

        if queue_index is None:
            messagebox.showerror(
                "Request Not Found",
                "The latest request was not found in the pending queue. "
                "No request was cancelled."
            )
            return

        if not messagebox.askyesno(
            "Cancel Last Added Request",
            f"Cancel the most recently added pending request?\n\n"
            f"{latest_request['title']}\n\n"
            "This uses Stack's Last In, First Out (LIFO) order."
        ):
            return

        cancelled_request = self.request_stack.pop()
        self.request_queue.items.pop(queue_index)

        self.log_activity(
            f"Cancelled pending request: {cancelled_request['title']}"
        )

        messagebox.showinfo(
            "Request Cancelled",
            f"Cancelled request:\n\n{cancelled_request['title']}"
        )

        self.show_page("Activity & Requests")

    def show_activity(self):
        self.page_header(
            "Activity & Requests",
            "Manage book requests with Queue and Stack, and review recent activity."
        )

        panel = tk.Frame(
            self.main_area,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        tk.Label(
            panel,
            text="Book Request Queue",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 3))

        tk.Label(
            panel,
            text=(
                "Queue uses FIFO: the oldest request is processed first."
            ),
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=20, pady=(0, 10))

        request_controls = tk.Frame(panel, bg=WHITE)
        request_controls.pack(fill="x", padx=20, pady=(0, 8))

        titles = sorted(
            {
                str(book.get("title", "")).strip()
                for book in self.books
                if str(book.get("title", "")).strip()
            },
            key=str.lower
        )

        self.request_title_var = tk.StringVar()

        request_box = ttk.Combobox(
            request_controls,
            textvariable=self.request_title_var,
            values=titles,
            state="readonly",
            width=35
        )

        request_box.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=4
        )

        tk.Button(
            request_controls,
            text="+ Add Request",
            command=self.add_book_request,
            bg=SAGE,
            fg=DARK,
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(8, 0))

        queue_list_frame = tk.Frame(panel, bg=WHITE)
        queue_list_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        self.request_listbox = tk.Listbox(
            queue_list_frame,
            height=3,
            font=("Segoe UI", 10),
            bg="#FCFBF8",
            fg=DARK,
            selectbackground=BLUE,
            selectforeground=DARK,
            relief="solid",
            bd=1,
            activestyle="none"
        )

        self.request_listbox.pack(fill="x", expand=True)

        request_actions = tk.Frame(panel, bg=WHITE)
        request_actions.pack(fill="x", padx=20, pady=(0, 6))

        tk.Button(
            request_actions,
            text="Process Next Request (FIFO)",
            command=self.process_next_request,
            bg=BLUE,
            fg=DARK,
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            request_actions,
            text="Cancel Last Added (LIFO)",
            command=self.cancel_last_added_request,
            bg=PEACH,
            fg=DARK,
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        tk.Label(
            panel,
            text="Request Stack",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=20, pady=(5, 2))

        self.stack_status_label = tk.Label(
            panel,
            text="",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
            anchor="w",
            justify="left",
            wraplength=750
        )

        self.stack_status_label.pack(
            anchor="w",
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        self.refresh_request_queue()

        tk.Frame(
            panel,
            bg=BORDER,
            height=1
        ).pack(fill="x", padx=20, pady=(2, 10))

        tk.Label(
            panel,
            text="Recent Activity",
            bg=WHITE,
            fg=DARK,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(0, 8))

        activity_frame = tk.Frame(panel, bg=WHITE)
        activity_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        activity_scrollbar = ttk.Scrollbar(
            activity_frame,
            orient="vertical"
        )

        activity_canvas = tk.Canvas(
            activity_frame,
            bg=WHITE,
            highlightthickness=0,
            yscrollcommand=activity_scrollbar.set
        )

        activity_scrollbar.configure(
            command=activity_canvas.yview
        )

        activity_scrollbar.pack(side="right", fill="y")
        activity_canvas.pack(side="left", fill="both", expand=True)

        activity_content = tk.Frame(activity_canvas, bg=WHITE)

        activity_window = activity_canvas.create_window(
            (0, 0),
            window=activity_content,
            anchor="nw"
        )

        def update_activity_scroll_region(event=None):
            activity_canvas.configure(
                scrollregion=activity_canvas.bbox("all")
            )

        def resize_activity_content(event):
            activity_canvas.itemconfigure(
                activity_window,
                width=event.width
            )

        activity_content.bind(
            "<Configure>",
            update_activity_scroll_region
        )

        activity_canvas.bind(
            "<Configure>",
            resize_activity_content
        )

        activities = self.activities.display()

        if not activities:
            tk.Label(
                activity_content,
                text="No activity recorded in this session yet.",
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=5)

        else:
            for activity in activities:
                tk.Label(
                    activity_content,
                    text=f"•  {activity}",
                    bg=WHITE,
                    fg=DARK,
                    font=("Segoe UI", 10),
                    anchor="w",
                    justify="left",
                    wraplength=650
                ).pack(anchor="w", fill="x", pady=4)


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartLibrary(root)
    root.mainloop()