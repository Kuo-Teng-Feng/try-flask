import sqlite3
    
def listcancelpaths(today, tomorrow, the_day_after_tomorrow): # datetime objects

    con = sqlite3.connect("product.db")
    cur = con.cursor()    
    res = cur.execute("SELECT cancelpath FROM preorder WHERE pickup_date = ? OR pickup_date = ? OR pickup_date = ?", (today.strftime('%Y-%m-%d'), tomorrow.strftime('%Y-%m-%d'), the_day_after_tomorrow.strftime('%Y-%m-%d')))
    lst = res.fetchall()
    postfix = []
    if len(lst) > 0: # !
        for tp in lst:
            postfix.append(tp[0])
    cur.close()
    con.close()
    return postfix

def mkOrderUdInventory(today, f_pickup_date, o): # datetime object x 2, dict.
    
    con = sqlite3.connect("product.db")
    cur = con.cursor()
    cur.execute("INSERT INTO preorder(opendate, pickup_date, pickup_time, name, contact, phone, product_id, num, cancelpath) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (today, f_pickup_date, o["pickup_time"], o["title"], o["contact"], o["phone"], o['now_product_id'], o['now_num'], o['cancelpath']))
    cur.execute("UPDATE now_product SET num = ? WHERE id = ?", (o['now_product_num'], o['now_product_id']))
    con.commit()
    cur.close()
    con.close()

def cancelOrderAndUdInventory(cancelpath):

    con = sqlite3.connect("product.db")
    cur = con.cursor()    
    res = cur.execute("SELECT num, product_id FROM preorder WHERE id > ? AND cancelpath = ?", ("0", cancelpath)) # str. Why placeholders '?' must be more than one??
    temp = res.fetchone()
    productId = str(temp[1]) # int to str.
    res = cur.execute("SELECT num FROM now_product WHERE id = ? AND num > ?", (productId, "-100"))
    new_num = res.fetchone()[0] + temp[0]
    cur.execute("UPDATE now_product SET num = ? WHERE id = ?", (str(new_num), productId))
    cur.execute("DELETE FROM preorder WHERE id > ? AND cancelpath = ?", ("0", cancelpath)) # type.
    con.commit()
    cur.close()
    con.close()
    
def getCancelFrom(cancelpath):
    
    con = sqlite3.connect("product.db")
    cur = con.cursor()    
    res = cur.execute("SELECT contact FROM preorder WHERE id > ? AND cancelpath = ?", ("0", cancelpath)) # str. Why placeholders '?' must be more than one??
    ans = res.fetchone()[0] # trans. from ans is needed.
    cur.close()
    con.close()
    return ans

def mkWish(name, n):
    
    con = sqlite3.connect("product.db")
    cur = con.cursor()      
    cur.execute("UPDATE future_product SET num = ? WHERE name = ?", (n, name))
    con.commit()
    cur.close()
    con.close()    