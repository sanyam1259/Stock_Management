import mysql.connector as sql
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


db='db'
pwd=''
table='stocks'


def mysql_login():
    
    global db
    global pwd
    global mysql_logout
    mysql_logout=True
    while mysql_logout:
        try:
            pwd = input('Enter MySQL password')
            conn = sql.connect(host='localhost', user='root', password=pwd)
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
        print('Values updated.')

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
    print('Row deleted.')


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
    
    print('--------------------------------------------------------------------------')
    print("HOME PAGE")
    print('--------------------------------------------------------------------------')
    print("(1) View entire stock ")
    print("(2) Add new product ")
    print("(3) Update stocks ")
    print("(4) Remove a product ")
    print("(5) Search for a product ")
    print('(6) Import stocks using CSV file ')
    print('(7) Export stocks to CSV file ')
    print('(8) Go back to login page ')
    print('(9) Exit ')
    print('(10)Visualise using Graphs ')
    print('(11)Delete database ')
    print('--------------------------------------------------------------------------')
    code=input('Enter code: ')
    print('--------------------------------------------------------------------------')

    if code == '1':
        try:
            df=fetch_all()
            df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
            view_stock()
        except:
            print('Empty stock')
            print('--------------------------------------------------------------------------')
        
    elif code == '2':
        pn=input('Enter product name: ')
        qn=int(input('Enter available quantity: '))
        prc=int(input('Enter selling price: '))
        prf=int(input('Enter  profit %: '))
        index = input('Enter Product Code ')
        val = '{},"{}","{}","{}","{}"'.format(index,pn,qn,prc,prf)
        add_row(val)
        
    elif code == '3':
        update_page()
        
    elif code == '4':
        r=input('Enter Product_Code to be deleted: ')
        drop_row(r)
        
    elif code == '5':
        search_page()

    elif code == '6':
        path=input('Enter memory address of CSV file without extention: ')
        df2=pd.read_csv(r"{}.csv".format(path))
        df2.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        for i in range(len(df2)):
            nrow=tuple(df2.iloc[i])
            import_csv(nrow)

    elif code == '7':
        path=input('Enter memory address of CSV file: ')
        filename=input('Enter CSV file name: ')
        export_csv(path,filename)

    elif code == '8':
        login()

    elif code == '9':
        print("exiting...")
        exit()

    elif code == '10':
        graph_page()
        
    elif code == '11':
        conn = sql.connect(host='localhost', user='root', password=pwd, database=db)
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
        print('Enter a valid code.')
    home_page()            


def view_stock():
    
    print('--------------------------------------------------------------------------')
    print('View data sorted by Product Codes (1)')
    print('View data sorted by Product name (2)')
    print('View data sorted by quantity (3)')
    print('View data sorted by price (4)')
    print('View data sorted by profit (5)')
    print('Go back to home page (0)')
    print('--------------------------------------------------------------------------')
    a=int(input('Enter code: '))
    print('--------------------------------------------------------------------------')
    
    if a==0:
        home_page()
        
    elif a not in [0,1,2,3,4,5]:
        print('Enter a valid code. ')
        
    else:       
        dict1={1:"Product_Code", 2:"Product_name", 3:"Available_quantity", 4:"Price", 5:"Profit"}
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


def update_page():
    
    global set_to
    global row_index
    global col_name
    
    print('--------------------------------------------------------------------------')
    print("UPDATE PAGE")
    print('--------------------------------------------------------------------------')
    print("Update Product Code (1)")
    print("Update Product name (2)")
    print("Update available quantity (3)")
    print("Update price (4)")
    print("Update profit % (5)")
    print('Back to home page (0)')
    print('--------------------------------------------------------------------------')
    
    col_code=int(input('Enter code: '))
    
    if col_code==0:
        print('Reverting back to home page...')
        print('--------------------------------------------------------------------------')
        home_page()
        
    elif col_code not in [0,1,2,3,4,5]:
        print('Enter a valid code. ')
        update_page()
        
    print('--------------------------------------------------------------------------')
    
    r=input('Enter Product Code to be updated: ')
    se=input('Enter new data ')
    c_name=''
    
    if col_code==1:
        c_name='Product_Code'
        
    elif col_code==2:
        c_name='Product_name'
        
    elif col_code==3:
        c_name='Available_quantity'
        
    elif col_code==4:
        c_name='Price'
        
    elif col_code==5:
        c_name='Profit'

    update_values(c_name, se, r)


def search_page():

    print('--------------------------------------------------------------------------')
    print("SEARCH PAGE")
    print('--------------------------------------------------------------------------')
    print('Search product using Product name (1)')
    print('Search product using Product Code (2)')
    print('Search product using Product price (3)')
    print('Search product using Product profit % (4)')
    print('Go Back (5)')
    print('--------------------------------------------------------------------------')
    usr = input('Enter code: ')
    print('--------------------------------------------------------------------------')
    
    if usr == '1':
        Product= input('Enter the Product name to find:')
        df =fetch_where('Product_name',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '2':
        Product= input('Enter the Product Code to find:')
        df =fetch_where('Product_Code',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '3':
        Product= input('Enter the Product price to find:')
        df =fetch_where('Price',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '4':
        Product= input('Enter the Product profit to find:')
        df =fetch_where('Profit',Product)
        df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
        print(df)
        search_page()
        
    if usr == '5':
        print('Reverting back to home page...')
        home_page()


def graph_plotter(x,y,type_graph):
    
    global table
    
    c_name=''
    set_tb(table)
    df=fetch_all()
    df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
    x=df['Product_name']
    
    lstX=[]
    for i in x :
        lstX.append(int(i))
    lstY=[]
    for i in y :
        lstY.append(int(i))
    if type_graph == 'line':
        try :
            plt.plot(lstX,lstY)
            plt.xticks(df['Product_name'])
            plt.show()
        except :
            print('ERROR, Not enough data to plot graph')
            
    elif type_graph == 'bar':
       
        plt.bar(lstX,lstY)
        plt.show()
        
        print('ERROR, Not enough data to plot graph')
    graph_page()

        
def graph_page():
    
    global table
    
    print('--------------------------------------------------------------------------')
    print("GRAPHING PAGE")
    print('--------------------------------------------------------------------------')
    g_type=input("Enter type of graph(bar/line)")
    print('--------------------------------------------------------------------------')
    print('Enter which graph to plot')
    print('(1) Product and Available quantity')
    print('(2) Product and Price')
    print('(3) Product and Profit%')
    print('--------------------------------------------------------------------------')
    col_code=int(input('Enter code: '))
    print('--------------------------------------------------------------------------')
    
    
    c_name=''
    set_tb(table)
    df=fetch_all()
    df.columns=['Product_Code','Product_name','Available_quantity','Price','Profit']
    x=df['Product_name']
        
    if col_code==1:
        c_name='Available_quantity'
        y=df[c_name]

    elif col_code==2:
        c_name='Price'
        y=df[c_name]
        
    elif col_code==3:
        c_name='Profit'
        y=df[c_name]

    graph_plotter(x,y,g_type)
    home_page()


mysql_login()
login()
