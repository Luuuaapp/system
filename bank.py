import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import json
import os
from datetime import datetime
import hashlib

class BankingSystem:
    def __init__(self):
        self.data_file = "bank_data.json"
        self.bank_accounts = self.load_data()
        self.current_user_id = None
        self.setup_gui()
        
    def load_data(self):
        """Load bank data from file or create default accounts"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default accounts with hashed passwords
        return {
            "1234": {
                "name": "Mos'ab", 
                "balance": 5000.0, 
                "password": self.hash_password("pass123"),
                "transactions": []
            },
            "5678": {
                "name": "Yamba boy", 
                "balance": 3000.0, 
                "password": self.hash_password("word567"),
                "transactions": []
            }
        }
    
    def save_data(self):
        """Save bank data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.bank_accounts, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save data: {str(e)}")
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def add_transaction(self, user_id, transaction_type, amount, balance_after):
        """Add transaction to user's history"""
        transaction = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance": balance_after
        }
        
        if "transactions" not in self.bank_accounts[user_id]:
            self.bank_accounts[user_id]["transactions"] = []
        
        self.bank_accounts[user_id]["transactions"].append(transaction)
        # Keep only last 50 transactions
        if len(self.bank_accounts[user_id]["transactions"]) > 50:
            self.bank_accounts[user_id]["transactions"] = self.bank_accounts[user_id]["transactions"][-50:]
    
    def setup_gui(self):
        """Setup the GUI"""
        self.root = tk.Tk()
        self.root.title("Enhanced Bank System - Group 4")
        self.root.geometry("500x700")
        self.root.configure(bg="#f0f0f0")
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill="x", pady=(0, 20))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="GROUP 4 BANK SYSTEM", 
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title_label.pack(expand=True)
        
        # Status frame
        self.status_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.status_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Please log in or register",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        self.status_label.pack()
        
        # Button frame
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)
        
        # Create buttons with better styling
        button_config = {
            'width': 25,
            'height': 2,
            'font': ('Arial', 11),
            'cursor': 'hand2'
        }
        
        # Authentication buttons
        self.btn_login = tk.Button(
            self.button_frame, text="🔐 Login", command=self.login,
            bg="#3498db", fg="white", **button_config
        )
        
        self.btn_register = tk.Button(
            self.button_frame, text="📝 Register New Account", command=self.register,
            bg="#27ae60", fg="white", **button_config
        )
        
        self.btn_logout = tk.Button(
            self.button_frame, text="🚪 Logout", command=self.logout,
            bg="#95a5a6", fg="white", **button_config
        )
        
        # Banking operation buttons
        self.btn_deposit = tk.Button(
            self.button_frame, text="💰 Deposit", command=self.deposit,
            bg="#2ecc71", fg="white", **button_config
        )
        
        self.btn_withdraw = tk.Button(
            self.button_frame, text="💸 Withdraw", command=self.withdraw,
            bg="#e74c3c", fg="white", **button_config
        )
        
        self.btn_transfer = tk.Button(
            self.button_frame, text="💳 Transfer Money", command=self.transfer,
            bg="#9b59b6", fg="white", **button_config
        )
        
        self.btn_view = tk.Button(
            self.button_frame, text="👤 View Account", command=self.view_account,
            bg="#34495e", fg="white", **button_config
        )
        
        self.btn_history = tk.Button(
            self.button_frame, text="📊 Transaction History", command=self.view_history,
            bg="#16a085", fg="white", **button_config
        )
        
        # Admin buttons
        self.btn_show_all = tk.Button(
            self.button_frame, text="📋 Show All Accounts", command=self.show_all_accounts,
            bg="#d35400", fg="white", **button_config
        )
        
        self.btn_remove = tk.Button(
            self.button_frame, text="🗑️ Remove Account", command=self.remove_account,
            bg="#c0392b", fg="white", **button_config
        )
        
        # Exit button
        self.btn_exit = tk.Button(
            self.button_frame, text="❌ Exit", command=self.exit_app,
            bg="#7f8c8d", fg="white", **button_config
        )
        
        self.update_gui_state(logged_in=False)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
    
    def update_gui_state(self, logged_in):
        """Update GUI based on login state"""
        # Hide all buttons first
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()
        
        if logged_in:
            user_name = self.bank_accounts[self.current_user_id]['name']
            balance = self.bank_accounts[self.current_user_id]['balance']
            self.status_label.config(
                text=f"Welcome, {user_name}! | Balance: ₱{balance:,.2f}",
                fg="#27ae60"
            )
            
            # Show logged-in buttons
            buttons = [
                self.btn_logout, self.btn_deposit, self.btn_withdraw, 
                self.btn_transfer, self.btn_view, self.btn_history,
                self.btn_show_all, self.btn_remove, self.btn_exit
            ]
        else:
            self.status_label.config(
                text="Please log in or register",
                fg="#7f8c8d"
            )
            buttons = [self.btn_login, self.btn_register, self.btn_exit]
        
        for btn in buttons:
            btn.pack(pady=8)
    
    def is_valid_id(self, id_str):
        """Validate account ID"""
        return id_str and id_str.isdigit() and len(id_str) == 4
    
    def input_valid_id(self, title="Account ID"):
        """Get valid ID from user"""
        while True:
            id_input = simpledialog.askstring(title, "Enter 4-digit Account ID:")
            if id_input is None:
                return None
            if self.is_valid_id(id_input):
                return id_input
            messagebox.showerror("Invalid Input", "Please enter a valid 4-digit number.")
    
    def login(self):
        """Login function with improved validation"""
        if self.current_user_id:
            messagebox.showinfo("Already Logged In", 
                              f"Already logged in as {self.bank_accounts[self.current_user_id]['name']}")
            return
        
        account_id = self.input_valid_id("Login")
        if account_id is None:
            return
        
        if account_id not in self.bank_accounts:
            messagebox.showerror("Login Failed", "Account not found.")
            return
        
        # Get password
        password = simpledialog.askstring("Password", 
                                        f"Enter password for account {account_id}:", 
                                        show="*")
        if password is None:
            return
        
        # Verify password
        if self.hash_password(password) == self.bank_accounts[account_id]["password"]:
            self.current_user_id = account_id
            user_name = self.bank_accounts[account_id]['name']
            messagebox.showinfo("Login Success", f"Welcome back, {user_name}!")
            self.update_gui_state(logged_in=True)
        else:
            messagebox.showerror("Login Failed", "Incorrect password.")
    
    def logout(self):
        """Logout function"""
        if self.current_user_id:
            user_name = self.bank_accounts[self.current_user_id]['name']
            messagebox.showinfo("Logout", f"Goodbye, {user_name}!")
            self.current_user_id = None
        else:
            messagebox.showinfo("Logout", "You're not logged in.")
        
        self.update_gui_state(logged_in=False)
    
    def deposit(self):
        """Enhanced deposit function"""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please log in first.")
            return
        
        while True:
            amount_str = simpledialog.askstring("Deposit", 
                                              "Enter deposit amount (₱):")
            if amount_str is None:
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Invalid Amount", "Amount must be positive.")
                elif amount > 1000000:  # Maximum deposit limit
                    messagebox.showerror("Limit Exceeded", "Maximum deposit is ₱1,000,000.")
                else:
                    # Process deposit
                    self.bank_accounts[self.current_user_id]["balance"] += amount
                    new_balance = self.bank_accounts[self.current_user_id]["balance"]
                    
                    # Add to transaction history
                    self.add_transaction(self.current_user_id, "Deposit", amount, new_balance)
                    self.save_data()
                    
                    messagebox.showinfo("Deposit Success", 
                                      f"₱{amount:,.2f} deposited successfully!\n"
                                      f"New balance: ₱{new_balance:,.2f}")
                    
                    self.update_gui_state(logged_in=True)
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    def withdraw(self):
        """Enhanced withdraw function"""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please log in first.")
            return
        
        current_balance = self.bank_accounts[self.current_user_id]["balance"]
        
        while True:
            amount_str = simpledialog.askstring("Withdraw", 
                                              f"Enter withdrawal amount (₱):\n"
                                              f"Available balance: ₱{current_balance:,.2f}")
            if amount_str is None:
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Invalid Amount", "Amount must be positive.")
                elif amount > current_balance:
                    messagebox.showerror("Insufficient Funds", 
                                       f"Insufficient balance. Available: ₱{current_balance:,.2f}")
                else:
                    # Process withdrawal
                    self.bank_accounts[self.current_user_id]["balance"] -= amount
                    new_balance = self.bank_accounts[self.current_user_id]["balance"]
                    
                    # Add to transaction history
                    self.add_transaction(self.current_user_id, "Withdrawal", amount, new_balance)
                    self.save_data()
                    
                    messagebox.showinfo("Withdrawal Success", 
                                      f"₱{amount:,.2f} withdrawn successfully!\n"
                                      f"New balance: ₱{new_balance:,.2f}")
                    
                    self.update_gui_state(logged_in=True)
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    def transfer(self):
        """New transfer function"""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please log in first.")
            return
        
        # Get recipient account
        recipient_id = self.input_valid_id("Transfer - Recipient")
        if recipient_id is None:
            return
        
        if recipient_id == self.current_user_id:
            messagebox.showerror("Invalid Transfer", "Cannot transfer to yourself.")
            return
        
        if recipient_id not in self.bank_accounts:
            messagebox.showerror("Transfer Failed", "Recipient account not found.")
            return
        
        current_balance = self.bank_accounts[self.current_user_id]["balance"]
        recipient_name = self.bank_accounts[recipient_id]["name"]
        
        # Get transfer amount
        while True:
            amount_str = simpledialog.askstring("Transfer Amount", 
                                              f"Transfer to: {recipient_name} ({recipient_id})\n"
                                              f"Your balance: ₱{current_balance:,.2f}\n"
                                              f"Enter transfer amount (₱):")
            if amount_str is None:
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Invalid Amount", "Amount must be positive.")
                elif amount > current_balance:
                    messagebox.showerror("Insufficient Funds", 
                                       f"Insufficient balance. Available: ₱{current_balance:,.2f}")
                else:
                    # Confirm transfer
                    confirm = messagebox.askyesno("Confirm Transfer", 
                                                f"Transfer ₱{amount:,.2f} to {recipient_name}?")
                    if confirm:
                        # Process transfer
                        self.bank_accounts[self.current_user_id]["balance"] -= amount
                        self.bank_accounts[recipient_id]["balance"] += amount
                        
                        sender_balance = self.bank_accounts[self.current_user_id]["balance"]
                        recipient_balance = self.bank_accounts[recipient_id]["balance"]
                        
                        # Add transactions
                        self.add_transaction(self.current_user_id, f"Transfer to {recipient_name}", 
                                           amount, sender_balance)
                        self.add_transaction(recipient_id, f"Transfer from {self.bank_accounts[self.current_user_id]['name']}", 
                                           amount, recipient_balance)
                        
                        self.save_data()
                        
                        messagebox.showinfo("Transfer Success", 
                                          f"₱{amount:,.2f} transferred to {recipient_name}!\n"
                                          f"Your new balance: ₱{sender_balance:,.2f}")
                        
                        self.update_gui_state(logged_in=True)
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
    
    def view_history(self):
        """View transaction history"""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please log in first.")
            return
        
        transactions = self.bank_accounts[self.current_user_id].get("transactions", [])
        
        if not transactions:
            messagebox.showinfo("Transaction History", "No transactions found.")
            return
        
        # Create a new window for transaction history
        history_window = tk.Toplevel(self.root)
        history_window.title("Transaction History")
        history_window.geometry("600x400")
        
        # Create text widget with scrollbar
        frame = tk.Frame(history_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(frame, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Display transactions (most recent first)
        text_widget.insert(tk.END, "TRANSACTION HISTORY\n")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        for transaction in reversed(transactions[-20:]):  # Show last 20 transactions
            text_widget.insert(tk.END, f"Date: {transaction['date']}\n")
            text_widget.insert(tk.END, f"Type: {transaction['type']}\n")
            text_widget.insert(tk.END, f"Amount: ₱{transaction['amount']:,.2f}\n")
            text_widget.insert(tk.END, f"Balance After: ₱{transaction['balance']:,.2f}\n")
            text_widget.insert(tk.END, "-" * 30 + "\n\n")
        
        text_widget.config(state=tk.DISABLED)
    
    def view_account(self):
        """Enhanced account view"""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please log in first.")
            return
        
        acc = self.bank_accounts[self.current_user_id]
        transaction_count = len(acc.get("transactions", []))
        
        account_info = (
            f"Account Information\n"
            f"{'=' * 25}\n"
            f"Account ID: {self.current_user_id}\n"
            f"Account Holder: {acc['name']}\n"
            f"Current Balance: ₱{acc['balance']:,.2f}\n"
            f"Total Transactions: {transaction_count}"
        )
        
        messagebox.showinfo("Account Status", account_info)
    
    def show_all_accounts(self):
        """Show all accounts (admin feature)"""
        if not self.bank_accounts:
            messagebox.showinfo("All Accounts", "No accounts available.")
            return
        
        accounts_info = "All Bank Accounts\n" + "=" * 30 + "\n\n"
        
        for account_id, info in self.bank_accounts.items():
            accounts_info += f"ID: {account_id}\n"
            accounts_info += f"Name: {info['name']}\n"
            accounts_info += f"Balance: ₱{info['balance']:,.2f}\n"
            accounts_info += "-" * 20 + "\n"
        
        # Create a new window for better display
        accounts_window = tk.Toplevel(self.root)
        accounts_window.title("All Accounts")
        accounts_window.geometry("400x500")
        
        text_widget = tk.Text(accounts_window, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(accounts_window, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        text_widget.insert(tk.END, accounts_info)
        text_widget.config(state=tk.DISABLED)
    
    def register(self):
        """Enhanced registration function"""
        # Get Account ID
        while True:
            account_id = simpledialog.askstring("Register", "Enter new 4-digit Account ID:")
            if account_id is None:
                return
            
            if not self.is_valid_id(account_id):
                messagebox.showerror("Invalid ID", "ID must be a 4-digit number.")
                continue
            
            if account_id in self.bank_accounts:
                messagebox.showerror("ID Exists", "This ID already exists. Please choose another.")
                continue
            
            break
        
        # Get Name
        while True:
            name = simpledialog.askstring("Register", "Enter Account Holder's Name:")
            if name is None:
                return
            
            name = name.strip()
            if not name:
                messagebox.showerror("Invalid Name", "Name cannot be empty.")
                continue
            
            if len(name) < 2:
                messagebox.showerror("Invalid Name", "Name must be at least 2 characters.")
                continue
            
            break
        
        # Get Password
        while True:
            password = simpledialog.askstring("Register", "Enter Password (min 6 characters):", show="*")
            if password is None:
                return
            
            if len(password) < 6:
                messagebox.showerror("Weak Password", "Password must be at least 6 characters.")
                continue
            
            password_confirm = simpledialog.askstring("Register", "Confirm Password:", show="*")
            if password_confirm is None:
                return
            
            if password != password_confirm:
                messagebox.showerror("Password Mismatch", "Passwords do not match.")
                continue
            
            break
        
        # Get Initial Deposit
        while True:
            deposit_str = simpledialog.askstring("Register", "Enter Initial Deposit (₱0 or more):")
            if deposit_str is None:
                return
            
            try:
                initial_deposit = float(deposit_str)
                if initial_deposit < 0:
                    messagebox.showerror("Invalid Amount", "Initial deposit cannot be negative.")
                    continue
                break
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
        
        # Create account
        self.bank_accounts[account_id] = {
            "name": name,
            "balance": initial_deposit,
            "password": self.hash_password(password),
            "transactions": []
        }
        
        # Add initial deposit transaction if > 0
        if initial_deposit > 0:
            self.add_transaction(account_id, "Initial Deposit", initial_deposit, initial_deposit)
        
        self.save_data()
        
        messagebox.showinfo("Registration Success", 
                          f"Account {account_id} registered successfully!\n"
                          f"Account Holder: {name}\n"
                          f"Initial Balance: ₱{initial_deposit:,.2f}")
    
    def remove_account(self):
        """Enhanced account removal"""
        if not self.current_user_id:
            messagebox.showerror("Error", "Please log in first.")
            return
        
        # Security confirmation
        password = simpledialog.askstring("Confirm Identity", 
                                        "Enter your password to confirm account deletion:", 
                                        show="*")
        if password is None:
            return
        
        if self.hash_password(password) != self.bank_accounts[self.current_user_id]["password"]:
            messagebox.showerror("Authentication Failed", "Incorrect password.")
            return
        
        balance = self.bank_accounts[self.current_user_id]["balance"]
        user_name = self.bank_accounts[self.current_user_id]["name"]
        
        # Final confirmation
        confirm_msg = f"Are you sure you want to delete your account?\n\n"
        confirm_msg += f"Account: {self.current_user_id}\n"
        confirm_msg += f"Holder: {user_name}\n"
        confirm_msg += f"Balance: ₱{balance:,.2f}\n\n"
        
        if balance > 0:
            confirm_msg += "WARNING: Your remaining balance will be lost!"
        
        if not messagebox.askyesno("Final Confirmation", confirm_msg):
            return
        
        # Delete account
        del self.bank_accounts[self.current_user_id]
        self.save_data()
        
        messagebox.showinfo("Account Deleted", 
                          f"Account {self.current_user_id} has been successfully deleted.")
        
        self.current_user_id = None
        self.update_gui_state(logged_in=False)
    
    def exit_app(self):
        """Exit application with confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.save_data()  # Save data before exit
            self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = BankingSystem()
    app.run()