import psycopg2
from datetime import date
conn = psycopg2.connect(database="sales_system", user='postgres', password='Genius1584.', host='localhost', port= '5432')

cur = conn.cursor()
# select function
def get_data(p):
   cur = conn.cursor()
   t = "select * from " + p
   cur.execute(t)
   data = cur.fetchall()
   return data

# insert function
def insert_product(values):
        # Connect to the PostgreSQL database
        cur = conn.cursor()

        # Execute the INSERT statement
        column_product="(name,buying_price,selling_price,stock_quantity)"
       
        store_products= f"INSERT INTO products{column_product}VALUES{values}"
    
        cur.execute(store_products,values)
        # Commit the transaction
        conn.commit()

        return True

def insert_sales(values):
      column_sales="(productid,quantity,created_at)"
      store_sales=f"INSERT INTO sales{column_sales} VALUES(%s,%s,%s)"

      cur.execute(store_sales,values)



def calc_profit():
      calc_query="select DATE(created_at) AS Date, sum((selling_price -buying_price)*quantity) as profit from sales join products on products.id=sales.productid group by Date order by date"
      cur.execute(calc_query)
      fetch=cur.fetchall()
      return fetch

#  create users
def create_users(values):
      values_us = "insert into users(full_name,email,password) VALUES (%s,%s,%s)"
      cur.execute(values_us,(values))
      conn.commit()




# query for email
def  check_email():
      check_all="select exist(select 1 from users where email = %s )"
      cur.execute(check_all)
      email_exist = cur.fetchone()[0]
      return email_exist

# query for password
def confirm_password():
      comf_pass = "select count(*) from users where password = %s and email = %s"
      cur.execute(comf_pass)
      con_pass = cur.fetchone()[0]
      return con_pass

# check email exists
def email_pass(email):
    cursor = conn.cursor()
    check_all = 'SELECT * FROM users WHERE email=%s'

    cursor.execute(check_all,(email))
    
    data=cursor.fetchone()

    if data:
     return data
    else:
         False


# check email and pass are the same
# def email_and_pas(email,password):
#      cur=conn.cursor()
#      e_p="SELECT userid FROM users where email =%s and password=%s"
#      cur.execute(e_p,(email,password))
#      check=cur.fetchone()
#      if check is not None:
#             userid = check[0]
#             return userid
#      else:
#             return None


    

def email_and_pas(email, password):
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    # Check if a user with the provided email exists
    if user:
        # Check if the password matches
        if user[3] == password:  
            return user  # Return the user data
    return False  # Email or password do not match