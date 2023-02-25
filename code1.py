import mysql.connector as sql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


db='Stock_Management'
pwd=''
table='Stocks'


def mysql_login():
    
    global db
    global pwd
    global mysql_logout
    mysql_logout=True
    while mysql_logout:
        try:
            pwd = input('Enter MySQL password: ')
            conn = sql.connect(host='localhost', user='root', password=pwd)
            query='create database if not exists '+db
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            mysql_logout=False 
        except:
            print('Wrong password!')
            print('-------------------------------------'*2)


def login():
    
    global username
    print('-------------------------------------'*2)
    print('LOGIN PAGE')
    print('-------------------------------------'*2)
    username=input("Username: ")
    password=input("Password: ")
    print('-------------------------------------'*2)
    check={'sam':'ps', 'kartik':'pk'}
    
    if (username, password) in check.items():
        print("Welcome "+username+'!')
        home_page()
    else:
        print('Wrong username and/or password!')
        print('-------------------------------------'*2)
        login()


def create_tb(tbname):
    
    global db
    global pwd
    conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "create table if not exists "+str(tbname)+"(Product_Code int (255) unique not null primary key);"
    cursor.execute(query)
    conn.commit()


def set_tb(tb_nm):
    
    global table
    table = tb_nm


def add_column(column_name, column_type, length = ''):
    
    global db
    global table
    global pwd
    conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query ="alter table "+str(table)+' add '+str(column_name)+' '+str(column_type)+' ('+str(length)+');'
    cursor.execute(query)
    conn.commit()
    

def add_row(values):
    
    global table
    global db
    global pwd
    conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "insert into "+str(table)+" values ("+str(values)+');'
    cursor.execute(query)
    conn.commit()


def update_values(col_name, set_to, row_index):
    
    try:
        global table
        global db
        global pwd
        conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
        cursor = conn.cursor()
        query = "update "+str(table)+" set "+str(col_name)+" = "+str(set_to)+" where Product_Code="+str(row_index)+";"
        cursor.execute(query)
        conn.commit()
        print('-------------------------------------'*2)
        print('Value updated.')
        print('-------------------------------------'*2)

    except:
        print('Invalid update request.')


def drop_row(row_index):
    
    global table
    global db
    global pwd
    conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "delete from "+str(table)+" where Product_Code="+str(row_index)+";"
    cursor.execute(query)
    conn.commit()
    print('-------------------------------------'*2)
    print('Product deleted.')
    print('-------------------------------------'*2)


def fetch_all():
    
    global db
    global table
    global pwd
    global df
    conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
    cursor = conn.cursor()
    query = "SELECT * from "+table+";"
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    conn.commit()
    return df


def fetch_where(colname,value):
    
    global db
    global table
    global pwd
    conn = sql.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "SELECT * from "+table+" where "+str(colname)+"='{}';".format(str(value))
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    conn.commit()
    return df


def import_csv(data):
    
    global table
    global db
    global pwd
    conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
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
    conn = sql.connect(host = 'localhost', user = 'root', password = pwd, database = str(db))
    cursor = conn.cursor()
    query = "SELECT * from "+str(table)+";"
    cursor.execute(query)
    output = cursor.fetchall()
    df = pd.DataFrame(output)
    df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
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
        create_tb("stocks")
        set_tb("stocks")
        add_column('Product_name','varchar','600')
        add_column('Available_quantity','int','255')
        add_column('Price','int','255')
        add_column('Profit','int','255')
    except:
        pass
    
    print('-------------------------------------'*2)
    print("HOME PAGE")
    print('-------------------------------------'*2)
    print("View entire stock (1) ")
    print("Add new product (2) ")
    print("Update stocks (3) ")
    print("Remove a product (4) ")
    print("Search for a product (5) ")
    print('Import stocks using CSV file (6) ')
    print('Export stocks to CSV file (7) ')
    print('Visualise using Graphs (8) ')
    print('Delete all stock data (9) ')
    print('Go back to login page (10) ')
    print('Exit Program (11) ')
    print('-------------------------------------'*2)
    code=input('Enter code: ')
    print('-------------------------------------'*2)

    if code == '1':
        try:
            df=fetch_all()
            df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
            view_stock()
        except:
            print('Empty stock')
            print('-------------------------------------'*2)
        
    elif code == '2':
        pn=input('Enter product name: ')
        qn=int(input('Enter available quantity: '))
        prc=int(input('Enter selling price: '))
        prf=int(input('Enter  profit %: '))
        index = input('Enter Product Code ')
        val = '{},"{}","{}","{}","{}"'.format(index,pn,qn,prc,prf)
        add_row(val)
        print('-------------------------------------'*2)
        print("Product Added")
        print('-------------------------------------'*2)
                
    elif code == '3':
        update_page()
        
    elif code == '4':
        r=input('Enter Product Code to be deleted: ')
        
        try:
            df=fetch_all()
            df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
            lst=list(df['Product_Code'])
            if int(r) in lst:
                drop_row(r) 
            else:
                print('Product Code not found.')
                
        except:
            print('Invalid deletion request.')
            
        
    elif code == '5':
        search_page()

    elif code == '6':
        path=input('Enter memory address of CSV file without extention: ')

        try:
            df2=pd.read_csv(r"{}.csv".format(path))
        except:
            print('Invalid Address ')
            print('-------------------------------------'*2)
            home_page()

        df2.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        for i in range(len(df2)):
            nrow=tuple(df2.iloc[i])
            import_csv(nrow)

    elif code == '7':
        path=input('Enter memory address of CSV file: ')
        filename=input('Enter CSV file name: ')
        try:
            export_csv(path,filename)
        except:
            print('Some error occured.')
            print('-------------------------------------'*2)

    elif code == '8':
        graph_page()

    elif code == '9':
        conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
        cursor = conn.cursor()
        query = "drop table "+str(table)+";"
        cursor.execute(query)
        conn.commit()
        print('-------------------------------------'*2)
        print("Data DELETED !")
        print('-------------------------------------'*2)
        print("Go Back to Login Page (1)")
        print("Go to Home Page (2)")
        print("Exit Program (3)")
        print('-------------------------------------'*2)
        code=input('Enter code: ')
        print('-------------------------------------'*2)

        if code == '1':
            login()
        elif code == '2':
            home_page()
        elif code == '3':
            print("Exiting...")
            exit()

    elif code == '10':
        login()

    elif code == '11':
        print("exiting...")
        exit()
                
    else:
        print('Enter a valid code.')
        print('-------------------------------------'*2)
    home_page()            


def view_stock():
    
    print('-------------------------------------'*2)
    print('View data sorted by Product codes (1)')
    print('View data sorted by Product name (2)')
    print('View data sorted by quantity (3)')
    print('View data sorted by price (4)')
    print('View data sorted by profit % (5)')
    print('Go back to home page (0)')
    print('-------------------------------------'*2)
    a=input('Enter code: ')
    print('-------------------------------------'*2)
    
    if a=='0':
        home_page()
        
    elif a not in ['0','1','2','3','4','5']:
        print('Enter a valid code. ')
        
    else:       
        dict1={'1':"Product_Code", '2':"Product_name", '3':"Available_quantity", '4':"Price", '5':"Profit"}
        cname=dict1[a]
        global db
        global table
        global pwd
        conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
        cursor = conn.cursor()
        query = "SELECT * from {} order by {};".format(str(table),cname)
        cursor.execute(query)
        output = cursor.fetchall()
        df=pd.DataFrame(output)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        conn.commit()
        print(df)
    view_stock()


def update_page():
    
    global set_to
    global row_index
    global col_name
    global df
    
    print('-------------------------------------'*2)
    print("UPDATE PAGE")
    print('-------------------------------------'*2)
    print("Update Product Code (1)")
    print("Update Product Name (2)")
    print("Update Available Quantity (3)")
    print("Update Price (4)")
    print("Update Profit % (5)")
    print('Back to Home Page (0)')
    print('-------------------------------------'*2)
    
    col_code=input('Enter code: ')
    print('-------------------------------------'*2)
    
    if col_code=='0':
        print('Reverting back to home page...')
        print('-------------------------------------'*2)
        home_page()
        
    elif col_code not in ['0','1','2','3','4','5']:
        print('Enter a valid code. ')
        print('-------------------------------------'*2)
        update_page()
            
    c_name=''
    df=fetch_all()
    df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
    
    if col_code=='1':
        c_name='Product_Code'
        
    elif col_code=='2':
        c_name='Product_name'
        
    elif col_code=='3':
        c_name='Available_quantity'
        
    elif col_code=='4':
        c_name='Price'
        
    elif col_code=='5':
        c_name='Profit'
    
    r=input('Enter Product Code to be updated: ')
    lst=list(df['Product_Code'])
    
    if int(r) in lst:
        se=input('Enter new data ')
        update_values(c_name, se, r)  
    else:
        print('Product Code not found.')
        update_page()


def search_page():

    print('-------------------------------------'*2)
    print("SEARCH PAGE")
    print('-------------------------------------'*2)
    print('Search product using Product name (1)')
    print('Search product using Product Code (2)')
    print('Search product using Product price (3)')
    print('Search product using Product profit % (4)')
    print('Go Back (0)')
    print('-------------------------------------'*2)
    usr = input('Enter code: ')
    print('-------------------------------------'*2)
    
    if usr == '1':
        Product= input('Enter the Product name to find: ')
        df =fetch_where('Product_name',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '2':
        Product= input('Enter the Product Code to find: ')
        df =fetch_where('Product_Code',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '3':
        Product= input('Enter the Product price to find: ')
        df =fetch_where('Price',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '4':
        Product= input('Enter the Product profit % to find: ')
        df =fetch_where('Profit',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '0':
        print('Reverting back to home page...')
        print('-------------------------------------'*2)
        home_page()

        
def graph_page():
    
    global table
    print('-------------------------------------'*2)
    print("GRAPHING PAGE")
    print('-------------------------------------'*2)
    print('Enter which graph to plot')
    print('(1) Product vs Available quantity')
    print('(2) Product vs Price')
    print('(3) Product vs Profit')
    print('(0) Go back to Home Page')
    print('-------------------------------------'*2)
    col_code=input('Enter code: ')
    print('-------------------------------------'*2)

    if col_code=='0':
        print('Reverting back to Home Page...')
        print('-------------------------------------'*2)
        home_page()

    print('Type of Graph :')
    print('Bar (1) ')
    print('Line (2) ')
    print('-------------------------------------'*2)
    g_code=input('Enter code: ')
    print('-------------------------------------'*2)
    
    
    c_name=''
    set_tb(table)
    df=fetch_all()
    df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
    x=range(len(df))
    
    if col_code=='1':
        c_name='Available_quantity'
        y=list(df[c_name])

    elif col_code=='2':
        c_name='Price'
        y=list(df[c_name])
        
    elif col_code=='3':
        c_name='Profit'
        y=list(df[c_name])

    else:
        print('Enter a valid code.')
        print('-------------------------------------'*2)
        graph_page()

    if g_code=='1':
        g_type='bar'

    elif g_code=='2':
        g_type='line'

    else:
        print('Enter a valid code.')
        print('-------------------------------------'*2)
        graph_page()

    x_tick=np.array(df['Product_name'])
    x_label='Product Name'
    y_label=c_name
    
    graph_plotter(x, y, g_type, x_tick, x_label, y_label, c_name)
    home_page()


def graph_plotter(x, y, g_type, x_tick, x_label, y_label, c_name):

    if g_type == 'line':
        try :
            plt.plot(x, y, color='blue', linestyle=":", marker='.', markerfacecolor='g', markersize=12, markeredgecolor='g')
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.xticks(x, x_tick)
            plt.title('Product vs '+c_name)
            plt.show()
        except :
            print('ERROR, Not enough data to plot graph')
            
    elif g_type == 'bar':
        try :
            plt.bar(x, y, width=0.6)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.xticks(x, x_tick)
            plt.title('Product vs '+c_name)
            plt.show()
        except :
            print('ERROR, Not enough data to plot graph')

    graph_page()


mysql_login()
login()
