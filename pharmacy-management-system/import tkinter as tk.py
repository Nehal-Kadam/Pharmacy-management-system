import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from tkinter import *
def deletefun(event):
connection = pymysql.connect(
host='localhost',
user='root',
db='stude',
)
rno=int(ro.get())
print(rno)
try:
cursor=connection.cursor()
sql = "delete from student where rno='%d'"
try:
args=(rno)
cursor.execute(sql%args)
except:
print("Oops! Something wrong")
connection.commit()
finally:
connection.close()
def addfun(event):
connection = pymysql.connect(
host='localhost',
user='root',
db='stude',
)
rno=int(ro.get())
print(rno)
name=n.get()
print(name)
try:
cur=connection.cursor()
sql = "INSERT INTO student (rno,name) VALUES ('%d','%s')"
args=(rno,name)
print(args)
try:
cur.execute(sql%args)
print("added successfully")
except:
print("oops something wrong")
connection.commit()
finally:
connection.close()
def read(event):
connection = pymysql.connect(
host='localhost',
user='root',
db='stude',
)
try:
cursor=connection.cursor()
sql = "select * from student"
try:
cursor.execute(sql)
res=cursor.fetchall()
for i in res:
print(f'{i[0]}\t\t {i[1]}')
except:
print("Oops! Something wrong")
connection.commit()
finally:
connection.close()
def updatefun(event):
connection = pymysql.connect(
host='localhost',
user='root',
db='stude',
)
rno=int(ro.get())
print(rno)
name=n.get()
print(name)
try:
cursor=connection.cursor()
sql = "UPDATE student SET name='%s' WHERE rno = '%d' "
args=(name,rno)
try:
cursor.execute(sql%args)
print("Successfully Updated...")
except:
print("Oops! Something wrong")
connection.commit()
finally:
connection.close()
window=Tk()
window.title('Hello Python')
window.geometry("400x400+10+10")
lbl=Label(window, text="roll no", fg='red', font=("Helvetica", 16))
lbl.place(x=60, y=50)
ro=Entry(window,bd=5)
ro.insert(0,"enter roll no")
ro.place(x=180, y=50)
lbl=Label(window, text="name", fg='red', font=("Helvetica", 16))
lbl.place(x=60, y=80)
n=Entry(window,bd=5)
n.insert(0,"enter name")
n.place(x=180, y=80)
btn=Button(window, text="update_record", fg='blue')
btn.place(x=200, y=150)
btn.bind('<Button-1>', updatefun)
btn=Button(window, text="Add record", fg='blue')
btn.place(x=200, y=200)
btn.bind('<Button-1>', addfun)
btn=Button(window, text="read record", fg='blue')
btn.place(x=200, y=250)
btn.bind('<Button-1>', read)
btn=Button(window, text="delete record", fg='blue')
btn.place(x=200, y=300)
btn.bind('<Button-1>', deletefun)
window.mainloop()
