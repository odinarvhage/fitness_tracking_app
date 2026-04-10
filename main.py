import streamlit as st
import mysql.connector

#Change the host to the IP address when we use a remote server.
connection = mysql.connector.connect(host="localhost",user="root", password="",database="test")

#Closes the connection once the program exits.
connection.close()

