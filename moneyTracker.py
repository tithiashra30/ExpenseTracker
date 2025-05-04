#Projectt Title : Money Tracker
#Enrollment No. : 23002171210010
#Subject name : Python
#Date : 28-02-25


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
from datetime import datetime

class MoneyTracker:
    def __init__(self, root):
        self.expenses = []
        self.root = root
        self.root.title("Expense Tracker")
        
        # Load expenses from file if available
        self.load_expenses()
        
        # Set up labels and entries
        self.label_description = tk.Label(self.root, text="Description:")
        self.label_description.grid(row=0, column=0)
        self.entry_description = tk.Entry(self.root)
        self.entry_description.grid(row=0, column=1)

        self.label_amount = tk.Label(self.root, text="Amount:")
        self.label_amount.grid(row=1, column=0)
        self.entry_amount = tk.Entry(self.root)
        self.entry_amount.grid(row=1, column=1)

        self.label_category = tk.Label(self.root, text="Category:")
        self.label_category.grid(row=2, column=0)
        self.category_var = tk.StringVar()
        self.category_menu = tk.OptionMenu(self.root, self.category_var, "Food", "Transport", "Entertainment", "Others")
        self.category_menu.grid(row=2, column=1)

        self.label_date = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.label_date.grid(row=3, column=0)
        self.entry_date = tk.Entry(self.root)
        self.entry_date.grid(row=3, column=1)
        
        # Search Section
        self.label_search = tk.Label(self.root, text="Search:")
        self.label_search.grid(row=4, column=0)
        self.search_var = tk.StringVar()
        self.entry_search = tk.Entry(self.root, textvariable=self.search_var)
        self.entry_search.grid(row=4, column=1)
        self.button_search = tk.Button(self.root, text="Search", command=self.search_expenses)
        self.button_search.grid(row=4, column=2)

        # Buttons
        self.button_add = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.button_add.grid(row=5, column=0, columnspan=2)

        self.button_edit = tk.Button(self.root, text="Edit Selected Expense", command=self.edit_expense)
        self.button_edit.grid(row=6, column=0, columnspan=2)

        self.button_delete = tk.Button(self.root, text="Delete Selected Expense", command=self.delete_expense)
        self.button_delete.grid(row=7, column=0, columnspan=2)

        self.button_calculate = tk.Button(self.root, text="Calculate Total", command=self.calculate_total)
        self.button_calculate.grid(row=8, column=0, columnspan=2)

        self.button_sort = tk.Button(self.root, text="Sort by Amount", command=self.sort_expenses)
        self.button_sort.grid(row=9, column=0, columnspan=2)

        # Set up the treeview to display expenses
        self.columns = ("Description", "Amount", "Category", "Date")
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings")
        self.tree.grid(row=11, column=0, columnspan=2)

        for col in self.columns:
            self.tree.heading(col, text=col)

        # Display existing expenses if any
        self.display_expenses()

    def add_expense(self):
        description = self.entry_description.get()
        amount = self.entry_amount.get()
        category = self.category_var.get()
        date = self.entry_date.get()

        if description == "" or amount == "" or category == "" or date == "":
            messagebox.showwarning("Input Error", "Please fill out all fields.")
        else:
            # Add expense to the list
            self.expenses.append({
                "description": description,
                "amount": float(amount),
                "category": category,
                "date": date
            })
            messagebox.showinfo("Success", "Expense added successfully!")
            self.clear_fields()
            self.display_expenses()
            self.save_expenses()

    def clear_fields(self):
        self.entry_description.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        
    def search_expenses(self):
        search_query = self.search_var.get().lower()
        filtered_expenses = [expense for expense in self.expenses if search_query in expense["description"].lower() or search_query in expense["category"].lower() or search_query in str(expense["amount"])]
        self.display_expenses(filtered_expenses)

    def display_expenses(self,expenses=None):   
        # Clear the existing entries in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Use the filtered expenses if provided, otherwise display all expenses
        expenses_to_display = expenses if expenses is not None else self.expenses

        # Insert all expenses from the list into the treeview
        for expense in expenses_to_display:
            self.tree.insert("", tk.END, values=(expense["description"], expense["amount"], expense["category"], expense["date"]))

    def delete_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            description = values[0]
            # Find and remove the selected expense from the list
            self.expenses = [expense for expense in self.expenses if expense["description"] != description]
            messagebox.showinfo("Deleted", "Expense deleted successfully!")
            self.display_expenses()
            self.save_expenses()
        else:
            messagebox.showwarning("Selection Error", "Please select an expense to delete.")

    def edit_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            description = values[0]
            # Find and edit the selected expense
            for expense in self.expenses:
                if expense["description"] == description:
                    expense["description"] = self.entry_description.get()
                    expense["amount"] = float(self.entry_amount.get())
                    expense["category"] = self.category_var.get()
                    expense["date"] = self.entry_date.get()
                    break
            messagebox.showinfo("Success", "Expense updated successfully!")
            self.display_expenses()
            self.save_expenses()
        else:
            messagebox.showwarning("Selection Error", "Please select an expense to edit.")

    def calculate_total(self):
        total = sum(expense["amount"] for expense in self.expenses)
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total:.2f}")

    def sort_expenses(self):
        self.expenses.sort(key=lambda x: x["amount"])  # Sort by amount
        self.display_expenses()

    def load_expenses(self):
        try:
            with open('expenses.json', 'r') as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            self.expenses = []

    def save_expenses(self):
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file)

# Set up the Tkinter root window
root = tk.Tk()
# Create the ExpenseTracker object
expense_tracker = MoneyTracker(root)
# Run the Tkinter main loop
root.mainloop()