from tkinter import *
from tkinter import messagebox
import mysql.connector
conn = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="password",
    database="password_manager"
)
mycursor = conn.cursor()
alter_query = """
ALTER TABLE passwords MODIFY COLUMN user_id INT AUTO_INCREMENT PRIMARY KEY;
"""
class PasswordManager:

    def __init__(self, master):
        self.master = master
        master.geometry("700x700")
        master.title(" Password Manager")
        master.configure(bg="#cfe8b5")
        # Username block
        self.labelName = Label(master, text="USERNAME",bg="#cfe8b5",fg="BLACK")
        self.labelName.grid(row=0, column=0, padx=15, pady=15)
        self.entryName = Entry(master)
        self.entryName.grid(row=0, column=1, padx=15, pady=15)

        # Password block
        self.labelPassword = Label(master, text="PASSWORD",bg="#cfe8b5",fg="BLACK")
        self.labelPassword.grid(row=1, column=0, padx=10, pady=5)
        self.entryPassword = Entry(master)
        self.entryPassword.grid(row=1, column=1, padx=10, pady=5)
        
        # Add button
        self.buttonAdd = Button(master, text="Add", command=self.add)
        self.buttonAdd.grid(row=2, column=0, padx=15, pady=8, sticky="we")

        # Get button
        self.buttonGet = Button(master, text="Get", command=self.get)
        self.buttonGet.grid(row=2, column=1, padx=15, pady=8, sticky="we")

        # List Button
        self.buttonList = Button(master, text="List", command=self.get_list)
        self.buttonList.grid(row=3, column=0, padx=15, pady=8, sticky="we")

        # Delete button
        self.buttonDelete = Button(master, text="Delete", command=self.delete)
        self.buttonDelete.grid(row=3, column=1, padx=15, pady=8, sticky="we")

        #clear
        self.buttonClear = Button(master, text="Clear", command=self.clear)
        self.buttonClear.grid(row=4, column=1, padx=15, pady=8, sticky="we")

        self.buttonUpdate = Button(master, text="Update", command=self.update)
        self.buttonUpdate.grid(row=4, column=0, padx=15, pady=8, sticky="we")

        self.tbBox = Text(master, width=50, height=20)
        self.tbBox.grid(row=5,column=1)
        self.user_id=1

    def clear(self):
        self.entryPassword.delete(0,END)
        self.entryName.delete(0,END)
        self.tbBox.delete(1.0,"end")


    def add(self,event=None):
        username = self.entryName.get()
        password = self.entryPassword.get()
        if username and password:
            with open("passwords.txt", 'a') as f:
                f.write(f"{username} {password}\n")
            try:
                mycursor.execute("INSERT INTO passwords(username,password) VALUES (%s,%s)",(username,password))
                conn.commit()
                messagebox.showinfo("Success", "Password added !!")
            except mysql.connector.Error as err:
                conn.rollback()  # Rollback the changes if an error occurs
                messagebox.showerror("Error", f"MySQL Error: {err}")
            
        else:
            messagebox.showerror("Error", "Please enter both the fields")

    def get(self):
        username = self.entryName.get()
        passwords = {}
        try:
            with open("passwords.txt", 'r') as f:
                for line in f:
                    data = line.split(' ')
                    passwords[data[0]] = data[1]
        except Exception as e:
            print(f"Error: {e}")

        if passwords:
            if username in passwords:
                messagebox.showinfo("Password", f"Password for {username} is {passwords[username]}")
            else:
                messagebox.showinfo("Password", "No Such Username Exists !!")
        else:
            messagebox.showinfo("Passwords", "EMPTY LIST!!")
    def get_list(self):
        passwords = {}
        try:
            with open("passwords.txt", 'r') as f:
                for line in f:
                    data = line.split(' ')
                    passwords[data[0]] = data[1]
        except Exception as e:
            print(f"Error: {e}")

        if passwords:
            mess = " \n"
            for name, password in passwords.items():
                mess += f"Username: {name} Password: {password}\n"
            #messagebox.showinfo("Passwords", mess)
            self.tbBox.insert(END,mess)

        else:
            messagebox.showinfo("Passwords", "Empty List !!")

    def delete(self):
        username = self.entryName.get()
        passwords = {}
        try:
            with open("passwords.txt", 'r') as f:
                for line in f:
                    data = line.split(' ')
                    passwords[data[0]] = data[1]
        except Exception as e:
            print(f"Error: {e}")
        if username in passwords:
            try:
                mycursor.execute("DELETE FROM passwords WHERE username =%s",(username,))
                conn.commit()
            except mysql.connector.Error as err:
                conn.rollback()
            
            temp_passwords = []
            try:
                with open("passwords.txt", 'r') as f:
                    for line in f:
                       data = line.split(' ')
                       if data[0] != username:
                            temp_passwords.append(f"{data[0]} {data[1]}")

                with open("passwords.txt", 'w') as f:
                    for line in temp_passwords:
                        f.write(line)
            
                messagebox.showinfo("Success", f"User {username} deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting user {username}: {e}")
        else:
            messagebox.showerror("error","username doesnot exist")
        
    def update(self):
        username = self.entryName.get()
        password = self.entryPassword.get()
        passwords = {}
        try:
            with open("passwords.txt", 'r') as f:
                for line in f:
                    data = line.strip().split(' ')
                    passwords[data[0]] = data[1]
        
            if username in passwords:
                    try:
                        mycursor.execute("UPDATE passwords SET password = %s WHERE username=%s",(password,username))
                        conn.commit()
                    except Exception as e:
                        messagebox.showerror("Error", f"Error during update: {str(e)}")
                    passwords[username] = password
                    
                    with open("passwords.txt", 'w') as f:
                        for name, pwd in passwords.items():
                            f.write(f"{name} {pwd}\n")
                
                    messagebox.showinfo("Success", "Password updated successfully")
            else:
                messagebox.showerror("Error", "Username does not exist")
        except Exception as e:
                messagebox.showerror("Error", f"Error updating password: {e}")

root = Tk()
app = PasswordManager(root)
root.mainloop()
