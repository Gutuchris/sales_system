from dbservice import get_data,insert_product,insert_sales,calc_profit,create_users,email_pass,email_and_pas
from flask import Flask,render_template,request,redirect,session,url_for



 
app=Flask(__name__)


# def login_check():
#     if session['email'] != None:
#         return redirect(url_for('dashbord'))
#     return redirect(url_for('user_login'))




@app.route("/")
def sales_system():
     return render_template("home.html")


@app.route("/add-product" , methods=["POST"])
def add_product():
    pn = request.form['name']
    bp = request.form['buying_price']
    sp = request.form['selling_price']
    sq = request.form['stock_quantity']

    stored_var=(pn,bp,sp,sq)
    insert_product(stored_var)

    return redirect("/products")

@app.route("/products")
def product():
    prod = get_data("products")
    return render_template("products.html",myproducts=prod)

@app.route("/add-sale" , methods=["POST"])
def add_sales():
     productid=request.form["productid"]
     quantity = request.form['quantity']  
     store_sale=(productid,quantity,'now()')
     insert_sales(store_sale)

     return redirect("/sales")

@app.route("/sales")
def sales():
     sale=get_data("sales")
     prd=get_data("products")
     return render_template("sales.html",mysales=sale , myprd=prd)

@app.route("/dashboard")
def dashboard():
     # login_check()
     dates = []
     profits = []
     for i  in calc_profit():
        dates.append(str(i[0]))
        profits.append(float(i[1]))

     return render_template("dashboard.html" ,dates=dates,profits=profits)



@app.route("/register", methods=['GET','POST'])
def user_register():
   if request.method=="POST":
     fn=request.form['full_name']
     em=request.form['email']
     ps=request.form['password']
     stored_value=(fn,em,ps)
     create_users(stored_value)

     return redirect(url_for("user_login"))

   return render_template("registration.html")



@app.route("/login" , methods=['GET','POST'])
def user_login():
   if request.method == 'POST': 
      m_email=request.form['email']
      m_pass=request.form['password']
      store=email_and_pas(m_email,m_pass)
      if store:
       session["userid"]=store[0]
       return redirect(url_for("dashboard"))
     
   return render_template("login.html")

#   if user_access:
          #  session['user_id'] = user_access
          # #  session['full_name'] = user_access[1]

app.run(debug=True)