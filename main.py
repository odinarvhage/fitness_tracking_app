import streamlit as st
import mysql.connector

#Change the host to the IP address when we use a remote server.
connection = mysql.connector.connect(host="localhost",user="root", password="",database="test")

#Function for the Create part of CRUD
def create_entry():
    pass

#Function for the Read part of CRUD
def read_entry():
    pass

#Function for the Update part of CRUD
def update_entry():
    pass

#Function for the Delete part of CRUD
def delete_entry():
    pass

#Closes the connection once the program exits.
connection.close()

