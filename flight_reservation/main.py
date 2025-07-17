# Add the project root directory to sys.path
import os
import sys
from mysql.connector.errors import IntegrityError
from models.flight_reservation import FlightReservation
from flightutilities import keyContinue
import pwinput
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Task 2, 5, 9: Import modules here
#may move to a seperate file
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
from sqlalchemy.dialects.mysql import insert

def login():
    connection = mysql.connector.connect(
    host="localhost",
    user="educative",
    password="secret",
    database="flight")

    username = input("Enter Username: ")
    password = pwinput.pwinput(prompt="Enter Password: ", mask="*")

    if connection.is_connected():
        mycursor = connection.cursor()
        insert_query = "SELECT * FROM account WHERE username = %s AND password = %s"
        mycursor.execute(insert_query, (username, password))
        result = mycursor.fetchone()
        if result:
            loginID = result[0]
            mycursor.execute("SELECT role_id FROM account_role WHERE account_id = %s",(loginID,))
            loginRole = mycursor.fetchall() 
            #if loginRole: may need later for when I update roles
            role_id = [row[0] for row in loginRole]
            if 1 in role_id:
                loginSuccessAdmin(username)
            else:
                loginSuccess(username)
        else:
            print("Incorrect username or password, please type 1 try again.")
                

def loginSuccess(username):
    print("Hello ", username)
    print("Please Select an Option (1-4): ")
    loginchoice = None
    reservation = FlightReservation()
    while loginchoice != '4':
        print("1. Search/Reserve Flights")
        print("2. View Reservations")
        print("3. Cancel Reservation")
        print("4. Log off")
        loginchoice = input("Make your selection now: ")
        if loginchoice == '1':
            print("Search for Flights:")
            reservation.reserveFlight(username)
            keyContinue()
        elif loginchoice == '2':
            print("Your Flight Reservations:")
            reservation.flightSearch(username)
            keyContinue()
        elif loginchoice == '3':
            print("Cancel a flight reservation?")
            reservation.flightRemove(username)
            keyContinue()
        elif loginchoice == '4':
            print("Logging off...")
            return
        else:
            print(loginchoice, "is not an option, please select options 1-6.")
            loginchoice = None

def loginSuccessAdmin(username):
    print("Hello ", username, ", (Administrator Options Available).")
    print("Please Select an Option (1-6): ")
    loginchoice = None
    reservation = FlightReservation()
    while loginchoice != '6':
        print("1. Search/Reserve Flights")
        print("2. View Reservations")
        print("3. Cancel Reservation")
        print("4. Add Flight (admin only)")
        print("5. Cancel Flight (admin only)")
        print("6. Log off")
        loginchoice = input("Make your selection now: ")
        if loginchoice == '1':
            print("Search for Flights:")
            reservation.reserveFlight(username)
            keyContinue()
        elif loginchoice == '2':
            print("Your Flight Reservations:")
            reservation.flightSearch(username)
            keyContinue()
        elif loginchoice == '3':
            print("Cancel a flight reservation?")
            reservation.flightRemove(username)
            keyContinue()
        elif loginchoice == '4':
            print("Here to add new flight.")
            reservation.adminflightadd()
            keyContinue()
        elif loginchoice == '5':
            print("Here to cancel a flight.")
            reservation.adminRemove()
            keyContinue()
        elif loginchoice == '6':
            print("Logging off...")
            return
        else:
            print(loginchoice, "is not an option, please select options 1-6.")
            loginchoice = None

def register():
    connection = mysql.connector.connect(
    host="localhost",
    user="educative",
    password="secret",
    database="flight")

    print("NEW USER REGISTRATION")
    newUsername = input("Enter new Username: ")
    newPassword = input("Enter new Password: ")


    if connection.is_connected():
        mycursor = connection.cursor()
        insert_query = "INSERT INTO account (username, password, status) VALUES (%s, %s, %s)"
        try:
            mycursor.execute(insert_query, (newUsername, newPassword, "active"))
            connection.commit()
            print("New User Registered, please login to use the database")
        except IntegrityError as e:
            if e.errno == 1062:
                print(f"Username '{newUsername}' is already taken, please type 2 enter a new one.")
            else:
                print(f"An error occurred: {e}")
        
        
        
# Task 2, 6, 10, 18: Redefine the main() function
def main():
    pass

if __name__ == "__main__":
    main()
    print("Welcome to the Airline Database Program!")
    print("Please Select an Option (1-3): ")
    choice = None
    while choice != '3':
        print("1 - Login ")
        print("2 - Register ")
        print("3 - Exit ")
        choice = input("Make your selection now: ")
        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '3':
            print("Goodbye, and thank you for using the Airline Database Program!")
        else:
            print(choice, "is not an option, please select options 1, 2, or 3.")
    
    