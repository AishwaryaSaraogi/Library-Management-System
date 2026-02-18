from datetime import datetime, timedelta

class Book:
    """Defines structured models for books [cite: 10]"""
    def __init__(self, book_id, title, author, category="General"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category  # Premium: Categorized shelves [cite: 20]
        self.is_issued = False

class Member:
    """Defines structured models for members [cite: 10]"""
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.issued_books = []  # Track issued books [cite: 6, 12]
        self.total_fine = 0.0

class LibrarySystem:
    def __init__(self):
        # Books and Members Databases [cite: 8]
        self.books = {}    
        self.members = {}  
        self.fine_per_day = 10.0 # Per-day late fee rule [cite: 15]

    # --- Book Inventory Module [cite: 6, 11] ---
    def add_book(self, book_id, title, author, category="General"):
        new_book = Book(book_id, title, author, category)
        self.books[book_id] = new_book
        print(f"Successfully added: {title}")

    def search_books(self, keyword):
        """Keyword-based search with partial matching [cite: 18]"""
        keyword = keyword.lower()
        results = [
            b for b in self.books.values() 
            if keyword in b.title.lower() or keyword in b.author.lower()
        ]
        return results

    # --- Member Management [cite: 6, 12] ---
    def register_member(self, member_id, name):
        self.members[member_id] = Member(member_id, name)
        print(f"Member '{name}' registered (ID: {member_id}).")

    # --- Issue Module [cite: 8, 13] ---
    def issue_book(self, book_id, member_id):
        book = self.books.get(book_id)
        member = self.members.get(member_id)

        # Validate availability [cite: 6]
        if not book or book.is_issued:
            print("Error: Book is currently unavailable.")
            return
        
        # Premium: Block members exceeding fine limits [cite: 19]
        if member.total_fine > 100:
            print(f"Issue Blocked: {member.name} exceeds fine limit.")
            return

        book.is_issued = True
        # Assigning due dates [cite: 13]
        due_date = datetime.now() + timedelta(days=14) 
        member.issued_books.append({'book_id': book_id, 'due_date': due_date})
        print(f"Book '{book.title}' issued. Due date: {due_date.date()}")

    # --- Return & Fine Calculation [cite: 6, 14, 15] ---
    def return_book(self, book_id, member_id, return_date_str):
        member = self.members.get(member_id)
        book = self.books.get(book_id)
        
        # Convert string to date object for comparison [cite: 14]
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d")

        for record in member.issued_books:
            if record['book_id'] == book_id:
                # Calculate late fees [cite: 15]
                days_late = (return_date - record['due_date']).days
                if days_late > 0:
                    fine = days_late * self.fine_per_day
                    member.total_fine += fine
                    print(f"Late Return! Fine: ${fine:.2f}")
                
                book.is_issued = False
                member.issued_books.remove(record)
                print(f"Book '{book.title}' returned successfully.")
                return
        print("Record not found.")

    # --- Reports [cite: 8, 16] ---
    def generate_report(self):
        print("\n--- Library Activity Report ---")
        for m in self.members.values():
            status = "Clear" if m.total_fine == 0 else f"Fine Due: ${m.total_fine}"
            print(f"Member: {m.name} | Books Held: {len(m.issued_books)} | Status: {status}")

# --- Demonstration Logic ---
if __name__ == "__main__":
    lib = LibrarySystem()
    
    # 1. Add Books [cite: 11]
    lib.add_book("B001", "Python Basics", "John Smith", "Education")
    lib.add_book("B002", "Data Science 101", "Jane Doe", "Science")
    
    # 2. Register Member [cite: 12]
    lib.register_member("M101", "Alice")
    
    # 3. Issue Book [cite: 13]
    lib.issue_book("B001", "M101")
    
    # 4. Return Book (Simulating a late return) 
    # Assuming return is 20 days from now (6 days late)
    late_date = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d")
    lib.return_book("B001", "M101", late_date)
    
    # 5. Show Final Report [cite: 16]
    lib.generate_report()