from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = "food application"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'food'

mysql = MySQL(app)

app.config["UPLOAD_FOLDER"] = 'static/assets/'

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from Product")
    data = cursor.fetchall()
    cursor.close()
    return render_template("index.html",data=list(data))

@app.route("/<cat>")
def category_vise(cat):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from Product WHERE category = %s",(cat,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("index.html",data=list(data))

@app.route("/cart")
def cart():
    if "email" not in session:
        flash("Please, login first")
        return redirect(url_for("sign_in"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT cart.id,product.photo,product.name,product.price,cart.quantity FROM cart JOIN product ON cart.product_id = product.id WHERE cart.user_id = %s",(session["id"],))
        data = cursor.fetchall()
        cursor.execute("SELECT SUM(product.price * cart.quantity),(COUNT(product_id) * 50),(SUM(product.price * cart.quantity) + (COUNT(product_id) * 50)) FROM cart JOIN product ON product.id = cart.product_id WHERE user_id = %s",(session["id"],))
        cart_det = cursor.fetchone()
        cursor.close()
        return render_template("cart.html",data=data,cart_det=cart_det)
    
@app.route("/cart_delete/<int:id>/")
def cart_delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM cart WHERE id = %s",(id,))
    mysql.connection.commit()
    flash("Removed from cart")
    return redirect(url_for("cart"))
    
@app.route("/food/<int:id>/")
def food_info(id):
    if "email" not in session:
        flash("Please, login first")
        return redirect(url_for("sign_in"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM product WHERE id = %s",(id,))
        data = cursor.fetchone()
        return render_template("foodinfo.html",data=data)

@app.route("/add_cart",methods=["GET","POST"])
def add_cart():
    data = request.form
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO cart ( user_id, product_id, quantity) VALUES (%s,%s,%s)",(session["id"],data["pid"],data["quantity"]))
    mysql.connection.commit()
    flash("Added to cart")
    return redirect(url_for("cart"))


@app.route("/cart_edit/<int:id>/")
def cart_edit(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT cart.id,product.photo,product.name,product.price,cart.quantity,product.description,product.category FROM cart JOIN product ON cart.product_id = product.id WHERE cart.user_id = %s AND cart.id = %s",(session["id"],id))
    data = cursor.fetchone()
    return render_template("editcart.html",data=data)    
    
@app.route("/edit_cart",methods=["GET","POST"])
def edit_cart():
    data = request.form
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE cart SET quantity = %s WHERE id = %s",(data["quantity"],data["cid"]))
    mysql.connection.commit()
    flash("Cart Edited")
    return redirect(url_for("cart"))

@app.route("/checkout",methods=["GET","POST"])
def checkout():
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT SUM(product.price * cart.quantity),(COUNT(product_id) * 50),(SUM(product.price * cart.quantity) + (COUNT(product_id) * 50)) FROM cart JOIN product ON product.id = cart.product_id WHERE user_id = %s",(session["id"],))
        cart_det = cursor.fetchone()
        if cart_det[0] == None :
            flash("Enable to checkout")
            return redirect(url_for("cart"))
        else:
            return render_template("checkout.html",cart_det=cart_det)
    else:
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id,product_id,quantity,((SELECT price FROM product WHERE id = product_id) * (quantity)) FROM cart WHERE user_id = %s",(session["id"],))
        cartdatas = cursor.fetchall()
        for cartdata in cartdatas :
            insertquery = "INSERT INTO orders (user_id,product_id,quantity,price,address,city,state,zip_code,country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(insertquery,(session["id"],cartdata[1],cartdata[2],(cartdata[3] + 50),data["address"],data["city"],data["state"],data["zip"],data["country"]))
            cursor.execute("DELETE FROM cart WHERE id = %s ",(cartdata[0],))
            mysql.connection.commit()
        cursor.close()
        return redirect(url_for("orders"))

@app.route("/orders")
def orders():
    if "email" not in session:
        flash("Please, login first")
        return redirect(url_for("sign_in"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT (SELECT photo FROM product WHERE id = product_id),(SELECT name FROM product WHERE id = product_id),price,quantity,status FROM orders WHERE user_id = %s ORDER BY order_date DESC",(session["id"],))
        orderdata = cursor.fetchall()
        cursor.close()
        return render_template("orders.html",orders=orderdata)

@app.route("/sign_in",methods=["GET","POST"])
def sign_in():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("select email,password,id from users WHERE email = %s",(data["email"],))
        record = cursor.fetchone()
        cursor.close()
        if record :
            if data["email"] == record[0] and data["password"] == record[1] :
                session["id"] = record[2]
                session["email"] = data["email"]
                session["password"] = data["password"]
                return redirect(url_for("index"))
            elif data["email"] == record[0] and data["password"] != record[1]:
                flash("Password Wrong")
                return redirect(url_for("sign_in"))
            else:
                flash("Unknown error")
                return redirect(url_for("sign_in"))
        elif data["email"]=="admin@gmail.com" and data["password"]=="admin@123":
                session["admin"] = data["email"]
                return redirect(url_for("admin_home"))
        else:
            flash("Account not found")
            return redirect(url_for("sign_in"))
        
@app.route("/logout")
def logout():
    session.pop("email",None)
    session.pop("password",None)
    return redirect(url_for("sign_in"))

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        data = request.form
        cursor = mysql.connection.cursor()
        query = "INSERT INTO Users (name, email, phone, password) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(data["name"],data["email"],data["phone"],data["password"]))
        mysql.connection.commit()
        cursor.close()
        flash("Successfully Registered")
        return redirect(url_for("sign_in"))


@app.route("/admin_home",methods=["GET","POST"])
def admin_home():
    if "admin" in session:
        if request.method == "GET":
            return render_template("admin_home.html")
        else:
            data = request.form
            photo = request.files["photo"]
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"],photo.filename))
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO Product (name, photo, category, price, description) VALUES (%s,%s,%s,%s,%s);",(data["name"],photo.filename,data["category"],data["price"],data["desc"]))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("admin_items"))
    else:
        flash("Please, sign in as admin")
        return redirect(url_for("sign_in"))


@app.route("/admin_items")
def admin_items():
    if "admin" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("select * from Product")
        data = cursor.fetchall()
        cursor.close()
        return render_template("admin_items.html",data=list(data))
    else:
        flash("Please, sign in as admin")
        return redirect(url_for("sign_in"))

@app.route("/delete/<int:id>")
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Product WHERE id = %s",(id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("admin_items"))

@app.route("/admin_orders")
def admin_orders():
    if "admin" in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT orders.id,product.photo,product.name,orders.quantity,orders.price,orders.address,orders.city,.orders.zip_code,orders.state,orders.country,(SELECT name FROM users WHERE id = user_id),orders.status FROM orders JOIN product WHERE orders.product_id = product.id ORDER BY order_date DESC")
        data = cursor.fetchall()
        return render_template("admin_orders.html",data=data)
    else:
        flash("Please, sign in as admin")
        return redirect(url_for("sign_in"))

@app.route("/order_update/<int:id>",methods=["GET","POST"])
def order_update(id):
    if request.method == "POST":
        data = request.form["status"]
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s",(data,id))
        mysql.connection.commit()
        return redirect(url_for("admin_orders"))

@app.route("/logout_admin")
def logout_admin():
    session.pop("admin",None)
    return redirect(url_for("sign_in"))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')