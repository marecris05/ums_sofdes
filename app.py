from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import time

con = None
mycursor = None

def connect_database():
    global con, mycursor
    try:
        con = pymysql.connect(host='localhost', user='root', password='1234', database='ums')
        mycursor = con.cursor()
        mycursor.execute("""CREATE TABLE IF NOT EXISTS user (
                            ID INT AUTO_INCREMENT PRIMARY KEY,
                            Name VARCHAR(50),
                            Phone VARCHAR(15),
                            Email VARCHAR(50),
                            Address VARCHAR(100),
                            Gender VARCHAR(10),
                            DOB VARCHAR(15),
                            Date VARCHAR(15),
                            Time VARCHAR(15))""")
        con.commit()
        messagebox.showinfo('Success', 'Database Connected Successfully')
        enable_buttons()
    except Exception as e:
        messagebox.showerror('Error', f'Database Connection Failed: {str(e)}')

def enable_buttons():
    add_button.config(state=NORMAL)
    delete_button.config(state=NORMAL)
    edit_button.config(state=NORMAL)
    show_users_button.config(state=NORMAL)

def add_user():
    try:
        if name_var.get() == "" or phone_var.get() == "":
            messagebox.showerror("Error", "Name and Phone are required")
            return
        query = "INSERT INTO user (Name, Phone, Email, Address, Gender, DOB, Date, Time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(query, (name_var.get(), phone_var.get(), email_var.get(), address_var.get(),
                                 gender_var.get(), dob_var.get(), time.strftime('%d/%m/%Y'), time.strftime('%H:%M:%S')))
        con.commit()
        messagebox.showinfo('Success', 'User Added Successfully')
        clear_entries()
        show_users()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to Add User: {str(e)}")

def show_users():
    try:
        user_table.delete(*user_table.get_children())
        query = "SELECT * FROM user"
        mycursor.execute(query)
        rows = mycursor.fetchall()
        for row in rows:
            user_table.insert('', END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to Fetch Data: {str(e)}")

def edit_user():
    selected_item = user_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "No User Selected")
        return

    user_data = user_table.item(selected_item)['values']
    if not user_data:
        messagebox.showerror("Error", "Failed to retrieve user data")
        return

    name_var.set(user_data[1])
    phone_var.set(user_data[2])
    email_var.set(user_data[3])
    address_var.set(user_data[4])
    gender_var.set(user_data[5])
    dob_var.set(user_data[6])

    def save_changes():
        try:
            query = """UPDATE user SET Name=%s, Phone=%s, Email=%s, Address=%s, Gender=%s, DOB=%s WHERE ID=%s"""
            mycursor.execute(query, (name_var.get(), phone_var.get(), email_var.get(),
                                     address_var.get(), gender_var.get(), dob_var.get(), user_data[0]))
            con.commit()
            messagebox.showinfo("Success", "User Updated Successfully")
            clear_entries()
            show_users()
            add_button.config(text="Add User", command=add_user)  # Reset the button
        except Exception as e:
            messagebox.showerror("Error", f"Failed to Update User: {str(e)}")

    add_button.config(text="Save Changes", command=save_changes)

def delete_user():
    selected_item = user_table.focus()
    if not selected_item:
        messagebox.showerror("Error", "No User Selected")
        return
    try:
        user_id = user_table.item(selected_item)['values'][0]
        query = "DELETE FROM user WHERE ID=%s"
        mycursor.execute(query, (user_id,))
        con.commit()
        messagebox.showinfo('Success', 'User Deleted Successfully')
        show_users()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to Delete User: {str(e)}")

def clear_entries():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    address_var.set("")
    gender_var.set("")
    dob_var.set("")

root = Tk()
root.title("User Management System")
root.geometry("900x500")


name_var = StringVar()
phone_var = StringVar()
email_var = StringVar()
address_var = StringVar()
gender_var = StringVar()
dob_var = StringVar()


Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky=W)
Entry(root, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Phone:").grid(row=1, column=0, padx=10, pady=10, sticky=W)
Entry(root, textvariable=phone_var).grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky=W)
Entry(root, textvariable=email_var).grid(row=2, column=1, padx=10, pady=10)

Label(root, text="Address:").grid(row=3, column=0, padx=10, pady=10, sticky=W)
Entry(root, textvariable=address_var).grid(row=3, column=1, padx=10, pady=10)

Label(root, text="Gender:").grid(row=4, column=0, padx=10, pady=10, sticky=W)
Entry(root, textvariable=gender_var).grid(row=4, column=1, padx=10, pady=10)

Label(root, text="DOB:").grid(row=5, column=0, padx=10, pady=10, sticky=W)
Entry(root, textvariable=dob_var).grid(row=5, column=1, padx=10, pady=10)

# Buttons
connect_button = Button(root, text="Connect to Database", command=connect_database)
connect_button.grid(row=6, column=0, padx=10, pady=20)

add_button = Button(root, text="Add", command=add_user, state=DISABLED)
add_button.grid(row=6, column=1, padx=10, pady=20)

delete_button = Button(root, text="Delete", command=delete_user, state=DISABLED)
delete_button.grid(row=6, column=2, padx=10, pady=20)

edit_button = Button(root, text="Edit", command=edit_user, state=DISABLED)
edit_button.grid(row=6, column=3, padx=10, pady=20)

show_users_button = Button(root, text="Show List", command=show_users, state=DISABLED)
show_users_button.grid(row=6, column=4, padx=10, pady=20)

columns = ('ID', 'Name', 'Phone', 'Email', 'Address', 'Gender', 'DOB', 'Date', 'Time')
user_table = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    user_table.heading(col, text=col)
    user_table.column(col, width=100)
user_table.grid(row=7, column=0, columnspan=6, padx=10, pady=10)

root.mainloop()

