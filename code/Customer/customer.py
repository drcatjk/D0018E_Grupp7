from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import pymysql
import sys
customer_bp = Blueprint('customer', __name__, 
                        template_folder='templates',
                        static_folder='static')



@customer_bp.route("/", methods=["GET", "POST"])
def customer():
    connection = pymysql.connect(host='localhost',          #apparently connection cannot be global or pymysql commits die
                            user='root',
                            password='bingus',
                            database='mydb',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT pro_name, pro_img, pro_info, price, pro_ID FROM Products"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result, file=sys.stderr)
    connection.close()
    return render_template("CusMain.html", title= "Customer Main", products = result)

@customer_bp.route("/enter", methods=["GET", "POST"])
def enterProduct():
    if "pro_ID" in request.form:
        currID = request.form['pro_ID']
        session['pro_ID'] = currID
        print(currID, file=sys.stderr)
        return redirect(url_for("customer.product"))
    else:
        return redirect(url_for("customer.customer"))
    
@customer_bp.route("/product", methods=["GET", "POST"])
def product():
    connection = pymysql.connect(host='localhost',
                        user='root',
                        password='bingus',
                        database='mydb',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT * FROM Products WHERE pro_ID = " + session["pro_ID"]
    print(sql, file=sys.stderr)
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result, file=sys.stderr)
    connection.close()
    return render_template("CusProduct.html", title= "Customer Product", product = result)


