from datetime import datetime
from random import *
import sqlite3
import os
conn = sqlite3.connect('DbBank4.db')
c = conn.cursor()
def account():
        os.system('cls')
        global d
        print("\t\t****SIGNING UP****\n")
        print("1.Enter your Fullname")
        FN = input()
        print("2.Enter your Password")
        pa = input()
        while len(pa)<6:
            print("Error:Password should be atleast 6 characters long")
            print("2.Enter your Password")
            pa = input()
        print("3.Re-Enter your Password")
        rpa = input()
        while True:
            if rpa != pa:
                print("Re-Enter your Password")
                rpa = input()
            else:
                break
        print("4.Enter your Address")
        add = input()
        print("5.Enter your City")
        city = input()
        print("6.Enter your State")
        state = input()
        print("7.Enter your Pin")
        pin = int(input())
        while len(str(pin))!=6:
            print("Error:Please enter valid Pincode")
            print("7.Enter your Pin")
            pin = input()
        print("8.Enter your Phone-number")
        pon = int(input())
        while len(str(pon))!=10:
            print("Error:Please enter valid Phone-number")
            print("8.Enter your Phone-number")
            pon = input()
        print("9.Enter your E-mail")
        email = input()
        flag=0;
        while flag==0:
          for i in email:
            if i == '@':
              flag=1;
          if flag==0:
            print("Error:Please enter valid E-mail")
            print("Enter your E-mail")
            email = input()
        print("10.Enter your Branch-name")
        BN = input()
        Date = datetime.now().strftime('%Y-%m-%d')
        print("We generated your Account ID:)")
        print("Date:",Date)
        d = randint(100000,999999) 
        print("Your ACCOUNT ID is ",d)
       
        c.execute("INSERT INTO BANK(Fullname,password,cpass,aline1,state,city,pin,phonenu,email,cid,branchname,creation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (FN, pa, rpa, add,city,state,pin,pon,email,d,BN,Date))
        conn.commit()
def withdraw(uid):
    amount=int(input("Enter Amount for Withdraw"))
    tp=c.execute("SELECT Type FROM AC WHERE id='%s'"%(uid))
    tk=tp.fetchall()
    for row in tk:
        tp=row
    print(tp)  
    if(tp==('saving',)):
        
        currentamount=c.execute("SELECT BALANCE FROM AC WHERE id='%s'"%(uid))
        y=currentamount.fetchall()
        for i in y:
            print(i)
        print(i[0])
        b=int(i[0])
        if((b-amount)>=0):
            total=b-amount
            c.execute("UPDATE AC SET BALANCE='%d' WHERE id='%s'"%(total,uid))
            print("Transcation done")
            Date=datetime.now().strftime('%Y-%m-%d')
            c.execute("INSERT INTO transaction2(cid, money, date, total) VALUES (?,?,?,?)" ,(uid,amount,Date,total))
            conn.commit()
        else:
            print("Insufficent Balance")
            return 0
    elif(tp==('current',)):
        
        currentamount=c.execute("SELECT BALANCE FROM AC WHERE id='%s'"%(uid))
        y=currentamount.fetchall()
        for i in y:
            print(i)
        print(i[0])
        b=int(i[0])
        if((b-amount)>5000):
            
            total=currentamount-amount
            c.execute("UPDATE AC SET BALANCE='%s' WHERE id='%s'"%(total,uid))
            c.execute("INSERT INTO transaction2(cid, money, date, total) VALUES (?,?,?,?)" ,(uid,amount,Date,total))
            print("Transcation done")
            conn.commit()
        else:
            print("Insufficent Balance")
            return 0
    else:
        
        return 0
def deposit(uid):
    amount=int(input("Enter Amount for Deposit"))
    currentamount=c.execute("SELECT BALANCE FROM AC WHERE id='%s'"%(uid))
    y=currentamount.fetchall()
    for i in y:
        print(i)
    b=int(i[0])
    total=b+amount
    c.execute("UPDATE AC SET BALANCE='%s' WHERE id='%s'"%(total,uid))
    Date=datetime.now().strftime('%Y-%m-%d')
    c.execute("INSERT INTO transaction2(cid, money, date, total) VALUES (?,?,?,?)" ,(uid,amount,Date,total))       
    print("Transcation done")
    conn.commit()
def AdressChange(uid):
    try:
        addr=input("Enter New Address ")
        state=input("Enter New State ")
        city=input("Enter New City ")
        pin=int(input("Enter New Pincode "))
        c.execute("UPDATE BANK SET aline1='%s' WHERE cid='%s'"%(addr,uid))
        c.execute("UPDATE BANK SET state='%s' WHERE cid='%s'"%(state,uid))
        c.execute("UPDATE BANK SET city='%s' WHERE cid='%s'"%(city,uid))
        c.execute("UPDATE BANK SET pin='%d' WHERE cid='%s'"%(pin,uid))
        print("Succesfully Change")
        conn.commit()
    except:
        print(e)
    return
def login():
    jem=0
    jam=0
    id=int(input("Enter Login Id"))
    row=c.execute("select cid from BANK")
    tp=row.fetchall()
    for i in tp:
        print(i[0])
        if id==int(i[0]):
            print(id)
            jem=1
    if jem==1:
        password=input("Enter your password")
        row=c.execute("select password from BANK WHERE cid='%d'"%(id))
        tp=row.fetchall()
        for i in tp:
            print(i[0])
            if password==str(i[0]):
                jam=1
                    
        if jam==1:
            print("Which type of account do you want to open?")
            account=int(input("1.Savings Account\n2.Current Account\n"))
            if account==1:
                        am=int(input("Enter initial opening money\n"))
                        v="saving"
                        print("You succsessfully open your account in our bank:)")
                        c.execute("INSERT INTO AC (id,Type,Balance) VALUES (?,?,?)",(id,v,am))
                        conn.commit()
            if account==2:
                        am=int(input("enter your money"))
                        while am<5000:
                            print("Error:As per our scheme you must have to insert minimum 5000/- as a initial money")
                            am=int(input("enter your money"))
                        v="current"
                        c.execute("INSERT INTO AC (id,Type,Balance) VALUES (?,?,?)",(id,v,am))
                        print("You succsessfully open your account in our bank:)")
                        conn.commit()
        else:
            print("incorrect password")
                    
    else:
            print("do not have account")
                
        
def Transfer():
    os.system('cls')
    print("\t\t****MONEY TRANSFER****\n")
    jem=0
    jam=1
    print("enter your c-id")
    id1=int(input("Enter Login Id\n"))
    row=c.execute("select cid from BANK")
    tp=row.fetchall()
    for i in tp:
        if id1==int(i[0]):
            jam=1
    if jam==1:
        password=input("Enter your password\n")
        row=c.execute("select password from BANK WHERE cid='%d'"%(id1))
        tp=row.fetchall()
        for i in tp:
            if password==str(i[0]):
                jem=1
        if jem==1:
            jam=0
            id=int(input("Enter your receiver cid\n"))
            row=c.execute("select cid from BANK")
            tp=row.fetchall()
            for i in tp:
                if id==int(i[0]):
                    jam=1
            if jam==1:
                am=int(input('enter money\n'))
                currentamount=c.execute("SELECT Balance FROM AC WHERE id='%s'"%(id))
                y=currentamount.fetchall()
                for i in y:
                    b=int(i[0])
                currentamount1=c.execute("SELECT Balance FROM AC WHERE id='%s'"%(id1))
                y1=currentamount1.fetchall()
                for i in y1:
                    b1=int(i[0])
                
                if am>b1:
                    return
                f=b1-am
                v=b+am
                Date=datetime.now().strftime('%Y-%m-%d')
                c.execute("INSERT INTO transaction2(cid, money, date, total) VALUES (?,?,?,?)" ,(id1,am,Date,f))
                c.execute("INSERT INTO transaction2(cid, money, date, total) VALUES (?,?,?,?)" ,(id,am,Date,v))
                c.execute("UPDATE AC SET Balance='%d' WHERE id='%d'"%(f,id1))
                c.execute("UPDATE AC SET Balance='%d' WHERE id='%d'"%(v,id))
                conn.commit()
                print("Success")
    
        else:
            print("incorrct password")
            
        
    else:
        print("you do not have account")
   # Pick a random number between 1 and 100.

while True:
    os.system('cls')
    print("\t\t****WELCOME TO THE BANK****\n")
    print("Menu:")
    print("1.Sign Up\n2.Sign in\n3.Exit")
    i=int(input("Enter your choice\n"))
    if i==1:
        account()
        login()
    elif i==2:
        os.system('cls')
        print("\t\t****SIGNING IN****\n")
        id=int(input("Enter your Account Id\n"))
        row=c.execute("select cid from BANK")
        tp=row.fetchall()
        for i in tp:
            if id==int(i[0]):
                jam=1
                break
        if jam==1:
            password=int(input("Enter your password\n"))
            row=c.execute("select password from BANK")
            tp=row.fetchall()
            for i in tp:
                if password==i[0]:
                    jem=1
                    break
        else:
            print("incorrect")
        if jem==1:
            os.system('cls')
            print("You successfully login to you Account\n")
            print("\t\t****MY ACCOUNT****\n")
            print("Menu:\nEnter your choice")
            print("1.Withdraw Money\n2.Deposit Money\n3.Transfer Money\n4.Address-Change")
            i=int(input("Enter your Choice\n"))
            if i==1:
                withdraw(id)
            elif i==2:
                deposit(id)
            elif i==3:
                Transfer()
            elif i==4:
                AdressChange(id)
        else:
             print("incorrect")
    elif i==3:
        exit(0)
        

