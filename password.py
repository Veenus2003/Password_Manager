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