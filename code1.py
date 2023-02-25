import mysql.connector
#import numpy as np
import pandas as pd


db='db'
pwd=''
table=''


def mysql_login():
    
    global pwd
    global mysql_logout
    mysql_logout=True
    while mysql_logout:
        try:
            pwd = '' #input('Enter MySQL password')
            conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd)
            query='create database if not exists '+db
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            mysql_logout=False   
        except:
            print('Wrong password!')
            print('--------------------------------------------------------------------------')


def login():
    
    global username
    print('--------------------------------------------------------------------------')
    username='u' #input("Enter username : ")
    password='p' #input("Enter password : ")
    print('--------------------------------------------------------------------------')
    if username=="u" and password=='p':
        print("Welcome "+str(username)+'!')
        home_page()
    else:
        login()


def create_tb(tbname):
    
    global db
    global pwd
    conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "create table if not exists "+str(tbname)+"(ind int (255) unique not null primary key);"
    cursor.execute(query)
    conn.commit()


def add_column(column_name, column_type, length = ''):
    
    global db
    global table
    global pwd
    conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query ="alter table "+str(table)+' add '+str(column_name)+' '+str(column_type)+' ('+str(length)+');'
    cursor.execute(query)
    conn.commit()


def add_values(values):
    
    global table
    global db
    global pwd
    conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "insert into "+str(table)+" values ("+str(values)+');'
    cursor.execute(query)
    conn.commit()


def update_values(col_name, set_to, row_index):
    
    try:
        global table
        global db
        global pwd
        conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
        cursor = conn.cursor()
        query = "update "+str(table)+" set "+str(col_name)+" = "+str(set_to)+" where ind="+str(row_index)+";"
        cursor.execute(query)
        conn.commit()
    except:
        print('uval except')


def drop_row(row_index):
    
    global table
    global db
    global pwd
    conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "delete from "+str(table)+" where ind="+str(row_index)+";"
    cursor.execute(query)
    conn.commit()


def fetch_all():
    
    global db
    global table
    global pwd
    global df
    conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "select * from "+table+";"
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    conn.commit()
    return df


def fetch_where(colname,value):
    
    global db
    global table
    global pwd
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "SELECT * from "+table+" where "+str(colname)+"='{}';".format(str(value))
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    conn.commit()
    return df


def set_tb(tb_nm):
    
    global table
    table = tb_nm


def import_csv(data):
    
    global table
    global db
    global pwd
    conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    try:
        query = "insert into "+str(table)+" values "+str(data)+';'
        cursor.execute(query)
        conn.commit()
    except:     #For redundant data
        pass


def export_csv(path,filename):
    
    global db
    global table
    global pwd
    conn = mysql.connector.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "SELECT * from "+str(table)+";"
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    df.columns=['ind','Product_name','Available_quantity','Price','Profit']
    df.to_csv(r"{}\{}.csv".format(path,filename))
    print("Data exported as "+str(filename)+".csv at ",path)
    conn.commit()
    

def home_page():
    
    global username
    global table
    global db
    global df
    set_tb(table)
    
    try:    
        create_tb(username+"_stonks")
        set_tb(username+"_stonks")
        add_column('Product_name','varchar','600')
        add_column('Available_quantity','int','255')
        add_column('Price','int','255')
        add_column('Profit','int','255')
    except:
        pass
    
    print('--------------------------------------------------------------------------')
    print("HOME PAGE")
    print('--------------------------------------------------------------------------')
    print("View complete stock (1)")
    print("Add Product (2)")
    print("Update stocks (3)")
    print("Remove product (4)")
    print("Search for a Product (5)")
    print('Add stocks using csv file (6)')
    print('Go back to login page (7)')
    print('Export (8)')
    print('Exit (9)')
    print('Delete database (10)')
    print('--------------------------------------------------------------------------')
    code=input('Enter code: ')
    print('--------------------------------------------------------------------------')

    if code == '1':
        try:
            df=fetch_all()
            df.columns=['ind','Product_name','Available_quantity','Price','Profit']
            print(df)
            print('--------------------------------------------------------------------------')
        except:
            print('Empty stock')
            print('--------------------------------------------------------------------------')
            
    elif code == '2':
        pn=input('Enter product name: ')
        qn=int(input('Enter available quantity: '))
        prc=int(input('Enter selling price: '))
        prf=int(input('Enter profit: '))
        index = input('Enter index value ')
        val = '{},"{}","{}","{}","{}"'.format(index,pn,qn,prc,prf)
        add_values(val)
        
    elif code == '3':
        update_page()
        
    elif code == '4':
        r=input('Enter row index to be deleted: ')
        drop_row(r)
        
    elif code == '5':
        search_page()

    elif code == '6':
        path=input('Enter memory address of CSV file: ')
        df2=pd.read_csv(r"{}.csv".format(path))
        df2.columns=['ind','Product_name','Available_quantity','Price','Profit']
        for i in range(len(df2)):
            nrow=tuple(df2.iloc[i])
            import_csv(nrow)

    elif code == '7':
        login()

    elif code == '8':
        path=input('Enter memory address of CSV file: ')
        filename=input('Enter CSV file name: ')
        export_csv(path,filename)

    elif code == '9':
        exit()

    elif code == '10':
        conn = mysql.connector.connect(host='localhost', user='root', password=pwd, database=db)
        cursor = conn.cursor()
        query = "drop database "+str(db)+";"
        cursor.execute(query)
        conn.commit()
        print('--------------------------------------------------------------------------')
        print("Database DELETED !")
        print('--------------------------------------------------------------------------')
        print("Go Back to Login Page (1)")
        print("Go to Home Page (2)")
        print("Exit (3)")
        print('--------------------------------------------------------------------------')
        code=input('Enter code: ')
        print('--------------------------------------------------------------------------')
        if code == '1':
            login()
        elif code == '2':
            home_page()
        elif code == '3':
            print("Exiting...")
            exit()
        
    else:
        print('Enter a valid code. ')
    home_page()            


def update_page():
    
    global set_to
    global row_index
    global col_name
    
    print('--------------------------------------------------------------------------')
    print("UPDATE PAGE")
    print('--------------------------------------------------------------------------')
    print("Update ind (1)")
    print("Update Product name (2)")
    print("Update available quantity (3)")
    print("Update price (4)")
    print("Update profit (5)")
    print('Back to home page (6)')
    print('--------------------------------------------------------------------------')
    
    col_code=input('Enter code: ')
    
    if col_code=='6':
        print('Reverting back to home page.')
        print('--------------------------------------------------------------------------')
        home_page()
        
    elif col_code not in ['1','2','3','4','5','6']:
        print('Enter a valid code. ')
        update_page()
        
    print('--------------------------------------------------------------------------')
    
    r=input('Enter row index to update: ')
    se=input('Enter new data ')
    c_name=''
    
    if col_code=='1':
        c_name='ind'
        
    elif col_code=='2':
        c_name='Product_name'
        
    elif col_code=='3':
        c_name='Available_quantity'
        
    elif col_code=='4':
        c_name='Price'
        
    elif col_code=='5':
        c_name='Profit'


    update_values(c_name, se, r)


def search_page():

    print('--------------------------------------------------------------------------')
    print("SEARCH PAGE")
    print('--------------------------------------------------------------------------')
    print('search product using Product_name  (1)')
    print('search product using Product_index (2)')
    print('Search product using Product_Price (3)')
    print('Search product using Product_Profit(4)')
    print('Go Back (5)')
    print('--------------------------------------------------------------------------')
    usr = input('enter code:')
    print('--------------------------------------------------------------------------')
    
    if usr == '1':
        Product= input('enter the product name you want to find:')
        df =fetch_where('Product_name',Product)
        df.columns=['ind','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '2':
        Product= input('enter the Product_index you want to find:')
        df =fetch_where('ind',Product)
        df.columns=['ind','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '3':
        Product= input('enter the Product_Price you want to find:')
        df =fetch_where('Price',Product)
        df.columns=['ind','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '4':
        Product= input('enter the Product_Profit you want to find:')
        df =fetch_where('Profit',Product)
        df.columns=['ind','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '5':
        print('Reverting back to home page.')
        home_page()
    
        
mysql_login()
login()