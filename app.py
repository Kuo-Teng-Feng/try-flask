from __future__ import with_statement
import sqlite3
import datetime
from flask import Flask, redirect, render_template, request
from flask_mail import Mail, Message
#from flask_bootstrap import Bootstrap
from inicancelpath import ini
from data import listcancelpaths, cancelOrderAndUdInventory, mkOrderUdInventory, getCancelFrom, mkWish

app = Flask(__name__)

infolst = []
#with open("./static/mailsender.txt", "r") as file: # but must use url_for in .html with flask.
with open("../for_try-flask/mailsender.txt", "r") as file: # but must use url_for in .html with flask.
    for line in file:
        infolst.append(line.strip())
app.config["MAIL_DEFAULT_SENDER"] = infolst[0]
app.config["MAIL_PASSWORD"] = infolst[1]
app.config["MAIL_PORT"] = int(infolst[2]) # type.
app.config["MAIL_SERVER"] = infolst[3]
app.config["MAIL_USE_SSL"] = True # SSL instead TLS
app.config["MAIL_USERNAME"] = infolst[4]
mail = Mail(app)

home = 'http://127.0.0.1:5000/'
onewordpass = ''
#with open("./static/dontreadme.txt", "r") as file:
with open("../for_try-flask/dontreadme.txt", "r") as file:
    onewordpass += file.read()
shifts = ["8:00 ~ 10:00", "10:00 ~ 12:00", "12:00 ~ 14:00", "14:00 ~ 16:00", "16:00 ~ 18:00"]
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
the_day_after_tomorrow = tomorrow + datetime.timedelta(days=1)
src_for_coming_soon = "https://s.yimg.com/ny/api/res/1.2/Jyx.0_PgY4c2sIqYMtsB5g--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTQyNw--/https://s.yimg.com/uu/api/res/1.2/lRSnT5qr.E8v0OpWJ7glHg--~B/aD02ODM7dz0xMDI0O2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/ko/news_ttv_com_tw_433/7bb7c79ab5517e83cc6b2a4d61fe3a55"
# add pics for coming soon in static

o = {} # operator

con = sqlite3.connect("product.db")
cur = con.cursor()

res = cur.execute("SELECT name, ingradients, num FROM future_product")
future_product = res.fetchone() # mk room for list later
future_product_name = future_product[0]
future_product_ingradients = future_product[1]
o['future_product_num'] = future_product[2]
o['wish_num'] = -1;

res = cur.execute("SELECT id, name, ingradients, src, alt, num FROM now_product")
now_product = res.fetchone() # mk room for list later
o['now_product_id'] = now_product[0]
o['now_product_name'] = now_product[1]
now_product_ingradients = now_product[2]
now_product_src = now_product[3]
now_product_alt = now_product[4]
o['now_product_num'] = now_product[5]

cur.close()
con.close()

def loginsetter(): # for unittest etc.
    
    o['login'] = True
    
def logoutsetter(): # for unittest etc.
    
    o['login'] = False

@app.route("/") # decorator
def index():
    
    o['login'] = False # important!
    return render_template(
        "0.html",
        src_for_coming_soon = src_for_coming_soon,
        future_product_name = future_product_name,
        future_product_ingradients = future_product_ingradients,
        now_product_num = o['now_product_num'],
        now_product_src = now_product_src,
        now_product_alt = now_product_alt,
        now_product_name = o['now_product_name'],
        now_product_ingradients = now_product_ingradients
        )

@app.route("/loggingin", methods=["POST", "GET"]) # decorator
def loggingin():
    
    if request.method == "GET" and o['login'] == True: # wish_num input, reload or redirect.
        wish_dealer()
        return loggedin()
    if request.method == "POST" and request.form.get("one_word") == onewordpass:
        #o['login'] = True # relocated to loggedin()
        return loggedin()
    o['login'] = False # important! (wrong pass or session breaks.)
    return redirect("/")

def wish_dealer():
    
    wish_num = request.args.get("wish_num") # str.
    if request.args.get("wish_revoke"):
        o['future_product_num'] -= o['wish_num']
        mkWish(future_product_name, o['future_product_num'])
        o['wish_num'] = -1
    if request.args.get("wish_num_submit"):
        o['future_product_num'] += int(wish_num) # type, again. = =
        mkWish(future_product_name, o['future_product_num'])
        o['wish_num'] = int(wish_num)

def loggedin():

    o['login'] = True # relocated from loggingin()
    return render_template(
        "1.html",
        src_for_coming_soon = src_for_coming_soon,
        future_product_name = future_product_name,
        future_product_ingradients = future_product_ingradients,
        now_product_num = o['now_product_num'],
        now_product_src = now_product_src,
        now_product_alt = now_product_alt,
        now_product_name = o['now_product_name'],
        now_product_ingradients = now_product_ingradients,
        today = today,
        tomorrow = tomorrow,
        the_day_after_tomorrow = the_day_after_tomorrow,
        hrs = datetime.datetime.now().hour,
        wish_num = o['wish_num']
        )
    
@app.route("/pickup", methods=["POST", "GET"]) # decorator
def pickup():
    
    if o['login'] == False or o['login'] == None:
        return redirect("/")
    
    pickup_date = request.form.get("pickup_date")
    now_num = request.form.get("now_num") # str.
    o['pickup_date'] = pickup_date
    o['now_num'] = int(now_num) # str to int.
    actual_shifts = []
    hrs = datetime.datetime.now().hour
    if "oday" in pickup_date:
        if hrs < 16:
            for ele in shifts:
                if hrs > int(ele[:ele.index(":")]): 
                    continue
                actual_shifts.append(ele)
        else:
            actual_shifts = ["16:00 ~ 18:00"]
    elif "Pr" in pickup_date: # force to choose.
        return loggedin()
    else:
        actual_shifts = shifts
        
    return render_template(
        "11.html",
        src_for_coming_soon = src_for_coming_soon,
        future_product_name = future_product_name,
        future_product_ingradients = future_product_ingradients,
        now_product_num = o['now_product_num'],
        now_product_src = now_product_src,
        now_product_alt = now_product_alt,
        now_product_name = o['now_product_name'],
        now_product_ingradients = now_product_ingradients,
        now_num = now_num,
        pickup_date = pickup_date,
        actual_shifts = actual_shifts,
        wish_num = o['wish_num']
        )
    
@app.route("/completing", methods=["POST"]) # decorator
def completing():

    if o['login'] == False or o['login'] == None:
        return redirect("/")

    o['now_product_num'] -= o['now_num'] # type!
    o['contact'] = request.form.get("contact")
    o["phone"] = request.form.get("phone")
    pickup_time = request.form.get("pickup_time")
    if "~" in pickup_time:
        o['pickup_time'] = pickup_time
    else: # with no specific time chosen.
        o['pickup_time'] = "before 18:00"
    actualtitle = request.form.get("title")
    if actualtitle == None or len(actualtitle.strip()) == 0:
        o['title'] = "Stranger"
    else:
        o['title'] = actualtitle

    pickup_date = o['pickup_date'] # str.
    f_pickup_date = today # date
    if "today" in pickup_date: # str.
        pass
    elif "after" in pickup_date:
        f_pickup_date += datetime.timedelta(days=2)
    else: 
        f_pickup_date += datetime.timedelta(days=1)
    o['cancelpath'] = ini(4, today, tomorrow, the_day_after_tomorrow)
    
    mkOrderUdInventory(today, f_pickup_date, o)
    try:
        email("Your preorder at Mountain Sharp Stone", # title
              "<p>Dear "+ o['title'] + ", you have " + 
              str(o['now_num']) + " " + o['now_product_name'] + 
              " to pick up <strong>" + o['pickup_date'] + ", " +
              o['pickup_time'] + 
              "</strong>.</p><p>If you need to cancel this order, please use the cancelpath for this order alone <strong>" + 
              o['cancelpath'] + f"</strong> <a href = '{home}cancel'>here</a>.</p>",  
              [o['contact']]) # lst.
    except:
        pass
    
    return render_template(
        "2.html",
        src_for_coming_soon = src_for_coming_soon,
        future_product_name = future_product_name,
        future_product_ingradients = future_product_ingradients,
        now_product_num = o['now_product_num'], # update.
        now_product_src = now_product_src,
        now_product_alt = now_product_alt,
        now_product_name = o['now_product_name'],
        now_product_ingradients = now_product_ingradients,
        now_num = o['now_num'], 
        pickup_date = o['pickup_date'],
        title = o['title'],
        pickup_time = o['pickup_time']
        )  

def email(sms, html, tolst):
    
    message = Message(sms, recipients = tolst)
    message.html = html
    mail.send(message)
        
# cancel
@app.route("/cancel")
def canceling():
    
    return render_template("29.html")

@app.route("/cancelled", methods=["POST"])
def cancelled():
    
    cancelpath = request.form.get("cancelpath")
    if cancelpath in listcancelpaths(today, tomorrow, the_day_after_tomorrow): # datetime objects.
        try:
            email("Your cancellation", "Your preorder is already cancelled with " + cancelpath + ".", [getCancelFrom(cancelpath)])
        except:
            pass
        cancelOrderAndUdInventory(cancelpath) # after email().
        return render_template(
            "3.html",
            cancelpath = cancelpath
            )
    if cancelpath == "test":
        return render_template(
            "3.html",
            cancelpath = "...Nope. Sorry, it's just a test. Pls try again."
            )
    return redirect("/cancel") # 'return' is needed.

        