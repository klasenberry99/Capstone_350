import pandas as pd
import mysql.connector
import os
import time
from datetime import datetime
import pymysql

# get_str_input(info, length) - prompts the user to enter a string of specified length.
# The isalnum() method returns True if a character is an alphabetic or numeric.     
       
def get_str_input(info, length):
    while True:
        user_input = input(f"Enter {info}:  ")
        if len(user_input) == length and all(char.isalnum() for char in user_input):
            return user_input
        else:
            print(f"Invalid {info}! Please enter a {length}-character alphanumeric string.")
            
def get_month():
    while True:
        user_input = input("Enter Numeric Month:  ")
        try:
            month_number = int(user_input)
            if 1 <= month_number <= 12:
                return str(month_number)
            else:
                print("Invalid Month Number! Please enter a number from 1 to 12.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

def get_trans_type():
    os.system('cls')
    user_input = ""
    while user_input != "q":
        print("*****  Select Transaction Type  *****\n\n")
       
        user_input = input("Select From following Transaction Types:\n" +
                           "1) EDUCATION\n" +
                           "2) ENTERTAINMENT\n" +
                           "3) GROCERY\n" +
                           "4) GAS\n" +
                           "5) BILLS\n" +
                           "6) TEST\n" +
                           "7) HEALTHCARE\n" +
                           "q) QUIT\n\n\n>> ")
        match user_input:
            case "1":
                user_input = "Education" 

            case "2":
                user_input = "Entertainment"

            case "3":
                user_input = "Grocery"

            case "4":
                user_input = "Gas" 
                
            case "5":
                user_input = "Bills" 

            case "6":
                user_input = "Test" 

            case "7":
                user_input =  "Healthcare"

            case "q":
                user_input = 'q'

            case _:
                os.system('cls')
                print(f"'{user_input}' is NOT a correct option. \nSelect options 1-7 or (q)uit: ")
                continue
        return user_input
            
def query_db(query):
    try:
        user = "root"
        password = "password"
        host = "localhost"
        port = 3306
        database = "creditcard_capstone"
        
        # Establish a connection to MySQL database
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(query)

        # Fetch the result into a Pandas DataFrame
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=[i[0] for i in cursor.description])
                # Close the cursor and the database connection
        cursor.close()
        connection.close()

        if not df.empty:
            return df
        else:
            print("EMPTY DATAFRAME")

    except Exception as e:
        
        print(f"ERROR connecting to Local database: {e}")
        
def main():
    os.system('cls')
    # Display menu
    user_input = ""
    while user_input != "q":
        
        print("******** CREDIT CARD CONSOLE ********")
   

        user_input = input("Select from the following options:\n" +
                           "1) Retrieve transactions for customer given zipcode, month, and year\n" +
                           "2) Retrieve total transactions for a given type\n" +
                           "3) Retrieve total number and values of branch transactions in a given state\n" +
                           "4) Retrieve account details of a given customer\n" +
                           #"5) Modify the account details of a customer\n" +
                           #"6) Produce a monthly bill for a credit card number for a given month and year\n" +
                           #"7) Display the transactions made by a customer between two dates\n" +
                           "q) quit\n\n>>  ")
        match user_input:
            
            case '1':
                zipcode = get_str_input('Zipcode', 5)
                year = get_str_input('Year', 4)
                month = get_month()
                print(f"Retrieving transactions for {month}/{year} in zipcode {zipcode}")
        
                query_db(f"SELECT TIMEID, TRANSACTION_ID, c.first_name, c.last_name, cust_city, \
                                cust_state, cust_zip, TRANSACTION_TYPE, TRANSACTION_VALUE\
                            FROM cdw_sapp_credit_card cc \
                            JOIN cdw_sapp_customer c \
                                ON cc.cust_ssn = c.ssn \
                            WHERE c.cust_zip = {zipcode} \
                            AND substr(TIMEID, 1, 4) = {year} \
                            AND substr(TIMEID, 5, 2) = {month} \
                            ORDER BY substr(TIMEID, 7, 2) DESC")
                        # display the number and total values of transactions for a given type.
            case '2':
                trans_type = get_trans_type()
                if trans_type == 'q':
                    continue
                
                query_db(f"SELECT Transaction_Type, count(*) Transaction_Count, sum(transaction_value) Transaction_Total \
                            FROM cdw_sapp_credit_card \
                            WHERE transaction_type = '{trans_type}' \
                            GROUP BY transaction_type")
                
                         # display the total number and total values of transactions for branches in a given state.
            case '3':
                state = get_str_input('State', 2)
                os.system('cls')
           
                print(f"TOTAL TRANSACTIONS FOR {state}")
    
                query_db(f"SELECT Branch_State, count(branch_state) Total_Transactions, sum(cc.transaction_value) Total_Value \
                            FROM cdw_sapp_branch b \
                            JOIN cdw_sapp_credit_card cc \
                                ON b.branch_code = cc.BRANCH_CODE \
                            WHERE b.branch_state = '{state}' \
                            GROUP BY branch_state")

                print(f"TOTAL FOR EACH BRANCH IN {state}")
          
                query_db(f"SELECT b.branch_code, Branch_State , count(branch_state) Total_Transactions, sum(cc.transaction_value) Total_Value \
                            FROM cdw_sapp_branch b \
                            JOIN cdw_sapp_credit_card cc \
                                ON b.branch_code = cc.BRANCH_CODE \
                            WHERE b.branch_state = '{state}' \
                            GROUP BY branch_code, branch_state")
                
                            # check the existing account details of a customer
            case '4':
                ssn = get_str_input('SSN', 9)
                query_db(f"SELECT * \
                            FROM cdw_sapp_customer c \
                            WHERE SSN = {ssn}", transpose=True)
            case 'q':
                user_input = 'q'
                
            case _:
                print("Invalid choice. Pls try again.")
                
main()
                
                