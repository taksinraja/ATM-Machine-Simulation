import tkinter as tk
from tkinter import messagebox, simpledialog
import pickle
# from tkinter import ttk


# Data storage
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0.00
        self.savings = 0.00
        self.transactions = []

# User Authentication
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username].password == password:
        current_user.set(username)
        main_screen()
    else:
        messagebox.showerror("Login Error", "Invalid credentials")

def register():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Registration Error", "Username and password cannot be empty")
        return

    if username in users:
        messagebox.showerror("Registration Error", "User already exists")
    else:
        users[username] = User(username, password)
        save_data()
        messagebox.showinfo("Registration Successful", "User registered successfully")

def logout():
    current_user.set("")
    login_screen()

# ATM Functionalities
def get_cash():
    user = users[current_user.get()]

    def submit_action():
        try:
            amount = float(amount_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid amount entered!")
            return

        pin = pin_entry.get()

        if pin != user.password:
            messagebox.showerror("PIN Error", "Incorrect PIN!")
            return

        if amount > user.balance:
            messagebox.showwarning("Warning", "Insufficient balance!")
        else:
            user.balance -= amount
            user.transactions.append(f"Withdrew: ₹{amount}")
            save_data()
            update_balance()
            messagebox.showinfo("Transaction Successful", f"₹{amount} withdrawn successfully!")
            cash_window.destroy()
            
    def cancel_action():
        cash_window.destroy()

    # Create a new window for the cash withdrawal
    cash_window = tk.Toplevel(window)
    cash_window.title("Withdraw Cash")
    cash_window.geometry("300x140")

    # Create and place labels and entry widgets
    tk.Label(cash_window, text="Enter amount:", font=('Arial', 12), anchor='w').grid(row=0, column=0, padx=10, pady=5, sticky='w')
    amount_entry = tk.Entry(cash_window, font=('Arial', 12))
    amount_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    tk.Label(cash_window, text="Enter PIN:", font=('Arial', 12), anchor='w').grid(row=1, column=0, padx=10, pady=5, sticky='w')
    pin_entry = tk.Entry(cash_window, font=('Arial', 12), show="*")
    pin_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

    # Create and place Confirm and Cancel buttons
    confirm_button = tk.Button(cash_window, text="Confirm", font=('Arial', 12), command=submit_action)
    confirm_button.grid(row=2, column=0, padx=10, pady=20, sticky='w')

    cancel_button = tk.Button(cash_window, text="Cancel", font=('Arial', 12), command=cancel_action)
    cancel_button.grid(row=2, column=1, padx=10, pady=20, sticky='e')

    # Adjust column weights to expand
    cash_window.grid_columnconfigure(1, weight=1)

def deposit():
    user = users[current_user.get()]
    amount = simpledialog.askfloat("Deposit", "Enter amount:")
    if amount is not None:
        user.balance += amount
        user.transactions.append(f"Deposited: ₹{amount}")
        save_data()
        update_balance()
        messagebox.showinfo("Transaction Successful", f"₹{amount} deposited successfully!")

def show_transactions():
    # Create a new window to display transactions
    transactions_window = tk.Toplevel(window)
    transactions_window.title("Transaction History")
    transactions_window.geometry("400x300")

    # Get the current user's transactions
    transactions = users[current_user.get()].transactions

    # Create a Text widget to display transactions
    transactions_text = tk.Text(transactions_window, wrap=tk.WORD, bg='white', fg='black', font=('Arial', 12))
    transactions_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Insert transactions into the Text widget
    for transaction in transactions:
        transactions_text.insert(tk.END, transaction + "\n")

    # Make the text widget read-only
    transactions_text.config(state=tk.DISABLED)

def credit_card():
    messagebox.showinfo("Credit Card", "Credit Card functionality coming soon!")

def account_settings():
    user = users[current_user.get()]
    show_edit_user_window(user)

def return_to_login():
    current_user.set("")
    login_screen()

def quick_cash():
    user = users[current_user.get()]
    amount = 500.00
    if amount > user.balance:
        messagebox.showwarning("Warning", "Insufficient balance!")
    else:
        user.balance -= amount
        user.transactions.append(f"Quick Cash: ₹{amount}")
        save_data()
        update_balance()
        messagebox.showinfo("Transaction Successful", f"₹{amount} withdrawn successfully!")

def make_clickable(widget, command):
    def on_click(event):
        command()
    widget.bind("<Button-1>", on_click)

def update_balance():
    user = users[current_user.get()]
    account_label.config(text=f"₹{user.balance:.2f}")
    savings_label.config(text=f"₹{user.savings:.2f}")

# User Details and Editing
def show_edit_user_window(user):
    def save_changes():
        new_username = username_entry.get()
        new_password = password_entry.get()

        if not new_username or not new_password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        if new_username != user.username and new_username in users:
            messagebox.showerror("Error", "Username already exists")
            return

        # Remove old user data
        del users[user.username]

        # Update user details
        user.username = new_username
        user.password = new_password
        users[new_username] = user
        save_data()
        messagebox.showinfo("Success", "User details updated successfully")
        edit_window.destroy()

    edit_window = tk.Toplevel(window)
    edit_window.title("Edit User Details")

    tk.Label(edit_window, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    username_entry = tk.Entry(edit_window)
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    username_entry.insert(0, user.username)

    tk.Label(edit_window, text="PIN").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password_entry = tk.Entry(edit_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    password_entry.insert(0, user.password)

    tk.Button(edit_window, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

# Saving and Loading Data
def save_data():
    with open("users.pkl", "wb") as f:
        pickle.dump(users, f)

def load_data():
    try:
        with open("users.pkl", "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        return {}

# User Interface
def login_screen():
    global username_entry, password_entry

    for widget in window.winfo_children():
        widget.destroy()

    frame = tk.Frame(window, bg='SystemTransparent')
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(frame, text="Name", font=('Arial', 16), bg='SystemTransparent', fg='white').grid(row=0, column=0, padx=10, pady=10, sticky="w")
    username_entry = tk.Entry(frame, font=('Arial', 16))
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="PIN", font=('Arial', 16), bg='SystemTransparent', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky="w")
    password_entry = tk.Entry(frame, font=('Arial', 16), show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # Adjust the buttons
    login_button = tk.Button(frame, text="Login", font=('Arial', 16), command=login, bg='white', bd=0)
    login_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    register_button = tk.Button(frame, text="Register", font=('Arial', 16), command=register, background='red', fg='black', bd=0)
    register_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

def main_screen():
    for widget in window.winfo_children():
        widget.destroy()

    
    # ATm
    tk.Label(window, text="Taksin's ATM", font=('Arial', 24), fg='white', bg='systemTransparent', anchor='w').place(x=20, y=20)
    
    # Welcome label
    tk.Label(window, text="Welcome", font=('Arial', 14), fg='red', bg='systemTransparent', anchor='w').place(x=20, y=100)
    tk.Label(window, text=f"{current_user.get()}", font=('Arial', 20), fg='white', bg='systemTransparent', anchor='w').place(x=20, y=120)

    # Account Balances
    global account_label, savings_label

    # Account #1 label
    tk.Label(window, text="Current Account", font=('Arial', 14), fg='red', bg='systemTransparent', anchor='w').place(x=20, y=180)
    account_label = tk.Label(window, text=f"₹{users[current_user.get()].balance:.2f}", font=('Arial', 20), fg='white', bg='systemTransparent', anchor='w')
    account_label.place(x=20, y=200)

    # Savings #2 label
    tk.Label(window, text="Savings Account", font=('Arial', 14), fg='red', bg='systemTransparent', anchor='w').place(x=20, y=260)
    savings_label = tk.Label(window, text=f"₹{users[current_user.get()].savings:.2f}", font=('Arial', 20), fg='white', bg='systemTransparent', anchor='w')
    savings_label.place(x=20, y=280)

    button_width = 200
    button_height = 60
    button_font = ('Arial', 16)

    # Buttons
    tk.Button(window, text="Get Cash", font=button_font, command=get_cash, bg='sky blue', bd=-1).place(x=200, y=100, width=button_width, height=button_height)
    tk.Button(window, text="Deposit", font=button_font, command=deposit, bg='sky blue', bd=0).place(x=420, y=100, width=button_width, height=button_height)
    tk.Button(window, text="Transactions", font=button_font, command=show_transactions, bg='sky blue', bd=0).place(x=200, y=180, width=button_width, height=button_height)
    tk.Button(window, text="Credit Card", font=button_font, command=credit_card, bg='sky blue', bd=0).place(x=420, y=180, width=button_width, height=button_height)
    tk.Button(window, text="Account Settings", font=button_font, command=account_settings, bg='sky blue', bd=0).place(x=200, y=260, width=button_width, height=button_height)
    tk.Button(window, text="Exit", font=button_font, command=return_to_login, bg='sky blue', bd=0).place(x=420, y=260, width=button_width, height=button_height)
  
    # Create a frame to hold the "$70" and "Quick Cash" labels
    quick_cash_frame = tk.Frame(window, bg='red', bd=0)
    quick_cash_frame.place(x=200, y=380, width=420, height=45)

    # Create and place the "$500" label
    dollar_label = tk.Label(quick_cash_frame, text="₹500", font=('Arial', 22, 'bold'), bg='red', fg='white')
    dollar_label.pack(side=tk.LEFT, padx=(60, 40))  # Adjust padx for the desired gap

    # Create and place the "Quick Cash" label
    quick_cash_label = tk.Label(quick_cash_frame, text="Quick Cash", font=('Arial', 16), bg='red', fg='white')
    quick_cash_label.pack(side=tk.RIGHT, padx=(30, 60))  # Adjust padx for the desired gap

    # Make labels clickable
    make_clickable(quick_cash_frame, quick_cash)
    # make_clickable(quick_cash_label, quick_cash)
    
    

if __name__ == "__main__":
    window = tk.Tk()
    window.title("ATM")
    window.geometry("660x450")
    window.configure(bg='systemTransparent')
    
    title_bar_icon = tk.PhotoImage(file="app-icon.png")
    window.iconphoto(False,title_bar_icon)


    users = load_data()
    current_user = tk.StringVar()

    login_screen()
    window.mainloop()
