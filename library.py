#-----------------------------***LIBRARY DATABASE SYSTEM SET UP***-------------------------
import mysql.connector
lib_db_config = mysql.connector.connect(
    host="127.0.0.1",
    user="Ericadeshh",
    password="404-found-#"
)

cursor = lib_db_config.cursor()
cursor.execute("DROP DATABASE IF EXISTS Library")
cursor.execute("CREATE DATABASE Library")
print("Library DB Created!")

cursor.execute("USE Library")
cursor.execute("set foreign_key_checks = 0")

member_table = '''
    CREATE TABLE IF NOT EXISTS MEMBER_TABLE(
        MEMBER_NAME VARCHAR(255),
        MEMBER_ID INT,
        MEMBER_EMAIL VARCHAR(255),
        MEMBER_PHONE_NO INT
        )
'''
cursor.execute(member_table)
#cursor.execute("CREATE INDEX IF NOT EXISTS idx_MEMBER_ID ON MEMBER_TABLE(MEMBER_ID)")
 # Check if index exists before creating it
cursor.execute("SHOW INDEX FROM MEMBER_TABLE WHERE Key_name = 'idx_MEMBER_ID'")
if not cursor.fetchone():
    cursor.execute("CREATE INDEX idx_MEMBER_ID ON MEMBER_TABLE(MEMBER_ID)")
lib_db_config.commit()
print("Member Table created.")

books_table = '''
    CREATE TABLE IF NOT EXISTS BOOK_TABLE(
        BOOK_NAME VARCHAR(255),
        BOOK_ID INT
        )
'''
cursor.execute(books_table)
lib_db_config.commit()
print("Book Table created.")

issue_table = '''
    CREATE TABLE IF NOT EXISTS ISSUE_TABLE(
        MEMBER_NAME VARCHAR(255),
        MEMBER_ID INT,
        BOOK_NAME VARCHAR(255),
        BOOK_ID INT,
        ISSUED_DATE VARCHAR(255),
        DUE_DATE VARCHAR(255),
        AVAILABILITY VARCHAR(255)
    )
'''
cursor.execute(issue_table)
lib_db_config.commit()
print("Issue table created")
#lib_db_config.close()

#--------------------------------------***BOOK FUNCTIONS***------------------------------------
#function of book
#function to add a book
def add_book():
    print("\n-----------------ADDING A BOOK-------------------")
    book_name = input("Enter Book Name: ")
    book_id = input("Enter Book ID: ")
    #check if book already exists
    check_query = "SELECT * FROM BOOK_TABLE WHERE BOOK_NAME=%s AND BOOK_ID=%s"
    check_values = (book_name,book_id)
    cursor.execute(check_query,check_values)
    existing_book = cursor.fetchone()

    if existing_book:
        print(f"\n{book_name}-Book Already exists in the databse")
        return
    #add book in the database
    add_book_query = '''
        INSERT INTO BOOK_TABLE(BOOK_NAME,BOOK_ID)
        VALUES( %s , %s) 
    '''
    add_book_values = (book_name,book_id)
    cursor.execute(add_book_query,add_book_values)
    lib_db_config.commit()
    print(f"\n{book_name}-Book Added Successfully")
#add_book()

#function to search book
def search_book_func():
    print("\n-----------------SEARCHING BOOKS----------------")
    search_book = input("\nSearch Book Name: ")
    search_book_query = "SELECT * FROM BOOK_TABLE WHERE BOOK_NAME=%s"
    search_book_values = (search_book,)
    cursor.execute(search_book_query,search_book_values)
    result= cursor.fetchall()
    if result:
        print("  Book found")
        for book in result:
            print(book)
    else:
        print('\nNo Such Book Found!')
    lib_db_config.commit()
#search_book_func()

#function to update  a book details
def update_book():
    print("\n--------------UPDATING THE VALUES IN THE BOOK TABLE--------------")
    cursor.execute("SELECT * FROM  BOOK_TABLE")
    rows = cursor.fetchall()

    search_id = input("\nEnter ID(The Digits in the Third Place): ")
    new_book_name = input("\nEnter new book name: ")
    new_book_id = input("Enter new book ID: ")

    update_book_query = "UPDATE  BOOK_TABLE SET BOOK_NAME=%s,BOOK_ID=%s WHERE BOOK_ID=%s"
    cursor.execute(update_book_query,(new_book_name,new_book_id,search_id))
    lib_db_config.commit()
    print(f"\n{new_book_name}- has been updated successfully\n")
#update_book(new_book_name,new_book_id)

#function to delete a book
def delete_book():
    print("\n-----------DELETING A BOOK-------------")
    del_book = input("\nEnter book name to delete: ")
    delete_book_query = "DELETE FROM BOOK_TABLE WHERE BOOK_NAME=%s"
    delete_book_values = (del_book,)
    cursor.execute(delete_book_query,delete_book_values)
    lib_db_config.commit()
    print(f"\n{del_book}-Book Deleted Successfully\n")
#delete_book(del_book)

# Function to view all books in the library
def view_all_books():
    print("\n---------------VIEW ALL BOOK IN THE BOOK_TABLE--------------")
    query = "SELECT * FROM BOOK_TABLE"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        print("All books in the library:")
        for book in result:
            print(book)
    else:
        print("No books available in the library.")
#view_all_books()

def choose_book_function():
    print("\n--BOOK OPERATIONS--\n")
    print("\n1. Add a Book!")
    print("2. Search a Book!")
    print("3. Update a Book!")
    print("4. Delete a Book!")
    print("5. View all Books")
    print("\n0. Exit\n")

    while True:
        choice_func = input("\nEnter Your Desired *BOOK*-Operation: ") 
        if choice_func == "1":
            add_book()
            continue
        elif choice_func == "2":
            search_book_func()
            continue
        elif choice_func == "3":
            update_book()
            continue
        elif choice_func == "4":
            delete_book()
            continue
        elif choice_func == "5":
            view_all_books()
            continue
        elif choice_func =="0":
            print("\nExiting Book Menu...\n")
            break
        else:
            print("Invalid Choice!")
#choose_book_function()

#-----------------------------------***MEMBER FUNCTIONS***--------------------------------
#Function to ADD a new Member
def add_member():
    add_member_name = input("\nEnter Member Name: ")
    add_member_id = int(input(f"Enter {add_member_name}'s ID: "))
    add_member_email = input(f"Enter {add_member_name}'s Email: ")
    add_member_phone_no = int(input(f"Enter {add_member_name}'s Phone Number: "))

    add_member_query = '''
        INSERT INTO MEMBER_TABLE(MEMBER_NAME,MEMBER_ID,MEMBER_EMAIL,MEMBER_PHONE_NO)
        VALUES(%s, %s,%s,%s)
    '''
    add_member_values = (add_member_name,add_member_id,add_member_email,add_member_phone_no)
    cursor.execute(add_member_query,add_member_values)
    print(f"{add_member_name}- Member Added Successfully")
    lib_db_config.commit()
#add_member()

#Function to Modify Members
def modify_members():
    print("\nUPDATING A MEMBER!")
    new_name = input("\nEnter New member name: ")
    new_id = int(input("Enter New member ID: "))
    new_email= input("Enter New Email: ")
    new_phone_no = int(input("Enter New Phone  Number: "))

    update_member_query = "UPDATE MEMBER_TABLE SET MEMBER_NAME = %s, MEMBER_EMAIL=%s,MEMBER_PHONE_NO=%s WHERE MEMBER_ID=%s"
    #update_member_values=(MEMBER_NAME,MEMBER_EMAIL,MEMBER_PHONE_NO,MEMBER_ID)
    cursor.execute(update_member_query,(new_name,new_email,new_phone_no,new_id))
    lib_db_config.commit()
    print(f"{new_name}- Member Updated Successfully")
#modify_members()

#function to delete a member
def delete_member():
    print("\nDELETING A MEMBER!")
    del_member_id = int(input("\nEnter the ID of the member you want to Delete: "))
    delete_member_query="DELETE FROM  MEMBER_TABLE WHERE MEMBER_ID=%s"
    delete_member_values = (del_member_id, )
    cursor.execute(delete_member_query,delete_member_values)
    lib_db_config.commit()
    print(f"\n{del_member_id}- Member deleted Successfully\n")
#delete_member()

def choose_member_function():
    print("\n--MEMBER OPERATIONS--")
    print("\n1. Add a New Member...")
    print("2. Update an Existing Member...")
    print("3. Remove a Member...")
    print("\n0. Exit\n")

    while True:
        choice_func = input("\nEnter Your Desired *MEMBER-BOOK*-Operation: ") 
        if choice_func == "1":
            add_member()
            continue
        elif choice_func == "2":
            modify_members()
            continue
        elif choice_func == "3":
            delete_member()
            continue
        elif choice_func =="0":
            print("\nExiting Members Menu...\n")
            break
        else:
            print("Invalid Choice!")
#choose_member_function()
            
#-------------------------***ISSUE FUNCTIONS***------------------------------
from datetime import datetime, timedelta
def issue_book():
    print("\n------------FUNCTION TO ISSUE A BOOK------------")
    member_name = input("\nEnter name of Student to issue book: ")
    member_id= input(f"Enter ID of {member_name} to issue book: ")
    book_name = input("Enter name of Book to issue: ")
    book_id = input(f"Enter {book_name}'s ID: ")

    due_date = datetime.now() + timedelta(days=10) # 10 days for the borrow period
    update_due_date_query = '''
        INSERT INTO ISSUE_TABLE(MEMBER_NAME,MEMBER_ID,BOOK_NAME,BOOK_ID,ISSUED_DATE,DUE_DATE,AVAILABILITY)
        VALUES(%s,%s,%s,%s,%s,%s,'ISSUED')
        '''
    update_due_date_values = (member_name,member_id,book_name,book_id,datetime.now(),due_date)
    cursor.execute(update_due_date_query,update_due_date_values)
    lib_db_config.commit()
    print("\nBook Issued Successfully. Due Date: ",due_date)
    
    issue_book_query = "SELECT * FROM ISSUE_TABLE WHERE MEMBER_NAME=%s AND MEMBER_ID=%s AND BOOK_NAME=%s AND BOOK_ID=%s AND AVAILABILITY='AVAILABLE'"
    issue_book_values = (member_name,member_id,book_name,book_id)
    cursor.execute(issue_book_query,issue_book_values)
    result = cursor.fetchone()

    if not result:
         #print("\nBOOK NOT AVAILABLE FOR ISSUING\n")
        pass
    else:
         #update book availability
        availabilty_query = "UPDATE ISSUE_TABLE SET AVAILABILITY = 'ISSUED' WHERE BOOK_ID=%s"
        cursor.execute(availabilty_query,(book_id))
        lib_db_config.commit()
#issue_book()

#function to RETURN BOOK to Library
def  return_book():
    print("\n-----------FUNCTION TO RETURN THE BOOK TO THE LIBRARY-----------\n")
    return_book_name = input("\nEnter name of Book To Return : ")
    return_book_id = input(f"Enter ID of {return_book_name}: ")
    member_that_borrowed_book ="SELECT MEMBER_NAME FROM ISSUE_TABLE WHERE BOOK_NAME=%s AND BOOK_ID=%s" 
    member_that_borrowed_book_values = (return_book_name,return_book_id)
    cursor.execute(member_that_borrowed_book,member_that_borrowed_book_values)
    member_info = cursor.fetchone()
    if not member_info:
        print("\nNO SUCH BOOK FOUND IN LIBRARY OR IT IS ALREADY RETURNED.\n")
    else:
        member_name = member_info[0]
        print(f"\n{return_book_name} is returned by {member_name}. Thank You!\n")
        
        #updating the database with returned status and date
        returned_status_and_date = ("RETURNED",datetime.now())
        returned_query = "UPDATE ISSUE_TABLE SET AVAILABILITY= %s , RETURNED_DATE= %s WHERE BOOK_NAME=%s AND BOOK_ID=%s"
        returned_query = f''' UPDATE ISSUE_TABLE
                            SET STATUS=%s,DATE_OF_RETURNED=%s
                            WHERE BOOK_NAME=%s AND BOOK_ID=%s'''
        cursor.execute(returned_query, (returned_status_and_date + (return_book_name, return_book_id)))
        lib_db_config.commit()
#return_book()

def choose_issue_function():
    print("\n--ISSUE OPERATIONS--")
    print("\n1. Get a Book Issued...")
    print("2. Return a Book...")
    print("\n0. Exit\n")

    while True:
        choice_func = input("\nEnter Your Desired *ISSUE-BOOK*-Operation: ") 
        if choice_func == "1":
            issue_book()
            continue
        elif choice_func == "2":
            return_book()
            continue
        elif choice_func =="0":
            print("\nExiting Issue Menu...\n")
            break
        else:
            print("Invalid Choice!")

#choose_issue_function()
            
#--------------------------------***MENU INTERFACE***--------------------------------
class Menu:
    def __init__(self):
        print("\n---------------WELCOME TO ABC SCHOOL LIBRARY---------------\n")
        print("*********GROUP S MEMBERS*********")

        group_S_members = ["Daisy Chebet","Evelyn Akinyi","Oscar Wamalwa"]
        for person in group_S_members:
            if person == "Daisy Chebet":
                print(f"{person}-database Dev")
            else:
                 print(f"{person}-Group Member")

    #function to display menu
    def display_menu(self):
        print("\nMain Menu: ")
        print("1. Library Management")
        print("2. Books Management")
        print("3. Issue Management")
        print("4. Member Management")
        print("5. Exit")

    def run_choice(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")
            if choice == "1":
                print("\nLibrary Management Module Selected")
                print("\nLIBRARY MODULE UNDER  DEVELOPMENT!\n")
            elif choice == "2":
                print("\nBook Functions Management Module Selected!")
                choose_book_management_func = '''
                    1.Add a New Book
                    2.Update a Book
                    3.Delete a Book
                '''
                print(choose_book_management_func)
                choose_book_management_func_input = input(">>>: ")
                if choose_book_management_func_input =="1":
                    add_book()
                    continue
                elif choose_book_management_func_input =="2":
                    update_book()
                    continue
                elif choose_book_management_func_input =="3":
                    delete_book()
                    continue
                else:
                    print("INVALID CHOICE FOR BOOK FUNC..")
                    continue

            elif choice == "3":
                print("\nIssue Management Module Selected!")
                choose_issue_management_func = '''
                    1.Issue a Book
                    2.Return a Book
                '''
                print(choose_issue_management_func)
                choose_issue_management_func_input = input(">>>: ")
                if choose_issue_management_func_input =="1":
                    issue_book()
                    continue
                elif choose_issue_management_func_input =="2":
                    return_book()
                    continue
                else:
                    print("INVALID CHOICE FOR BOOK FUNC..")
                    continue

            elif choice == "4":
                print("\nMember Management Module Selected!")
                choose_member_management_func = '''
                    1.Add a New Member
                    2.Update a Member
                    3.Delete a Member
                '''
                print(choose_member_management_func)
                choose_member_management_func_input = input(">>>: ")
                if choose_member_management_func_input =="1":
                   add_member()
                   continue
                elif choose_member_management_func_input =="2":
                    modify_members()
                    continue
                elif choose_member_management_func_input =="3":
                   delete_member()
                   continue
                else:
                    print("INVALID CHOICE FOR MEMBER FUNC..")
                    continue

            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a valid option!")

menu = Menu()
menu.run_choice()

'''if __name__ =="__main__":
    menu = Menu()
    menu.run_choice()
    '''


