import sqlite3
import datetime
#from browser_test import NO_sessionStorage_involved

# today.strftime('%Y-%m-%d'), "2022-10-16"
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
the_day_after_tomorrow = tomorrow + datetime.timedelta(days=1)
con = sqlite3.connect("product.db")
cur = con.cursor()
#cur.execute("CREATE TABLE preorder(id INTEGER PRIMARY KEY AUTOINCREMENT, opendate TEXT, pickup_date TEXT, pickup_time TEXT, name TEXT, contact TEXT, product_id INTEGER, num INTEGER)")
#cur.execute("DROP TABLE preorder")
#con.commit()
#cur.execute("ALTER TABLE preorder ADD phone")
#con.commit()
#cur.execute("INSERT INTO preorder(opendate, pickup_date, pickup_time, name, contact, product_id, num) VALUES(?, ?, ?, ?, ?, ?, ?)", (today, today, "testtime", "testname", "test@g", 1, 1))
#cur.execute("UPDATE now_product SET num = ? WHERE id = ?", (50, 1))
#cur.execute("DELETE FROM preorder WHERE id > 23")
con.commit()
#res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
#print(res.fetchall())
res = cur.execute("SELECT id, cancelpath FROM preorder WHERE id > 10")
#print(res.fetchall())
#res = cur.execute("SELECT num FROM now_product")
#print(res.fetchone())
#print(res.fetchall())
cur.close()
con.close()
#print(NO_sessionStorage_involved())
