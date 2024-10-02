import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Inventory dictionary to store items
inventory = {}

# Function to check stock availability
def check_stock(quantity):
    if quantity < 50:
        return 'LOW IN STOCK'
    elif quantity >= 60:
        return 'IN STOCK'
    else:
        return 'Moderate Stock'

# Function to validate form input
def validate_form():
    if not item_name_entry.get() or not item_quantity_entry.get() or not item_price_entry.get():
        messagebox.showerror("Form Error", "Please fill all fields before submitting.")
        return False
    try:
        int(item_quantity_entry.get())
        float(item_price_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Quantity must be an integer and price must be a valid number.")
        return False
    return True

# Function to add or update an item
def add_item():
    if not validate_form():
        return
    
    name = item_name_entry.get()
    quantity = int(item_quantity_entry.get())
    price = float(item_price_entry.get())
    
    if name in inventory:
        # Update existing item
        inventory[name]['quantity'] += quantity
        inventory[name]['price'] = price
        messagebox.showinfo("Updated", f"{name} updated. New quantity: {inventory[name]['quantity']}, Price: {inventory[name]['price']}")
    else:
        # Add new item
        inventory[name] = {'quantity': quantity, 'price': price}
        messagebox.showinfo("Added", f"{name} added to inventory.")
    
    clear_form()
    update_inventory_list()

# Function to update the price of an existing item
def update_price():
    if not validate_form():
        return
    
    name = item_name_entry.get()
    new_price = float(item_price_entry.get())
    
    if name in inventory:
        inventory[name]['price'] = new_price
        messagebox.showinfo("Updated", f"{name}'s price updated to {new_price}")
    else:
        messagebox.showerror("Not Found", f"{name} is not in the inventory.")
    
    clear_form()
    update_inventory_list()

# Function to remove an item
def remove_item():
    name = item_name_entry.get()
    
    if name in inventory:
        del inventory[name]
        messagebox.showinfo("Removed", f"{name} removed from inventory.")
    else:
        messagebox.showerror("Not Found", f"{name} is not in the inventory.")
    
    clear_form()
    update_inventory_list()

# Function to generate and display the inventory report in a new window
def generate_report():
    report_window = tk.Toplevel(root)
    report_window.title("Inventory Report")
    
    report = tk.Text(report_window, wrap=tk.NONE, height=20, width=80)
    report.pack(expand=True, fill="both")
    
    report.insert(tk.END, "Inventory Report:\n")
    report.insert(tk.END, "Name\t\tQuantity\tPrice\tTotal Value\tStock Status\n")
    report.insert(tk.END, "-"*60 + "\n")
    
    for name, details in inventory.items():
        total_value = details['quantity'] * details['price']
        stock_status = check_stock(details['quantity'])
        report.insert(tk.END, f"{name}\t\t{details['quantity']}\t{details['price']}\t{total_value}\t{stock_status}\n")

    # Make the report read-only
    report.config(state=tk.DISABLED)

# Function to search for an item by name
def search_item():
    name = item_name_entry.get()
    
    if name in inventory:
        details = inventory[name]
        stock_status = check_stock(details['quantity'])
        messagebox.showinfo("Item Found", f"Name: {name}\nQuantity: {details['quantity']}\nPrice: {details['price']}\nStock Status: {stock_status}")
    else:
        messagebox.showerror("Not Found", f"{name} is not in the inventory.")
    
    clear_form()

# Function to clear the form fields
def clear_form():
    item_name_entry.delete(0, tk.END)
    item_quantity_entry.delete(0, tk.END)
    item_price_entry.delete(0, tk.END)

# Function to update the listbox with current inventory
def update_inventory_list():
    inventory_listbox.delete(0, tk.END)
    for name, details in inventory.items():
        inventory_listbox.insert(tk.END, f"{name} - Quantity: {details['quantity']}, Price: {details['price']}")

# Function to switch between different frames
def show_frame(frame):
    frame.tkraise()

# Main GUI
root = tk.Tk()
root.title("Hannah's Store")

# Set window size and position
root.geometry("900x500")
root.configure(bg="#F3F4F6")

# Frames for layout
sidebar_frame = tk.Frame(root, bg="#2C3E50", width=200, height=500)
sidebar_frame.grid(row=0, column=0, sticky="ns")

main_frame = tk.Frame(root, bg="#ECF0F1", width=600, height=500)
main_frame.grid(row=0, column=1, sticky="nsew")

# Create different frames for dynamic content
add_item_frame = tk.Frame(main_frame, bg="#ECF0F1")
search_item_frame = tk.Frame(main_frame, bg="#ECF0F1")
report_frame = tk.Frame(main_frame, bg="#ECF0F1")

for frame in (add_item_frame, search_item_frame, report_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# Sidebar Buttons
tk.Button(sidebar_frame, text="Add Item", bg="#2980B9", fg="white", font=("Arial", 12), command=lambda: show_frame(add_item_frame)).pack(pady=20, fill="x")
tk.Button(sidebar_frame, text="Search Item", bg="#2980B9", fg="white", font=("Arial", 12), command=lambda: show_frame(search_item_frame)).pack(pady=20, fill="x")
tk.Button(sidebar_frame, text="Generate Report", bg="#2980B9", fg="white", font=("Arial", 12), command=generate_report).pack(pady=20, fill="x")

# Add Item Frame Content
tk.Label(add_item_frame, text="Add New Item", bg="#ECF0F1", font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=20)

tk.Label(add_item_frame, text="Item Name:", bg="#ECF0F1", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, padx=20)
item_name_entry = tk.Entry(add_item_frame, width=30)
item_name_entry.grid(row=1, column=1, padx=20)

tk.Label(add_item_frame, text="Quantity:", bg="#ECF0F1", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, padx=20)
item_quantity_entry = tk.Entry(add_item_frame, width=30)
item_quantity_entry.grid(row=2, column=1, padx=20)

tk.Label(add_item_frame, text="Price:", bg="#ECF0F1", font=("Arial", 12)).grid(row=3, column=0, sticky=tk.W, padx=20)
item_price_entry = tk.Entry(add_item_frame, width=30)
item_price_entry.grid(row=3, column=1, padx=20)

# Buttons in Add Item Frame
tk.Button(add_item_frame, text="Add Item", bg="#27AE60", fg="white", font=("Arial", 12), command=add_item).grid(row=4, column=1, padx=20, pady=10, sticky=tk.E)
tk.Button(add_item_frame, text="Update Price", bg="#F39C12", fg="white", font=("Arial", 12), command=update_price).grid(row=5, column=1, padx=20, pady=10, sticky=tk.E)
tk.Button(add_item_frame, text="Remove Item", bg="#C0392B", fg="white", font=("Arial", 12), command=remove_item).grid(row=6, column=1, padx=20, pady=10, sticky=tk.E)

# Search Item Frame Content
tk.Label(search_item_frame, text="Search Item", bg="#ECF0F1", font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=20)

tk.Label(search_item_frame, text="Item Name:", bg="#ECF0F1", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, padx=20)
search_name_entry = tk.Entry(search_item_frame, width=30)
search_name_entry.grid(row=1, column=1, padx=20)

tk.Button(search_item_frame, text="Search", bg="#2980B9", fg="white", font=("Arial", 12), command=search_item).grid(row=2, column=1, padx=20, pady=20, sticky=tk.E)

# Inventory List
inventory_listbox = tk.Listbox(main_frame, height=15, width=50)
inventory_listbox.grid(row=0, column=0, pady=10)

show_frame(add_item_frame)

root.mainloop()
