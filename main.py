from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_service import get_data, add_product as db_add_product, make_sale as db_make_sale, fetch_all_products, calculate_sales_per_product, calculate_profit_per_product, add_user, check_email_exists, check_email_password_match, calculate_sales_per_day,calculate_profit_per_day,total_products,total_sales,total_profits,top_selling,profit_daily,sales_daily
app = Flask(__name__)
app.secret_key = "Helloworld"

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/products')
def products():
    products_data = get_data("products")
    return render_template("products.html", myproducts=products_data)

@app.route("/add_products", methods=["GET", "POST"])
def add_product_route():
    if request.method == "POST":
        pn = request.form["product_name"]

        bp = request.form["buying_price"]
        sp = request.form["selling_price"]
        sq = request.form["stock_quantity"]

        db_add_product(pn, bp, sp, sq)
        flash("Product added successfully", "success")
        return redirect(url_for("products"))

    return render_template("add_product.html")

@app.route('/sales')
def sales():
    sales_data = get_data("sales")
    products = fetch_all_products()
    return render_template("sales.html", mysales=sales_data, products=products)

@app.route('/make_sales', methods=["GET", "POST"])
def add_sales_route():
    if request.method == "POST":
        product_id = request.form["product_id"]
        quantity = request.form["quantity"]
        db_make_sale(product_id, quantity)
        flash("Sale made successfully!", "success")
        return redirect(url_for("sales"))

    products = fetch_all_products()
    return render_template("sales.html", products=products, mysales=get_data("sales"))

@app.route('/dashboard')
def dashboard():
    p_name = []
    p_sales = []
    p_n = []
    p_s = []
    sale_p = calculate_sales_per_product()
    sale_q = calculate_profit_per_product()
    tp = total_products()
    ts = total_sales()
    tf = total_profits()
    tsp = top_selling()
    pd = profit_daily()
    sd = sales_daily()


    
    for i in sale_p:
        p_name.append(i[0])  # append product name to p_name list
        p_sales.append(float(i[1]))  # append sales amount to p_sales list

    for i in sale_q:
        p_n.append(i[0])  # append product name to p_n list
        p_s.append(float(i[1]))  # append profit amount to p_s list
    
    #sales per day on a line chart 

        ds=calculate_sales_per_day()
        day=[]
        sl=[]

    for i in ds:
        day.append(str(i[0]))
        sl.append(float(i[1]))

        dp=calculate_profit_per_day()
        day=[]
        profit=[]

    for i in dp:
        day.append(str(i[0]))
        profit.append(float(i[1]))


    return render_template("dashboard.html", p_name=p_name, p_sales=p_sales, p_n=p_n, p_s=p_s, day=day,sl=sl, profit=profit,tp=tp,ts=ts,tf=tf,tsp=tsp,pd=pd,sd=sd)

@app.route('/more')
def more():
    return render_template("more.html")

@app.route('/register', methods=['GET', 'POST'])
def reg():
    if request.method == "POST":
        fn = request.form["full_name"]
        em = request.form["email"]
        pas = request.form["password"]

        if not check_email_exists(em):
            add_user(fn, em, pas)
            flash(f"Account created successfully, Welcome, {fn}", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Email already exists. Please use a different email or login to your account.", "error")
            return redirect(url_for('log'))

    return render_template("registration.html")

@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == "POST":
        em = request.form["email"]
        pas = request.form["password"]

        full_name = check_email_password_match(em, pas)

        if full_name:
            session['user_name'] = full_name
            flash(f'Login Successful, Welcome {full_name}', 'success')
            return redirect(url_for("dashboard"))

        elif check_email_exists(em):
            flash("Invalid login credentials. Please try again.", 'error')
            return redirect(url_for("log"))

        else:
            flash("Email not found. Please register.", 'error')
            return redirect(url_for("reg"))

    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
