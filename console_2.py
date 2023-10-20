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
       
        selected_type = input("Select From following Transaction Types:\n" +
                           "1) EDUCATION\n" +
                           "2) ENTERTAINMENT\n" +
                           "3) GROCERY\n" +
                           "4) GAS\n" +
                           "5) BILLS\n" +
                           "6) TEST\n" +
                           "7) HEALTHCARE\n" +
                           "q) QUIT\n\n\n>> ")
        match selected_type:
            case "1":
                selected_type = "Education" 

            case "2":
                selected_type = "Entertainment"

            case "3":
                selected_type = "Grocery"

            case "4":
                selected_type = "Gas" 
                
            case "5":
                selected_type = "Bills" 

            case "6":
                selected_type = "Test" 

            case "7":
                selected_type =  "Healthcare"

            case "q":
                selected_type = 'q'

            case _:
                os.system('cls')
                print(f"'{user_input}' is NOT a correct option. \nSelect options 1-7 or (q)uit: ")
                continue
            
        return selected_type
            
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
        
import os
import pymysql

def update_cust_db(ssn):
    os.system('cls')
    user_input = ""
    while user_input != 'q':
        os.system('cls')
        results = query_db(f"SELECT first_name, middle_name, last_name, credit_card_no, full_street_address, \
                        cust_city, cust_state, cust_country, cust_zip, cust_phone, cust_email \
                        FROM cdw_sapp_customer \
                        WHERE ssn = {ssn}")
        os.system('cls')
        print("****** Select item number to modify or (q)uit ******\n")
        
        user_input = input("Select From following Transaction Types:\n" +
                           "1)  First Name\n" +
                           "2)  Middle Name\n" +
                           "3)  Last Name\n" +
                           "4)  Credit Card Number\n" +  # Added missing '\n' here
                           "5)  Street Address\n" +
                           "6)  City\n" +
                           "7)  State\n" +
                           "8)  Country\n" +
                           "9)  Phone Number\n" +
                           "10) Email\n" +
                           "q)  QUIT\n\n\n>> ")
        match user_input:
            case "1":
                col_name = "first_name"
            case "2":
                col_name = "middle_name"
            case "3":
                col_name = "last_name"
            case "4":
                col_name = "credit_card_no"
            case "5":
                col_name = "full_street_address"
            case "6":
                col_name = "cust_city"
            case "7":
                col_name = "cust_state"
            case "8":
                col_name = "cust_country"
            case "9":
                col_name = "cust_phone"
            case "10":
                col_name = "cust_email"
            case "q":
                user_input = 'q'
            case _:
                os.system('cls')
                print(f"'{user_input}' is NOT a correct option. \nSelect options 1-10 or (q)uit: ")
                continue

        # Check if user_input is in range
        if user_input.isdigit():
            user_input = int(user_input)
            if not 1 <= user_input <= 10:
                print("Selection not in range 1-10")
                user_input = ""
                continue
            
        else:  
            if user_input == 'q':
             print("\n\n\n")
             break
        
            else:
                print("Invalid input. Please enter a number between 1 and 10.")
                continue

        new_item = input(f"| {user_input} | {col_name} |  ")
        if new_item == 'q':
            break
        
        # Connect to the database and update the selected column
        try:
            user = "root"
            password = "password"
            host = "localhost"
            port = 3306
            database = "creditcard_capstone"
            
            # Create query statement
            query = f"UPDATE cdw_sapp_customer \
                     SET {col_name} = '{new_item}', \
                     last_updated = CURRENT_TIMESTAMP \
                     WHERE ssn = {ssn}"
        
            # Establish a connection to the MySQL database
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

        except Exception as e:
            print("There was an error:", e)

        finally:
            connection.commit()
            cursor.close()
            connection.close()
        
    # Clear screen because exiting this function (update_cust_db)
    print("update completed successfully")
    os.system('cls')

          
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
                           "5) Modify the account details of a customer\n" +
                           #"6) Produce a monthly bill for a credit card number for a given month and year\n" +
                           #"7) Display the transactions made by a customer between two dates\n" +
                           "q) quit\n\n>>  ")
        match user_input:
            
            case '1':
                zipcode = get_str_input('Zipcode', 5)
                year = get_str_input('Year', 4)
                month = get_month()
                print(f"Retrieving transactions for {month}/{year} in zipcode {zipcode}\n\n")
        
                cust_transx=query_db(f"SELECT TIMEID, TRANSACTION_ID, c.first_name, c.last_name, cust_city, \
                                cust_state, cust_zip, TRANSACTION_TYPE, TRANSACTION_VALUE\
                            FROM cdw_sapp_credit_card cc \
                            JOIN cdw_sapp_customer c \
                                ON cc.cust_ssn = c.ssn \
                            WHERE c.cust_zip = {zipcode} \
                            AND substr(TIMEID, 1, 4) = {year} \
                            AND substr(TIMEID, 5, 2) = {month} \
                            ORDER BY substr(TIMEID, 7, 2) DESC")
                
                        # display the number and total values of transactions for a given type.
                
                if not cust_transx.empty:
                    # Display the result in a formatted table
                    print("\n|   TIMEID   | TRANSACTION_ID | FIRST NAME | LAST NAME | CITY | STATE | ZIPCODE | TRANSACTION TYPE | TRANSACTION VALUE |")
                    for index, row in cust_transx.iterrows():
                        print(f"| {row['TIMEID']} | {row['TRANSACTION_ID']} | {row['first_name']} | {row['last_name']} | {row['cust_city']} | {row['cust_state']} | {row['cust_zip']} | {row['TRANSACTION_TYPE']} | {row['TRANSACTION_VALUE']:.2f} |")
                else:
                    print("No transactions found for the specified criteria.")
                
            case '2':
                trans_type = get_trans_type()
                if trans_type == 'q':
                    continue
                
                tranx_type=query_db(f"SELECT Transaction_Type, count(*) Transaction_Count, sum(transaction_value) Transaction_Total \
                            FROM cdw_sapp_credit_card \
                            WHERE transaction_type = '{trans_type}' \
                            GROUP BY transaction_type")
                
                         # display the total number and total values of transactions for branches in a given state.
                              
                if not tranx_type.empty:
                    # Display the result in a formatted table
                    print("\n| TRANSACTION TYPE | TRANSACTION COUNT | TRANSACTION TOTAL |")
                    for index, row in tranx_type.iterrows():
                        print(f"| {row['Transaction_Type']} | {row['Transaction_Count']} | {row['Transaction_Total']:.2f} |")
                else:
                    print(f"No transactions found for the transaction type: {trans_type}")  
                         
            case '3':
                state = get_str_input('State', 2)
                os.system('cls')
    
                result_tot_trans=query_db(f"SELECT Branch_State, count(branch_state) Total_Transactions, sum(cc.transaction_value) Total_Value \
                            FROM cdw_sapp_branches b \
                            JOIN cdw_sapp_credit_card cc \
                                ON b.branch_code = cc.BRANCH_CODE \
                            WHERE b.branch_state = '{state}' \
                            GROUP BY branch_state")
                
                result_tot_branch= query_db(f"SELECT b.branch_code, Branch_State , count(branch_state) Total_Transactions, sum(cc.transaction_value) Total_Value \
                            FROM cdw_sapp_branches b \
                            JOIN cdw_sapp_credit_card cc \
                                ON b.branch_code = cc.BRANCH_CODE \
                            WHERE b.branch_state = '{state}' \
                            GROUP BY branch_code, branch_state")
                
                if not result_tot_trans.empty:
                    total_transactions = result_tot_trans['Total_Transactions'].sum()
                    total_value = result_tot_trans['Total_Value'].sum()
                    print(f"TOTAL NUMBER OF TRANSACTIONS IN {state} = {total_transactions}")
                    print(f"TOTAL VALUE OF TRANSACTIONS FOR BRANCH IN {state} = ${total_value:.2f}\n")
        
                    # Display the details for each branch
                    print("BRANCH CODE | BRANCH STATE | TOTAL TRANSACTIONS | TOTAL VALUE")
        
                    for index, row in result_tot_branch.iterrows():
                        print(f"{row['branch_code']} | {row['Branch_State']} | {row['Total_Transactions']} | ${row['Total_Value']:.2f}")
                else:
                    print(f"No transactions found for state: {state}")
            
                
                            # check the existing account details of a customer
            case '4':
                ssn = get_str_input('SSN', 9)
                acct_detail= query_db(f"SELECT SSN, FIRST_NAME, MIDDLE_NAME, CREDIT_CARD_NO, FULL_STREET_ADDRESS, CUST_CITY, CUST_STATE, CUST_COUNTRY, CUST_ZIP, CUST_PHONE, CUST_EMAIL, LAST_UPDATED FROM cdw_sapp_customer c WHERE SSN = {ssn}")
                                     
                if acct_detail is not None:
                    if not acct_detail.empty:
                        print("\n| SSN | First Name | Middle Name | ... | Last Updated |")
                        for index, row in acct_detail.iterrows():
                            # Format and print the relevant columns
                            print(f"| {row['SSN']} | {row['FIRST_NAME']} | {row['MIDDLE_NAME']} | {row['CREDIT_CARD_NO']} |{row['FULL_STREET_ADDRESS']} |{row['CUST_CITY']}|{row['CUST_STATE']}|{row['CUST_PHONE']}|{row['CUST_EMAIL']} | {row['LAST_UPDATED']} |")
                    else:
                        print(f"No account details found for SSN: {ssn}")
                else:
                    print("An error occurred while querying the database. Please try again.")
                    
            case '5':
                ssn = get_str_input('SSN', 9)
                update_cust_db(ssn)

            case 'q':
                user_input = 'q'
                
            case _:
                print("Invalid choice. Pls try again.")

main()


                