import unittest
import sqlite3
import json
from flask import Flask, jsonify
from inicancelpath import randomizer
from app import app, loginsetter

class Test_randomizer(unittest.TestCase):    
    # n-digit.
    def test_randomizer_4(self): # prefix "test_" is necessary.      
        self.assertEqual(len(randomizer(4)), 4)
    
    def test_randomizer_30(self): #2
        self.assertEqual(len(randomizer(30)), 30)
        
    def test_randomizer_62(self): #3
        self.assertEqual(len(randomizer(62)), 62)
    
    def test_randomizer_99(self): #4
        self.assertEqual(len(randomizer(99)), 99)
        
    def test_randomizer_999(self): #5
        self.assertEqual(len(randomizer(999)), 999)

# database
dbnames = ['now_product', 'future_product', 'preorder']
now_product_col = ["id", "opendate", "name", "ingradients", "src", "alt", "num"]
future_product_col = ["name", "ingradients", "src", "alt", "num"]
preorder_col = ["id", "opendate", "pickup_date", "pickup_time", "name", "contact", "product_id", "num", "cancelpath", "phone"]

class Test_db_structure(unittest.TestCase):   
       
    def test_dbnames(self): #6
        
        con = sqlite3.connect("product.db")
        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        lst = res.fetchall()
        nlist = []
        if len(lst) > 0: 
            for tp in lst: # "tp" for "tuple"
                nlist.append(tp[0])
        cur.close()
        con.close()
        for ele in dbnames:
            if ele not in nlist:
                self.assertIn(ele, nlist)
        # default tested if here arrived 
        
    def test_now_product(self): #7

        con = sqlite3.connect("product.db")
        cur = con.cursor()
        res = cur.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'now_product'")
        comm = res.fetchone()[0] #sql command.
        cur.close()
        con.close()
        for ele in now_product_col:
            if ele not in comm:
                self.assertIn(ele, comm)

    def test_future_product(self): #8

        con = sqlite3.connect("product.db")
        cur = con.cursor()
        res = cur.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'future_product'")
        comm = res.fetchone()[0]
        cur.close()
        con.close()
        for ele in future_product_col:
            if ele not in comm:
                self.assertIn(ele, comm)
                
    def test_preorder(self): #9

        con = sqlite3.connect("product.db")
        cur = con.cursor()
        res = cur.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'preorder'")
        comm = res.fetchone()[0]
        cur.close()
        con.close()
        for ele in preorder_col:
            if ele not in comm:
                self.assertIn(ele, comm)
                
class Test_db_validity(unittest.TestCase):
    
    def test_now_product(self): #10
        
        con = sqlite3.connect("product.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM now_product")
        lst = res.fetchall() #list of tuples
        cur.close()
        con.close()
        for tp in lst:
            leng = len(tp)
            for i in range(0, leng):
                ele = tp[i]
                if str(ele) == "" or ele == None:
                    self.assertEqual(ele, f"{now_product_col[i]} of {tp[0]}, {tp[2]}")

    def test_future_product(self): #11
        
        con = sqlite3.connect("product.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM future_product")
        lst = res.fetchall() #list of tuples
        cur.close()
        con.close()
        for tp in lst:
            leng = len(tp)
            for i in range(0, leng):
                ele = tp[i]
                if str(ele) == "" or ele == None:
                    self.assertEqual(ele, f"{future_product_col[i]} of {tp[0]}, {tp[2]}")

    def test_preorder(self): #12
        
        con = sqlite3.connect("product.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM preorder")
        lst = res.fetchall() #list of tuples
        cur.close()
        con.close()
        for tp in lst:
            leng = len(tp)
            for i in range(0, leng - 1): # 'phone' can be empty.
                ele = tp[i]
                if str(ele) == "" or ele == None:
                    self.assertEqual(ele, f"{preorder_col[i]} of {tp[2]}, {tp[5]}")
        
class Test_web(unittest.TestCase):
    
    def setUp(self): 
        
        self.app = app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index(self): #13
        
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_cancel(self): #14
        
        res = self.client.get("/cancel")
        self.assertEqual(res.status_code, 200)
            
    def test_login(self): #15
        
        onewordpass = ''
        with open("../for_try-flask/dontreadme.txt", "r") as file:
            onewordpass += file.read()
        
        res = self.client.post("/loggingin", data = {"one_word" : onewordpass}) 
        self.assertEqual(res.status_code, 200)
        
    def test_login_failure_redirect(self): #16
         
        res = self.client.post("/loggingin", data = {}) 
        self.assertEqual(res.status_code, 302)
        self.assertIn('href="/"', res.text)
    
    #def test_counter(self): #
        
    #   res = self.client.post("/cancelled", data=json.dumps({"cancelpath" : "whatever"}))
    #    self.assertEqual(res.status_code, 200)
        
    
    
        

if __name__ == "__main__":
    unittest.main()