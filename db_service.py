import psycopg2

# Function to connect to the database
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="sales",
        user="postgres",
        password="Genius1584."
    )

# Function to get data from a specified table
def get_data(table):
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
    return rows

# Function to add a product
def add_product(name, buying_price, selling_price, stock_quantity):
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute(
                """
                INSERT INTO products (product_name, buying_price, selling_price, stock_quantity)
                VALUES (%s, %s, %s, %s)
                """,
                (name, buying_price, selling_price, stock_quantity)
            )
            con.commit()

# Function to make a sale
def make_sale(product_id, quantity):
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sales (product_id, quantity, created_at)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                """,
                (product_id, quantity)
            )
            con.commit()
            
# Function to fetch all products
def fetch_all_products():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT product_id, product_name FROM products")
            return cur.fetchall()

# Function to calculate profit per product
def calculate_profit_per_product():
    with connect_db() as con:
        with con.cursor() as cur:
            # Query to get sales data along with buying and selling prices
            query = """
                SELECT 
                    p.product_name,
                    SUM((p.selling_price - p.buying_price) * s.quantity) AS total_profit
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                GROUP BY p.product_name
                ORDER BY p.product_name;
            """
            cur.execute(query)
            data = cur.fetchall()
    return data

# Function to calculate total sales per product
def calculate_sales_per_product():
    with connect_db() as con:
        with con.cursor() as cur:
            # Query to get sales data along with selling prices
            query = """
                SELECT p.product_name, SUM(p.selling_price * s.quantity) AS total_sales
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                GROUP BY p.product_name
            """
            cur.execute(query)
            data = cur.fetchall()
    return data

# Function to create profit per day
def calculate_profit_per_day():
    with connect_db() as con:
        with con.cursor() as cur:
            # Query to get sales data along with buying and selling prices
            query = """
                SELECT 
                    DATE(s.created_at) AS sale_date,
                    SUM((p.selling_price - p.buying_price) * s.quantity) AS total_profit
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                GROUP BY sale_date
                ORDER BY sale_date;
            """
            cur.execute(query)
            data = cur.fetchall()
    return data

# Function to calculate sales per day
def calculate_sales_per_day():
    with connect_db() as con:
        with con.cursor() as cur:
            query = """
                SELECT 
                    DATE(created_at) AS sale_date, 
                    SUM(quantity) AS total_quantity,
                    SUM(p.selling_price * s.quantity) AS total_sales
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                GROUP BY sale_date
                ORDER BY sale_date;
            """
            cur.execute(query)
            data = cur.fetchall()
    return data

def add_user(full_name, email, password):
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            
            if user:
                return "User already registered"
            
            cur.execute(
                """
                INSERT INTO users (full_name, email, password)
                VALUES (%s, %s, %s)
                """,
                (full_name, email, password)  # Store plain text password
            )
            con.commit()
            return "User registered successfully"

def check_email_exists(email):
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)", (email,))
            exists = cur.fetchone()[0]
    return exists

def check_email_password_match(email, password):
    with connect_db() as con:
        with con.cursor() as cur:
            query = "SELECT full_name, password FROM users WHERE email = %s"
            cur.execute(query, (email,))
            result = cur.fetchone()
            
            if result:
                stored_password = result[1]
                if stored_password == password:
                    full_name = result[0]
                    return full_name
            return None
 # Fetch the total number of products
def total_products():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM products")
            total_product = cur.fetchall()[0]
    return total_product
# def total_sales():
#     with connect_db() as con:
#             with con.cursor() as cur:
#               cur.execute("SELECT SUM(selling_price )FROM products")
#               total_sale = cur.fetchall()[0]
#     return total_sale
# def total_profits():
#     with connect_db() as con:
#             with con.cursor() as cur:       
#              cur.execute("SELECT SUM(selling_price - buying_price) FROM products")
#              total_profit = cur.fetchall()[0] 
#     return total_profit
# def top_selling():
#     with connect_db() as con:
#             with con.cursor() as cur:        
#              cur.execute("SELECT product_name, SUM(quantity) as total_quantity FROM sales JOIN products ON sales.product_id = products.id GROUP BY product_name ORDER BY total_quantity DESC LIMIT 1")
#              top_selling_product = cur.fetchone()[0] if cur.fetchone() else "N/A"
#     return top_selling_product
# def profit_daily():
#     with connect_db() as con:
#             with con.cursor() as cur:
#              cur.execute("SELECT SUM(selling_price - buying_price) FROM products WHERE DATE(sale_date) = CURDATE()")
#              profit_today = cur.fetchone()[0] or 0
#     return profit_today
# def sales_daily():
#     with connect_db() as con:
#             with con.cursor() as cur:        
#              cur.execute("SELECT SUM(selling_price * quantity) FROM products WHERE DATE(sale_date) = CURDATE()")
#              sales_today = cur.fetchone()[0] or 0
#     return sales_today

def total_sales():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT SUM(products.selling_price * sales.quantity)
                FROM sales
                JOIN products ON sales.product_id = products.product_id
            """)
            total_sale = cur.fetchone()[0] or 0
    return total_sale

def total_profits():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT SUM((products.selling_price - products.buying_price) * sales.quantity)
                FROM sales
                JOIN products ON sales.product_id = products.product_id
            """)
            total_profit = cur.fetchone()[0] or 0
    return total_profit

def top_selling():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT products.product_name, SUM(sales.quantity) as total_quantity
                FROM sales
                JOIN products ON sales.product_id = products.product_id
                GROUP BY products.product_name
                ORDER BY total_quantity DESC
                LIMIT 1
            """)
            result = cur.fetchone()
            top_selling_product = result[0] if result else "N/A"
    return top_selling_product

def profit_daily():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT SUM((products.selling_price - products.buying_price) * sales.quantity)
                FROM sales
                JOIN products ON sales.product_id = products.product_id
                WHERE DATE(sales.created_at) = CURRENT_DATE
            """)
            profit_today = cur.fetchone()[0] or 0
    return profit_today

def sales_daily():
    with connect_db() as con:
        with con.cursor() as cur:
            cur.execute("""
                SELECT SUM(products.selling_price * sales.quantity)
                FROM sales
                JOIN products ON sales.product_id = products.product_id
                WHERE DATE(sales.created_at) = CURRENT_DATE
            """)
            sales_today = cur.fetchone()[0] or 0
    return sales_today
