import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import sqlite3
from datetime import datetime
import os

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("CIB Inventory Management System")
        self.root.geometry("1080x720")
        self.root.configure(bg="#f0f0f0")

        # Get the directory of the executable or script
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Load images
        try:
            self.employee_img = PhotoImage(file=os.path.join(base_dir, "images", "employee_icon.png"))
            self.database_img = PhotoImage(file=os.path.join(base_dir, "images", "database_icon.png"))
            self.item_img = PhotoImage(file=os.path.join(base_dir, "images", "item_icon.png"))
            self.logout_img = PhotoImage(file=os.path.join(base_dir, "images", "logout_icon.png"))
            self.login_image = PhotoImage(file=os.path.join(base_dir, "images", "login_icon.png"))
        except:
            # Create blank images if actual images aren't found
            self.employee_img = PhotoImage(width=48, height=48)
            self.database_img = PhotoImage(width=48, height=48)
            self.item_img = PhotoImage(width=48, height=48)
            self.logout_img = PhotoImage(width=48, height=48)
            self.login_image = PhotoImage(width=48, height=48)
        
        # Initialize database
        self.create_database()
        
        # Variables for login
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Variables for item entry
        self.item_code_var = tk.StringVar()
        self.product_code_var = tk.StringVar()
        self.item_name_var = tk.StringVar()
        self.selling_price_var = tk.StringVar()
        
        # Variables for dropdowns
        self.item_code_dropdown_var = tk.StringVar()
        self.product_code_dropdown_var = tk.StringVar()
        self.item_name_dropdown_var = tk.StringVar()
        self.selling_price_dropdown_var = tk.StringVar()
        
        # Variable for category selection
        self.selected_category = tk.StringVar()
        
        # Define categories and their items
        self.categories = {
            "LADIES 2FOLD": [
                "2 FOLD BLACK", "2 FOLD SATIN", "2 FOLD BLACK UV",
                "2 FOLD PLAIN COLOUR WITH PRINT", "2 FOLD PLAIN BORDER DESIGN",
                "2 FOLD PRINTED UV", "2 FOLD PRINTED FRIELD UMBRELLA",
                "2 FOLD BLACK HALF MOON"
            ],
            "LADIES 3 FOLD": [
                "3 FOLD BLACK", "3 FOLD PRINTED", "3 FOLD SATIN",
                "3 FOLD BLACK UV", "3 FOLD PLAIN COLOUR WITH PRINT",
                "3 FOLD PLAIN BORDER DESIGN", "3 FOLD UV PRINTED",
                "3 FOLD PRINTED FRIELD UMBRELLA", "3 FOLD BLACK HALF MOON"
            ],
            "24\" GENTS": [
                "24*16 GOLD METAL FRAME MANUAL OPEN BLACK",
                "24*16 GOLD METAL FRAME MANUAL OPEN MULTI",
                "24*16 GOLD METAL FRAME MANUAL OPEN SILVER",
                "24*16 MANUAL OPEN TELESCOPE (MULTI)"
            ],
            "27\" GENTS": [
                "27*16 GOLD METAL FRAME MANUAL OPEN BLACK",
                "27*16 GOLD METAL FRAME MANUAL OPEN MULTI",
                "27*16 GOLD METAL FRAME MANUAL OPEN UV",
                "27*16 MANUAL OPEN TELESCOPE (MULTI)",
                "27*16 METAL FRAME MULTI-SIXTY PANNEL"
            ],
            "30\" GENTS": [
                "30*16 GOLD METAL FRAME MANUAL OPEN PLAIN",
                "30*16 GOLD METAL FRAME MANUAL OPEN MULTI",
                "30*16 GOLD METAL FRAME MANUAL OPEN UV",
                "30*16 METAL FRAME MULTI-SIXTY PANNEL"
            ],
            "MUTHU UMBRELLA": [
                "NORMAL MUTHU UMBRELLA WHITE", "NORMAL MUTHU UMBRELLA YELLOW",
                "NORMAL FRILED WITH RIB COVER WHITE", "NORMAL FRILED WITH RIB COVER YELLOW",
                "SEAQUEENS FRILED WITH RIB COVER WHITE", "SEAQUEENS FRILED WITH RIB COVER YELLOW",
                "DESIGN FRILED WITH RIB COVER YELLOW", "DESIGN FRILED WITH RIB COVER WHITE",
                "NORMAL MUTHU UMBRELLA WHITE SIXTY PANNEL", "NORMAL MUTHU UMBRELLA YELLOW SIXTY PANNEL"
            ],
            "CAR UMBRELLA": ["CAR UMBRELLA"],
            "GARDEN UMBRELLA": [
                "36*8 GARDEN UMBRELLA", "44*16 GARDEN UMBRELLA",
                "44*16 GARDEN UMBRELLA SIXTY PANNEL"
            ],
            "BABY UMBRELLA": [
                "BABY PLAIN", "BABY PRINTED", "BABY TELESCOPE UMBRELLA"
            ],
            "PIRIKARA UMBRELLA": [
                "2 FOLD (BLACK)", "2 FOLD (BROWN)", "2 FOLD (ORANGE)",
                "2 FOLD (YELLOW)", "2 FOLD (MEROON)", "24*16 MANUAL PIRIKARA (BLACK)",
                "24*16 MANUAL PIRIKARA (BROWN)", "24*16 MANUAL PIRIKARA (ORANGE)",
                "24*16 MANUAL PIRIKARA (MEROON)", "24*16 MANUAL PIRIKARA (YELLOW)"
            ],
            "MOSQUITO NETS": [
                "SR-NORMAL NETS SMALL", "SR-NORMAL NETS MEDIUM",
                "SR-NORMAL NETS LARGE", "SR-NORMAL NETS EXTRA LARGE"
            ]
        }

        # Shopping cart for bill printing
        self.cart_items = []
        
        # Create frames
        self.login_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.item_frame = tk.Frame(self.root, bg="#f0f0f0")
        
        # Start with login frame
        self.show_login_frame()
    
    def create_database(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        
        # Create items table with stricter constraints
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_code TEXT NOT NULL CHECK(length(item_code) > 0),
            product_code TEXT UNIQUE NOT NULL CHECK(length(product_code) > 0),
            item_name TEXT NOT NULL CHECK(length(item_name) > 0),
            selling_price REAL NOT NULL CHECK(selling_price >= 0),
            date_added TEXT NOT NULL
        )
        ''')
        
        # Create default admin user if it doesn't exist
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                          ('admin', 'admin123', 'admin'))
        
        # Insert sample items if they don't exist
        sample_items = [
            ('100100008', 'S2001', '2 FOLD BLACK', 930.00, '2025-05-04 10:34:01'),
            ('100100009', 'S2002', '2FOLD PRINTED', 950.00, '2025-05-04 10:34:01'),
            ('100100010', 'S2003', '2FOLD SATIN', 1050.00, '2025-05-04 10:34:01'),
            ('100100015', 'S2004', '2FOLD BLACK UV', 1240.00, '2025-05-04 10:34:01'),
            ('100100012', 'S2005', '2FOLD PLAIN COLOUR WITH PRINT', 1210.00, '2025-05-04 10:34:01'),
            ('100100013', 'S2006', '2FOLD PLAIN BORDER DESIGN', 1250.00, '2025-05-04 10:34:01'),
            ('100100011', 'S2008', '2FOLD PRINTED UV', 1260.00, '2025-05-04 10:34:01'),
            ('100100090', 'S2009', '2FOLD PRINTED FRIELD UMBRELLA', 1130.00, '2025-05-04 10:34:01'),
            ('100100091', 'S2010', '2FOLD BLACK HALF MOON', 1120.00, '2025-05-04 10:34:01'),
        ]
        
        for item in sample_items:
            cursor.execute("SELECT * FROM items WHERE item_code=?", (item[0],))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO items (item_code, product_code, item_name, selling_price, date_added) VALUES (?, ?, ?, ?, ?)", item)
        
        # Clean up any invalid entries (like those with "✅" or "OK" in price)
        cursor.execute("UPDATE items SET selling_price = 0 WHERE selling_price NOT LIKE '%.%' AND selling_price NOT GLOB '*[0-9]*'")
        
        conn.commit()
        conn.close()
    
    def logout(self):
        """Handle user logout with confirmation"""
        confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out?")
        if confirm:
            # Clear all entry fields and variables
            self.clear_fields()
            # Reset cart items
            self.cart_items = []
            # Show login frame
            self.show_login_frame()
    
    def show_login_frame(self):
        # Hide all frames
        self.main_frame.pack_forget()
        self.item_frame.pack_forget()
        
        # Configure login frame with gradient background
        self.login_frame = tk.Frame(self.root, bg="#0047B3")
        self.login_frame.pack(fill="both", expand=True)
        
        # Create gradient background
        canvas = tk.Canvas(self.login_frame, width=1080, height=720, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Draw gradient from dark blue to lighter blue
        for i in range(720):
            r = int(0 + (100 - 0) * (i / 720))
            g = int(71 + (150 - 71) * (i / 720))
            b = int(179 + (255 - 179) * (i / 720))
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, 1080, i, fill=color)
        
        # Main container for login elements
        login_container = tk.Frame(canvas, bg="white", bd=0, relief="flat")
        login_container.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)
        
        # Add subtle shadow effect
        shadow = tk.Frame(login_container, bg="#e0e0e0")
        shadow.place(x=5, y=5, relwidth=1, relheight=1, width=-5, height=-5)
        
        # Title with logo
        logo_frame = tk.Frame(login_container, bg="white")
        logo_frame.pack(pady=(30, 20))
        
        # Logo icon
        logo_icon = tk.Label(logo_frame, image=self.login_image, font=("Arial", 40), bg="white")
        logo_icon.pack(side="left", padx=10)
        
        # Title text
        title_text = tk.Label(logo_frame, bg="white", fg="#0047B3")
        title_text.pack(side="left")
        
        subtitle = tk.Label(login_container, text="CIB Inventory Management System", 
                           font=("Arial", 12), bg="white", fg="#666")
        subtitle.pack(pady=(0, 30))
        
        # Input fields container
        input_frame = tk.Frame(login_container, bg="white")
        input_frame.pack(pady=10, padx=30, fill="x")
        
        # Username field
        username_label = tk.Label(input_frame, text="Username", 
                                font=("Arial", 10), bg="white", fg="#555", anchor="w")
        username_label.pack(fill="x", pady=(5, 0))
        
        username_entry = tk.Entry(input_frame, textvariable=self.username_var, 
                                font=("Arial", 12), bd=1, relief="solid",
                                highlightthickness=1, highlightcolor="#0047B3",
                                highlightbackground="#ddd")
        username_entry.pack(fill="x", pady=5, ipady=8)
        
        # Password field
        password_label = tk.Label(input_frame, text="Password", 
                                font=("Arial", 10), bg="white", fg="#555", anchor="w")
        password_label.pack(fill="x", pady=(15, 0))
        
        password_entry = tk.Entry(input_frame, textvariable=self.password_var, 
                                font=("Arial", 12), show="*", 
                                bd=1, relief="solid",
                                highlightthickness=1, highlightcolor="#0047B3",
                                highlightbackground="#ddd")
        password_entry.pack(fill="x", pady=5, ipady=8)
        
        # Login button with hover effect
        def on_enter(e):
            login_button['background'] = '#003399'
        
        def on_leave(e):
            login_button['background'] = '#0047B3'
        
        login_button = tk.Button(login_container, text="LOG IN", 
                               font=("Arial", 12, 'bold'), bg="#0047B3", fg="white",
                               command=self.login, bd=0, cursor="hand2",
                               activebackground="#003399", activeforeground="white",
                               padx=20, pady=10)
        login_button.pack(pady=30, ipadx=30)
        login_button.bind("<Enter>", on_enter)
        login_button.bind("<Leave>", on_leave)
        
        # Footer
        footer = tk.Label(login_container, text="© 2024 CIB Inventory System", 
                         font=("Arial", 8), bg="white", fg="#999")
        footer.pack(side="bottom", pady=10)
        
        # Bind the enter key to Login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Set focus to username field
        username_entry.focus_set()
    
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required")
            return
        
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            self.username_var.set("")
            self.password_var.set("")
            self.show_main_frame()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_main_frame(self):
        """Show the main application frame"""
        # Hide other frames
        self.login_frame.pack_forget()
        self.item_frame.pack_forget()
        
        # Configure main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar(self.main_frame)
        
        # Main content area
        content_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="CIB inventory management system", 
                              font=("Arial", 24, "bold"), fg="white", bg="#0047B3")
        title_label.pack(fill="x", pady=(0, 20))
        
        # Database section title
        db_title = tk.Label(content_frame, text="Database", font=("Arial", 14), fg="white", bg="#0047B3")
        db_title.pack(fill="x", pady=(0, 10))
        
        # Content container
        container = tk.Frame(content_frame, bg="#f0f0f0", relief="ridge", bd=1)
        container.pack(fill="both", expand=True)
        
        # Item entry area
        entry_frame = tk.Frame(container, bg="#f0f0f0")
        entry_frame.pack(fill="x", padx=10, pady=10)
        
        # Entry fields
        item_code_frame = tk.Frame(entry_frame, bg="#5271FF")
        item_code_frame.grid(row=0, column=0, padx=5, pady=5)
        item_code_label = tk.Label(item_code_frame, text="Item code", bg="#5271FF", fg="white")
        item_code_label.pack(side="left", padx=5)
        tk.Label(item_code_frame, text="▼", bg="#5271FF", fg="white").pack(side="right", padx=5)
        
        product_code_frame = tk.Frame(entry_frame, bg="#5271FF")
        product_code_frame.grid(row=0, column=1, padx=5, pady=5)
        product_code_label = tk.Label(product_code_frame, text="Product code", bg="#5271FF", fg="white")
        product_code_label.pack(side="left", padx=5)
        tk.Label(product_code_frame, text="▼", bg="#5271FF", fg="white").pack(side="right", padx=5)
        
        item_name_frame = tk.Frame(entry_frame, bg="#5271FF")
        item_name_frame.grid(row=0, column=2, padx=5, pady=5)
        item_name_label = tk.Label(item_name_frame, text="Item", bg="#5271FF", fg="white")
        item_name_label.pack(side="left", padx=5)
        tk.Label(item_name_frame, text="▼", bg="#5271FF", fg="white").pack(side="right", padx=5)
        
        selling_price_frame = tk.Frame(entry_frame, bg="#5271FF")
        selling_price_frame.grid(row=0, column=3, padx=5, pady=5)
        selling_price_label = tk.Label(selling_price_frame, text="Selling price", bg="#5271FF", fg="white")
        selling_price_label.pack(side="left", padx=5)
        tk.Label(selling_price_frame, text="▼", bg="#5271FF", fg="white").pack(side="right", padx=5)
        
        # Entry widgets
        item_code_entry = tk.Entry(entry_frame, textvariable=self.item_code_var, width=15)
        item_code_entry.grid(row=1, column=0, padx=5, pady=5)
        
        product_code_entry = tk.Entry(entry_frame, textvariable=self.product_code_var, width=15)
        product_code_entry.grid(row=1, column=1, padx=5, pady=5)
        
        item_name_entry = tk.Entry(entry_frame, textvariable=self.item_name_var, width=15)
        item_name_entry.grid(row=1, column=2, padx=5, pady=5)
        
        selling_price_entry = tk.Entry(entry_frame, textvariable=self.selling_price_var, width=15)
        selling_price_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Table for item display
        tree_frame = tk.Frame(container)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("item_code", "product_code", "item_name", "selling_price", "date_added")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10, selectmode="extended")
        
        # Configure columns
        self.tree.heading("item_code", text="Item Code")
        self.tree.heading("product_code", text="Product Code")
        self.tree.heading("item_name", text="Item Name")
        self.tree.heading("selling_price", text="Selling Price")
        self.tree.heading("date_added", text="Date Added")
        
        self.tree.column("item_code", width=100)
        self.tree.column("product_code", width=100)
        self.tree.column("item_name", width=150)
        self.tree.column("selling_price", width=100)
        self.tree.column("date_added", width=150)
        
        # Bind the treeview select event
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # Cart section
        cart_frame = tk.Frame(container, bg="#f0f0f0")
        cart_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        cart_label = tk.Label(cart_frame, text="Receipt", font=("Arial", 10, "bold"), bg="#f0f0f0")
        cart_label.pack(side="left")
        
        self.cart_count_label = tk.Label(cart_frame, text="Items in receipt: 0", font=("Arial", 10), bg="#f0f0f0")
        self.cart_count_label.pack(side="left", padx=20)
        
        clear_cart_btn = tk.Button(cart_frame, text="Clear Receipt", bg="#FF5252", fg="white", 
                                  command=self.clear_cart, cursor="hand2")
        clear_cart_btn.pack(side="right")
        
        add_to_cart_btn = tk.Button(cart_frame, text="Add to Receipt", bg="#5271FF", fg="white", 
                                   command=self.add_to_cart, cursor="hand2")
        add_to_cart_btn.pack(side="right", padx=10)
        
        # Action buttons frame
        buttons_container = tk.Frame(container, bg="#f0f0f0")
        buttons_container.pack(fill="x", padx=10, pady=10)
        
        # Action buttons
        button_frame = tk.Frame(buttons_container, bg="#f0f0f0")
        button_frame.pack(side="right")
        
        add_btn = tk.Button(button_frame, text="ADD Item", bg="#5271FF", fg="white", 
                           width=15, height=2, font=("Arial", 10, "bold"), 
                           command=self.add_item, cursor="hand2")
        add_btn.grid(row=0, column=0, pady=5, padx=5)
        
        delete_btn = tk.Button(button_frame, text="Delete Item", bg="#5271FF", fg="white", 
                              width=15, height=2, font=("Arial", 10, "bold"), 
                              command=self.delete_item, cursor="hand2")
        delete_btn.grid(row=0, column=1, pady=5, padx=5)
        
        update_btn = tk.Button(button_frame, text="Update Item", bg="#5271FF", fg="white", 
                              width=15, height=2, font=("Arial", 10, "bold"), 
                              command=self.update_item, cursor="hand2")
        update_btn.grid(row=1, column=0, pady=5, padx=5)
        
        print_btn = tk.Button(button_frame, text="Print Receipt", bg="#5271FF", fg="white", 
                             width=15, height=2, font=("Arial", 10, "bold"), 
                             command=self.print_bill, cursor="hand2")
        print_btn.grid(row=1, column=1, pady=5, padx=5)
        
        # Load items
        self.load_items()
    
    def show_item_frame(self):
        """Show the Item Management frame with dropdown menus and category radio buttons"""
        # Hide other frames
        self.main_frame.pack_forget()
        self.login_frame.pack_forget()
        
        # Configure item frame
        self.item_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.item_frame.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar(self.item_frame)
        
        # Main content area
        content_frame = tk.Frame(self.item_frame, bg="#f0f0f0")
        content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(content_frame, text="CIB inventory management system - Item Management", 
                              font=("Arial", 20, "bold"), fg="white", bg="#0047B3")
        title_label.pack(fill="x", pady=(0, 20))
        
        # Database section title
        db_title = tk.Label(content_frame, text="Item Management", font=("Arial", 14), fg="white", bg="#0047B3")
        db_title.pack(fill="x", pady=(0, 10))
        
        # Content container
        container = tk.Frame(content_frame, bg="#f0f0f0", relief="ridge", bd=1)
        container.pack(fill="both", expand=True)
        
        # Create a frame for the left side (categories and dropdowns) and right side (treeview)
        main_content_frame = tk.Frame(container, bg="#f0f0f0")
        main_content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left side frame for categories and dropdowns
        left_frame = tk.Frame(main_content_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        # Category selection frame (radio buttons)
        category_frame = tk.LabelFrame(left_frame, text="Categories", bg="#f0f0f0", font=("Arial", 10, "bold"))
        category_frame.pack(fill="x", padx=5, pady=5)
        
        # Create a vertical frame for radio buttons
        radio_frame = tk.Frame(category_frame, bg="#f0f0f0")
        radio_frame.pack(fill="both", expand=True)
        
        # Create radio buttons for each category in a vertical layout
        for category in self.categories.keys():
            rb = tk.Radiobutton(
                radio_frame,
                text=category,
                variable=self.selected_category,
                value=category,
                command=self.update_item_dropdowns,
                bg="#f0f0f0",
                anchor="w",
                width=20  # Set a fixed width for alignment
            )
            rb.pack(anchor="w", padx=5, pady=2)
        
        # Dropdown selection area
        dropdown_frame = tk.LabelFrame(left_frame, text="Database", bg="#f0f0f0", font=("Arial", 10, "bold"))
        dropdown_frame.pack(fill="x", padx=5, pady=5)
        
        # Create dropdown menus with labels
        tk.Label(dropdown_frame, text="Item Code:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.item_code_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.item_code_dropdown_var, 
                                             state="readonly", width=20)
        self.item_code_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.item_code_dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        
        tk.Label(dropdown_frame, text="Product Code:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.product_code_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.product_code_dropdown_var, 
                                               state="readonly", width=20)
        self.product_code_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.product_code_dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        
        tk.Label(dropdown_frame, text="Item Name:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.item_name_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.item_name_dropdown_var, 
                                            state="readonly", width=20)
        self.item_name_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.item_name_dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        
        tk.Label(dropdown_frame, text="Selling Price:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.selling_price_dropdown = ttk.Combobox(dropdown_frame, textvariable=self.selling_price_dropdown_var, 
                                                state="readonly", width=20)
        self.selling_price_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.selling_price_dropdown.bind("<<ComboboxSelected>>", self.on_dropdown_select)
        
        # Search and Clear buttons
        search_btn = tk.Button(dropdown_frame, text="Search", bg="#5271FF", fg="white", 
                              command=self.search_items, cursor="hand2", width=10)
        search_btn.grid(row=4, column=0, padx=5, pady=10, sticky="e")
        
        clear_search_btn = tk.Button(dropdown_frame, text="Clear Search", bg="#FF5252", fg="white", 
                                    command=self.clear_item_search, cursor="hand2", width=10)
        clear_search_btn.grid(row=4, column=1, padx=5, pady=10, sticky="w")
        
        # Right side frame for the treeview
        right_frame = tk.Frame(main_content_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Table for item display
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("item_code", "product_code", "item_name", "selling_price", "date_added")
        self.item_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10, selectmode="extended")
        
        # Configure columns
        self.item_tree.heading("item_code", text="Item Code")
        self.item_tree.heading("product_code", text="Product Code")
        self.item_tree.heading("item_name", text="Item Name")
        self.item_tree.heading("selling_price", text="Selling Price")
        self.item_tree.heading("date_added", text="Date Added")
        
        self.item_tree.column("item_code", width=100)
        self.item_tree.column("product_code", width=100)
        self.item_tree.column("item_name", width=150)
        self.item_tree.column("selling_price", width=100)
        self.item_tree.column("date_added", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.item_tree.pack(fill="both", expand=True)
        
        # Cart section
        cart_frame = tk.Frame(right_frame, bg="#f0f0f0")
        cart_frame.pack(fill="x", pady=(10, 0))
        
        cart_label = tk.Label(cart_frame, text="Receipt", font=("Arial", 10, "bold"), bg="#f0f0f0")
        cart_label.pack(side="left")
        
        self.cart_count_label = tk.Label(cart_frame, text="Items in receipt: 0", font=("Arial", 10), bg="#f0f0f0")
        self.cart_count_label.pack(side="left", padx=20)
        
        clear_cart_btn = tk.Button(cart_frame, text="Clear Receipt", bg="#FF5252", fg="white", 
                                  command=self.clear_cart, cursor="hand2")
        clear_cart_btn.pack(side="right")
        
        add_to_cart_btn = tk.Button(cart_frame, text="Add to Receipt", bg="#5271FF", fg="white", 
                                   command=self.add_to_cart, cursor="hand2")
        add_to_cart_btn.pack(side="right", padx=10)
        
        # Print button
        print_btn = tk.Button(right_frame, text="Print Receipt", bg="#5271FF", fg="white", 
                             width=15, height=2, font=("Arial", 10, "bold"), 
                             command=self.print_bill, cursor="hand2")
        print_btn.pack(pady=10)
        
        # Load all items initially
        self.load_item_tree()
    
    def create_sidebar(self, parent_frame):
        """Create the sidebar with navigation buttons"""
        sidebar_frame = tk.Frame(parent_frame, bg="#0047B3", width=70)
        sidebar_frame.pack(side="left", fill="y")
        
        # Sidebar buttons
        employee_btn = tk.Button(sidebar_frame, image=self.employee_img, bg="#0047B3",
                               relief="flat", command=self.show_main_frame, cursor="hand2")
        employee_btn.pack(pady=(20, 10), padx=10)
        employee_label = tk.Label(sidebar_frame, text="Employee", font=("Arial", 10), bg="#0047B3", fg="white")
        employee_label.pack()
        
        database_btn = tk.Button(sidebar_frame, image=self.database_img, bg="#0047B3",
                               relief="flat", command=self.show_main_frame, cursor="hand2")
        database_btn.pack(pady=(20, 10), padx=10)
        database_label = tk.Label(sidebar_frame, text="Database", font=("Arial", 10), bg="#0047B3", fg="white")
        database_label.pack()
        
        item_btn = tk.Button(sidebar_frame, image=self.item_img, bg="#0047B3",
                           relief="flat", command=self.show_item_frame, cursor="hand2")
        item_btn.pack(pady=(30, 15), padx=10)
        item_label = tk.Label(sidebar_frame, text="Item", font=("Arial", 10), bg="#0047B3", fg="white")
        item_label.pack()
        
        # Log out button
        logout_btn = tk.Button(sidebar_frame, image=self.logout_img, bg="#0047B3",
                             relief="flat", command=self.logout, cursor="hand2")
        logout_btn.pack(pady=(30, 15), padx=10)
        logout_label = tk.Label(sidebar_frame, text="Log out", font=("Arial", 10), bg="#0047B3", fg="white")
        logout_label.pack()
    
    def update_item_dropdowns(self):
        """Update dropdown values based on selected category"""
        category = self.selected_category.get()
        if not category:
            return
            
        # Get items for the selected category
        category_items = self.categories.get(category, [])
        
        # Connect to database to get item details
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        # Get items that match the category's item names
        item_codes = []
        product_codes = []
        item_names = []
        selling_prices = []
        
        for item_name in category_items:
            cursor.execute("SELECT item_code, product_code, item_name, selling_price FROM items WHERE item_name=?", (item_name,))
            result = cursor.fetchone()
            if result:
                item_codes.append(result[0])
                product_codes.append(result[1])
                item_names.append(result[2])
                selling_prices.append(str(result[3]))
        
        conn.close()
        
        # Update dropdown values
        self.item_code_dropdown['values'] = item_codes
        self.product_code_dropdown['values'] = product_codes
        self.item_name_dropdown['values'] = item_names
        self.selling_price_dropdown['values'] = selling_prices
        
        # Clear current selections
        self.item_code_dropdown_var.set("")
        self.product_code_dropdown_var.set("")
        self.item_name_dropdown_var.set("")
        self.selling_price_dropdown_var.set("")
        
        # Update the item tree with items from this category
        self.update_item_tree_with_category(category_items)

    def update_item_tree_with_category(self, category_items):
        """Update the item treeview with items from the specified category"""
        # Clear current items
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        
        if not category_items:
            return
            
        # Connect to database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        # Build query to get all items that match the category's item names
        query = "SELECT item_code, product_code, item_name, selling_price, date_added FROM items WHERE item_name IN ({})".format(
            ','.join(['?'] * len(category_items)))
        cursor.execute(query, category_items)
        items = cursor.fetchall()
        conn.close()
        
        # Insert into treeview
        for item in items:
            self.item_tree.insert("", "end", values=item)
    
    def on_dropdown_select(self, event):
        """Handle selection from any dropdown menu"""
        # Get the selected value from the dropdown that triggered the event
        widget = event.widget
        selected_value = widget.get()
        
        # Determine which dropdown was selected
        if widget == self.item_code_dropdown:  # Item Code dropdown
            self.product_code_dropdown_var.set("")
            self.item_name_dropdown_var.set("")
            self.selling_price_dropdown_var.set("")
        elif widget == self.product_code_dropdown:  # Product Code dropdown
            self.item_code_dropdown_var.set("")
            self.item_name_dropdown_var.set("")
            self.selling_price_dropdown_var.set("")
        elif widget == self.item_name_dropdown:  # Item Name dropdown
            self.item_code_dropdown_var.set("")
            self.product_code_dropdown_var.set("")
            self.selling_price_dropdown_var.set("")
        elif widget == self.selling_price_dropdown:  # Selling Price dropdown
            self.item_code_dropdown_var.set("")
            self.product_code_dropdown_var.set("")
            self.item_name_dropdown_var.set("")
    
    def search_items(self):
        """Search items based on dropdown selections"""
        item_code = self.item_code_dropdown_var.get()
        product_code = self.product_code_dropdown_var.get()
        item_name = self.item_name_dropdown_var.get()
        selling_price = self.selling_price_dropdown_var.get()
        
        # Build query based on selected filters
        query = "SELECT item_code, product_code, item_name, selling_price, date_added FROM items WHERE 1=1"
        params = []
        
        if item_code:
            query += " AND item_code=?"
            params.append(item_code)
        
        if product_code:
            query += " AND product_code=?"
            params.append(product_code)
        
        if item_name:
            query += " AND item_name=?"
            params.append(item_name)
        
        if selling_price:
            query += " AND selling_price=?"
            params.append(float(selling_price))
        
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        items = cursor.fetchall()
        conn.close()
        
        # Clear current items
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        
        # Insert filtered items
        for item in items:
            self.item_tree.insert("", "end", values=item)
    
    def clear_item_search(self):
        """Clear all dropdown selections and reload all items"""
        self.item_code_dropdown_var.set("")
        self.product_code_dropdown_var.set("")
        self.item_name_dropdown_var.set("")
        self.selling_price_dropdown_var.set("")
        self.selected_category.set("")
        self.load_item_tree()
    
    def load_item_tree(self):
        """Load all items into the item treeview"""
        # Clear current items
        for item in self.item_tree.get_children():
            self.item_tree.delete(item)
        
        # Load from database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT item_code, product_code, item_name, selling_price, date_added FROM items")
        items = cursor.fetchall()
        conn.close()
        
        # Insert into treeview
        for item in items:
            self.item_tree.insert("", "end", values=item)
    
    def load_items(self):
        """Load all items into the main treeview"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load from database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT item_code, product_code, item_name, selling_price, date_added FROM items")
        items = cursor.fetchall()
        conn.close()
        
        # Insert into treeview
        for item in items:
            self.tree.insert("", "end", values=item)
    
    def add_to_cart(self):
        """Add selected items to the Receipt"""
        # Determine which treeview to use based on current frame
        if self.item_frame.winfo_ismapped():
            tree = self.item_tree
        else:
            tree = self.tree
        
        selected_items = tree.selection()
        
        if not selected_items:
            messagebox.showerror("Error", "No items selected")
            return
        
        for item_id in selected_items:
            item_values = tree.item(item_id, "values")
            try:
                item_data = {
                    'item_code': item_values[0],
                    'product_code': item_values[1],
                    'item_name': item_values[2],
                    'selling_price': float(item_values[3]),
                    'quantity': 1  # Default quantity
                }
                
                # Check if item already in receipt
                existing_item = next((i for i in self.cart_items if i['item_code'] == item_data['item_code']), None)
                if existing_item:
                    existing_item['quantity'] += 1
                else:
                    self.cart_items.append(item_data)
            except (ValueError, IndexError):
                messagebox.showerror("Error", f"Invalid data for item: {item_values}")
                continue
        
        # Update cart count label
        self.update_cart_count()
        messagebox.showinfo("Success", f"{len(selected_items)} item(s) added to cart")
    
    def update_cart_count(self):
        """Update the cart count label"""
        total_items = sum(item['quantity'] for item in self.cart_items)
        if self.item_frame.winfo_ismapped():
            self.cart_count_label.config(text=f"Items in receipt: {total_items}")
        else:
            self.cart_count_label.config(text=f"Items in receipt: {total_items}")
    
    def clear_cart(self):
        """Clear all items from the cart"""
        if not self.cart_items:
            return
        
        confirm = messagebox.askyesno("Clear receipt", "Are you sure you want to clear the cart?")
        if confirm:
            self.cart_items = []
            self.update_cart_count()
            messagebox.showinfo("Cart Cleared", "All items have been removed from the cart")
    
    def print_bill(self):
        """Generate and print a bill for all items in the cart"""
        if not self.cart_items:
            # If cart is empty, check if items are selected in tree
            if self.item_frame.winfo_ismapped():
                tree = self.item_tree
            else:
                tree = self.tree
            
            selected_items = tree.selection()
            if selected_items:
                # Add selected items to cart first
                self.add_to_cart()
            else:
                messagebox.showerror("Error", "No items in cart. Please add items to cart first.")
                return
        
        # Calculate totals
        subtotal = sum(item['selling_price'] * item['quantity'] for item in self.cart_items)
        tax = subtotal * 0.07  # 7% tax rate
        total = subtotal + tax
        
        # Generate a bill
        bill_text = f"""
=====================================================
                CIB INVENTORY SYSTEM
=====================================================
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Bill No: BILL-{datetime.now().strftime('%Y%m%d%H%M%S')}

-----------------------------------------------------
Item Code      Item Name       Qty    Price    Total
-----------------------------------------------------
"""
        
        # Add items to bill
        for item in self.cart_items:
            item_total = item['selling_price'] * item['quantity']
            bill_text += f"{item['item_code']:<15}{item['item_name']:<15}{item['quantity']:<8}Rs:{item['selling_price']:<8.2f}Rs:{item_total:<8.2f}\n"
        
        # Add totals
        bill_text += f"""
-----------------------------------------------------
Subtotal: Rs:{subtotal:.2f}
Tax (7%): Rs:{tax:.2f}
-----------------------------------------------------
TOTAL:    Rs:{total:.2f}
=====================================================
                   Thank You!
=====================================================
"""
        
        # Get user's desktop path for saving the bill
        try:
            if os.name == 'nt':  # Windows
                desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            else:  # macOS and Linux
                desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
                
            # If desktop folder doesn't exist, use home directory
            if not os.path.exists(desktop):
                desktop = os.path.expanduser('~')
                
            # Create a 'Bills' folder if it doesn't exist
            bills_folder = os.path.join(desktop, 'CIB_Bills')
            if not os.path.exists(bills_folder):
                os.makedirs(bills_folder)
                
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = os.path.join(bills_folder, f"CIB_Bill_{timestamp}.txt")
            
            # Save bill to file
            with open(filename, "w") as f:
                f.write(bill_text)
            
            # Also save a copy in the application directory for reference
            local_filename = f"bill_{timestamp}.txt"
            with open(local_filename, "w") as f:
                f.write(bill_text)
            
            messagebox.showinfo("Bill Generated", f"Bill has been saved to:\n{filename}")
            
            # Try to open the file with default text editor
            try:
                if os.name == 'nt':  # For Windows
                    os.startfile(filename)
                elif os.name == 'posix':  # For macOS and Linux
                    os.system(f"open {filename}" if os.uname().sysname == "Darwin" else f"xdg-open {filename}")
            except Exception as e:
                messagebox.showinfo("Note", f"Bill saved but couldn't automatically open it.\nYou can find it at: {filename}")
                
        except Exception as e:
            # Fallback to saving in the current directory if there's an issue
            filename = f"bill_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            with open(filename, "w") as f:
                f.write(bill_text)
            messagebox.showinfo("Bill Generated", f"Bill has been saved to the application folder as: {filename}")
        
        # Ask if user wants to clear cart after printing
        clear_confirm = messagebox.askyesno("Clear Cart", "Bill saved successfully. Clear cart now?")
        if clear_confirm:
            self.cart_items = []
            self.update_cart_count()
    
    def add_item(self):
        item_code = self.item_code_var.get()
        product_code = self.product_code_var.get()
        item_name = self.item_name_var.get()
        selling_price = self.selling_price_var.get()
        
        # Validate input
        if not (item_code and product_code and item_name and selling_price):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            selling_price = float(selling_price)
            if selling_price < 0:
                raise ValueError("Price cannot be negative")
        except ValueError:
            messagebox.showerror("Error", "Selling price must be a positive number")
            return
        
        try:
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            
            # Check if item code already exists
            cursor.execute("SELECT * FROM items WHERE product_code=?", (product_code,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Product code already exists")
                conn.close()
                return
            
            # Insert new item
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO items (item_code, product_code, item_name, selling_price, date_added) VALUES (?, ?, ?, ?, ?)",
                (item_code, product_code, item_name, selling_price, current_date)
            )
            conn.commit()
            conn.close()
            
            # Clear fields
            self.clear_fields()
            
            # Reload items
            self.load_items()
            
            messagebox.showinfo("Success", "Item added successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
    
    def delete_item(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showerror("Error", "No item selected")
            return
        
        item_values = self.tree.item(selected_item[0], "values")
        item_code = item_values[0]
        
        confirm = messagebox.askyesno("Confirm", f"Delete item {item_code}?")
        if confirm:
            try:
                conn = sqlite3.connect('inventory.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM items WHERE item_code=?", (item_code,))
                conn.commit()
                conn.close()
                
                self.load_items()
                self.clear_fields()
                
                messagebox.showinfo("Success", "Item deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}")
    
    def update_item(self):
        selected_items = self.tree.selection()
        
        if not selected_items:
            messagebox.showerror("Error", "No item selected")
            return
        
        item_code = self.item_code_var.get()
        product_code = self.product_code_var.get()
        item_name = self.item_name_var.get()
        selling_price = self.selling_price_var.get()
        
        # Validate input
        if not (item_code and product_code and item_name and selling_price):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            selling_price = float(selling_price)
            if selling_price < 0:
                raise ValueError("Price cannot be negative")
        except ValueError:
            messagebox.showerror("Error", "Selling price must be a positive number")
            return
        
        try:
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            
            # Update item
            cursor.execute(
                "UPDATE items SET product_code=?, item_name=?, selling_price=? WHERE item_code=?",
                (product_code, item_name, selling_price, item_code)
            )
            conn.commit()
            conn.close()
            
            # Reload items
            self.load_items()
            
            # Clear fields
            self.clear_fields()
            
            messagebox.showinfo("Success", "Item updated successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
    
    def clear_fields(self):
        self.item_code_var.set("")
        self.product_code_var.set("")
        self.item_name_var.set("")
        self.selling_price_var.set("")
    
    def on_item_select(self, event):
        selected_items = self.tree.selection()
        
        if len(selected_items) == 1:
            item_values = self.tree.item(selected_items[0], "values")
            if len(item_values) >= 4:  # Ensure all required values are present    
                self.item_code_var.set(item_values[0])
                self.product_code_var.set(item_values[1])
                self.item_name_var.set(item_values[2])
                self.selling_price_var.set(item_values[3])
        elif len(selected_items) > 1:
            # Clear form fields when multiple items are selected
            self.clear_fields()

# Main application runner
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()