from tkinter import *
import time
import sqlite3
import random
import tempfile
import win32api
import win32print

f=''
flag=''
flags=''

login=sqlite3.connect("admin.db")
l=login.cursor()

c=sqlite3.connect("medicine.db")
cur=c.cursor()

columns=('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')

def open_win(): #OPENS MAIN MENU----------------------------------------------------------------------------MAIN MENU
    global apt, flag
    flag='apt'
    apt=Tk()
    apt.geometry("970x610")
    img = PhotoImage(file='4.png')
    label17 = Label(apt, image=img)
    label17.place(x=1, y=1)
    apt.title("MINI PROJECT")
    Label(apt, text="         SFIT PHARMACY MAIN MENU         ", bg="pink", fg="black", font="Verdana 30",width=30).grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=3,pady=9, padx=9, ipadx=100,ipady=5)


    Label(apt, text="Stock Maintenance", font="Verdana 12",bd=2, relief="solid").grid(row=2, column=0,pady=3, padx=3, ipadx=3,ipady=3)

    Button(apt,text='New V.C.',width=19, font="Verdana 12", command=val_cus).grid(row=4,column=0,pady=10, padx=10, ipadx=10,ipady=10)
    Button(apt,text='Add product to Stock',width=19, font="Verdana 12",command=stock).grid(row=5,column=0,pady=10, padx=10, ipadx=10,ipady=10)
    Button(apt,text='Delete product from Stock',width=19, font="Verdana 12",command=delete_stock).grid(row=6,column=0,pady=10, padx=10, ipadx=10,ipady=10)

    Label(apt, text="Access Database", font="Verdana 12",bd=2, relief="solid").grid(row=2, column=1,pady=5, padx=5, ipadx=5,ipady=5)

    Button(apt,text='Modify',width=19, font="Verdana 12",command=modify).grid(row=4,column=1,pady=10, padx=10, ipadx=10,ipady=10)
    Button(apt,text='Search',width=19, font="Verdana 12", command=search).grid(row=5,column=1,pady=10, padx=10, ipadx=10,ipady=10)
    Button(apt,text='Expiry Check',width=19, font="Verdana 12",command=exp_date).grid(row=6,column=1,pady=10, padx=10, ipadx=10,ipady=10)

    Label(apt, text="Handle Cash Flows", bd=2, font="Verdana 12",relief="solid").grid(row=2, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    Button(apt,text="Check Today's Revenue",width=19, font="Verdana 12",command=show_rev).grid(row=5,column=2,pady=10, padx=10, ipadx=10,ipady=10)
    Button(apt,text='Billing',width=19, font="Verdana 12",command=billing).grid(row=4,column=2,pady=10, padx=10, ipadx=10,ipady=10)

    Button(apt,text='Logout',command=again,font="Verdana 12",bg='red').grid(row=13, column=2,pady=10, padx=10, ipadx=10,ipady=10)

    apt.mainloop()

def delete_stock(): #OPENS DELETE WINDOW----------------------------------------------------DELETES A PARTICULAR STOCK ITEM
    global cur, c, flag, lb1, d
    apt.destroy()
    flag='d'
    d=Tk()
    d.geometry("800x430")
    img = PhotoImage(file='3.png')
    label17 = Label(d, image=img)
    label17.place(x=1, y=1)
    d.title("Delete a product from Stock")
    Label(d,text='Select Product to delete:',font="Verdana 12").grid(row=0,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    Label(d,text='Product',font="Verdana 10").grid(row=2,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    Label(d,text='Qty.  Exp.dt.     Cost                           ',font="Verdana 10").grid(row=2,column=1,pady=5, padx=5, ipadx=5,ipady=5)
    ren()
    b=Button(d,width=20,text='Delete',command=delt,font="Verdana 10").grid(row=0,column=3,pady=5, padx=5, ipadx=5,ipady=5)
    b=Button(d,width=20,text='Main Menu',command=main_menu,font="Verdana 10").grid(row=5,column=3,pady=5, padx=5, ipadx=5,ipady=5) 
    d.mainloop()

def ren():
    global lb1,d,cur,c
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(d,width=25, yscrollcommand=vsb.set)
    lb2=Listbox(d,width=30,yscrollcommand=vsb.set)
    vsb.grid(row=3,column=2,sticky=N+S)
    lb1.grid(row=3,column=0)
    lb2.grid(row=3,column=1)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        s1=[str(i[0]),str(i[1])]
        s2=[str(i[3]),str(i[6]),str(i[4])]
        lb1.insert(cx,'. '.join(s1))
        lb2.insert(cx,'   '.join(s2))
    c.commit()
    lb1.bind('<<ListboxSelect>>', sel_del)

def sel_del(e):
    global lb1, d, cur, c,p, sl2
    p=lb1.curselection()
    print (p)
    x=0
    sl2=''
    cur.execute("select * from med")
    for i in cur:
        print (x, p[0])
        if x==int(p[0]):
            sl2=i[0]
            break
        x+=1
    c.commit()
    print (sl2)
    Label(d,text=' ',bg='white', width=20).grid(row=0,column=1)
    cur.execute('Select * from med')
    for i in cur:
        if i[0]==sl2:
            Label(d,text=i[0]+'. '+i[1],bg='white').grid(row=0,column=1)
    c.commit()
    
def delt():
    global p,c,cur,d
    cur.execute("delete from med where sl_no=?",(sl2,))
    c.commit()
    ren()

def modify():    # window for modification-----------------------------------------------------------------------MODIFY
    global cur, c, accept, flag, att, up, n, name_, apt, st, col,col_n
    col=('', '', 'type', 'qty_left', 'cost', 'purpose', 'expdt', 'loc', 'mfg')
    col_n=('', '', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')
    flag='st'
    name_=''
    apt.destroy()
    n=[]
    cur.execute("select * from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    st=Tk()
    st.geometry("800x430")
    img = PhotoImage(file='3.png')
    label17 = Label(st, image=img)
    label17.place(x=1, y=1)
    st.title('MODIFY')
    Label(st, text=' MODIFY DATABASE ',font='Verdana 12').grid(row=0, column=0,columnspan=6,pady=5, padx=5, ipadx=5,ipady=5)
    def onvsb(*args):
        name_.yview(*args)
    def onmousewheel():
        name_.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    vsb.grid(row=1,column=3,sticky=N+S)
    name_=Listbox(st,width=43,yscrollcommand=vsb.set)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        name_.insert(cx,(str(i[0])+'.  '+str(i[1])))
        name_.grid(row=1,column=1,columnspan=2)
    c.commit()
    name_.bind('<MouseWheel>',onmousewheel)
    name_.bind('<<ListboxSelect>>', sel_mn)

    Label(st, text='Enter Medicine Name: ',font='Verdana 10').grid(row=1, column=0,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st, text='Enter changed Value of: ',font='Verdana 10').grid(row=2, column=0,pady=5, padx=5, ipadx=5,ipady=5)
    att=Spinbox(st, values=col_n)
    att.grid(row=2, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    up=Entry(st,font='Verdana 10')
    up.grid(row=2, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=10,text='Submit', command=save_mod,font='Verdana 9').grid(row=2, column=4,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=10,text='Reset', command=res,font='Verdana 9').grid(row=2, column=5,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=10,text='Show data', command=show_val,font='Verdana 9').grid(row=1, column=4,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=10,text='Main Menu',command=main_menu,font='Verdana 9').grid(row=5,column=5,pady=5, padx=5, ipadx=5,ipady=5)
    st.mainloop()

def res():
    global st, up
    up=Entry(st)
    up.grid(row=2, column=2)
    Label(st,width=20, text='                         ').grid(row=5,column=i)

def sel_mn(e):
    global n,name_, name_mn, sl, c, cur
    name_mn=''
    p=name_.curselection()
    print (p)
    x=0
    sl=''
    cur.execute("select * from med")
    for i in cur:
        print (x, p[0])
        if x==int(p[0]):
            sl=i[0]
            break
        x+=1
    c.commit()
    print (sl)
    name_nm=n[int(sl)]
    print (name_nm)
    
def show_val():
    global st, name_mn, att, cur, c, col, col_n, sl
    for i in range(3):
        Label(st,width=20, text='                         ').grid(row=5,column=i)
    cur.execute("select * from med")
    for i in cur:
        for j in range(9):
            if att.get()==col_n[j] and sl==i[0]:
                Label(st, text=str(i[0])).grid(row=5,column=0)
                Label(st, text=str(i[1])).grid(row=5,column=1)
                Label(st, text=str(i[j])).grid(row=5,column=2)
    c.commit()

def save_mod(): #save modified data
    global cur, c, att, name_mn, st, up, col_n, sl
    for i in range(9):
        if att.get()==col_n[i]:
            a=col[i]
    sql="update med set '%s' = '%s' where sl_no = '%s'" % (a,up.get(),sl)
    cur.execute(sql)
    c.commit()
    Label(st, text='Updated!').grid(row=5,column=4)
    
    
def stock():    #add to stock window------------------------------------------------------------------------ADD TO STOCK
    global cur, c, columns, accept, flag, sto, apt
    apt.destroy()
    flag='sto'
    accept=['']*10
    sto=Tk()
    sto.title('STOCK ENTRY')
    sto.geometry("970x510")
    img = PhotoImage(file='3.png')
    label17 = Label(sto, image=img)
    label17.place(x=1, y=1)
    Label(sto,text='ENTER NEW PRODUCT DATA TO THE STOCK',font="Verdana 12").grid(row=0,column=0,columnspan=2,pady=5, padx=5, ipadx=5,ipady=5)
    for i in range(1,len(columns)):
        Label(sto,width=15,text=' '*(14-len(str(columns[i])))+str(columns[i])+':').grid(row=i+2,column=0)
        accept[i]=Entry(sto)
        accept[i].grid(row=i+2, column=1)
    Button(sto,width=15,text='Submit',font="Verdana 10",command=submit).grid(row=12,column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Button(sto,width=15,text='Reset',font="Verdana 10",command=reset).grid(row=12,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    Button(sto,width=15,text='Refresh stock',font="Verdana 10",command=ref).grid(row=12,column=4, padx=5, ipadx=5,ipady=5)
    for i in range(1,6):
        Label(sto,text=columns[i]).grid(row=14,column=i-1)
    Label(sto,text='Exp           Rack   Manufacturer                      ',font="Verdana 10").grid(row=14,column=5)
    Button(sto,width=15,text='Main Menu',font="Verdana 10",command=main_menu).grid(row=12,column=5, padx=5, ipadx=5,ipady=5)
    ref()
    sto.mainloop()

def ref(): # creates a multi-listbox manually to show the whole database 
    global sto, c, cur
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)
        lb3.yview(*args)
        lb4.yview(*args)
        lb5.yview(*args)
        lb6.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        lb3.ywiew=('scroll',event.delta,'units')
        lb4.ywiew=('scroll',event.delta,'units')
        lb5.ywiew=('scroll',event.delta,'units')
        lb6.ywiew=('scroll',event.delta,'units')
        
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(sto,yscrollcommand=vsb.set)
    lb2=Listbox(sto,yscrollcommand=vsb.set)
    lb3=Listbox(sto,yscrollcommand=vsb.set,width=10)
    lb4=Listbox(sto,yscrollcommand=vsb.set,width=7)
    lb5=Listbox(sto,yscrollcommand=vsb.set,width=25)
    lb6=Listbox(sto,yscrollcommand=vsb.set,width=37)
    vsb.grid(row=15,column=6,sticky=N+S)
    lb1.grid(row=15,column=0)
    lb2.grid(row=15,column=1)
    lb3.grid(row=15,column=2)
    lb4.grid(row=15,column=3)
    lb5.grid(row=15,column=4)
    lb6.grid(row=15,column=5)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    lb3.bind('<MouseWheel>',onmousewheel)
    lb4.bind('<MouseWheel>',onmousewheel)
    lb5.bind('<MouseWheel>',onmousewheel)
    lb6.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        seq=(str(i[0]),str(i[1]))
        lb1.insert(cx,'. '.join(seq))
        lb2.insert(cx,i[2])
        lb3.insert(cx,i[3])
        lb4.insert(cx,i[4])
        lb5.insert(cx,i[5])
        lb6.insert(cx,i[6]+'    '+i[7]+'    '+i[8])
    c.commit()

def reset():
    global sto, accept
    for i in range(1,len(columns)):
        Label(sto,width=15,text=' '*(14-len(str(columns[i])))+str(columns[i])+':').grid(row=i+2,column=0)
        accept[i]=Entry(sto)
        accept[i].grid(row=i+2, column=1)
    
def submit(): #for new stock submission
    global accept, c, cur, columns, sto
    prev=time.perf_counter()
    x=['']*10
    cur.execute("select * from med")
    for i in cur:
        y=int(i[0])
    for i in range(1,9):
        x[i]=accept[i].get()
    sql="insert into med values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (y+1,x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8])
    cur.execute(sql)
    cur.execute("select * from med")
    c.commit()
    now=time.process_time()
    print (now-prev)
    top=Tk()
    Label(top,width=20, text='Success!').pack()
    top.mainloop()
    main_menu()

def chk(): #checks if the medicine is already present so that can be modified
    global cur, c, accept, sto
    cur.execute("select * from med")
    for i in cur:
        if accept[6].get()==i[6] and i[1]==accept[1].get():
            sql="update med set qty_left = '%s' where name = '%s'" % (str(int(i[3])+int(accept[3].get())),accept[1].get())
            cur.execute(sql)
            c.commit()
            top=Tk()
            Label(top,width=20, text='Modified!').pack()
            top.mainloop()
            main_menu()
        else:
            submit()
    c.commit()

def exp_date(): # expiry window open-----------------------------------------------------------------------------EXPIRY
    global exp, s,c, cur, flag, apt, flags
    apt.destroy()
    flag='exp'
    from datetime import date
    now=time.localtime()
    n=[]
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    exp=Tk()
    exp.title('EXPIRY CHECK')
    exp.geometry("800x430")
    img = PhotoImage(file='3.png')
    label17 = Label(exp, image=img)
    label17.place(x=1, y=1)
    Label(exp,text='Today : '+str(now[2])+'/'+str(now[1])+'/'+str(now[0]),font="Verdana 15").grid(row=0, column=0, columnspan=3,pady=5, padx=5, ipadx=5,ipady=5)
    Label(exp,text='Selling Expired Medicines and Drugs is Illegal',font="Verdana 12").grid(row=1, column=0,columnspan=3,pady=5, padx=5, ipadx=5,ipady=5)
    s=Spinbox(exp,values=n,font="Verdana 12")
    s.grid(row=3, column=0,pady=5, padx=5, ipadx=5,ipady=5)
    Button(exp,text='Check Expiry date' ,font="Verdana 10",command=s_exp).grid(row=3, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    if flags=='apt1':
        Button(exp,text='Main Menu',font="Verdana 10" ,command=main_cus).grid(row=5, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    else:
        Button(exp,width=20,text='Check Products expiring', font="Verdana 10" ,command=exp_dt).grid(row=5, column=0,pady=5, padx=5, ipadx=5,ipady=5)
        Button(exp,text='Main Menu',  font="Verdana 10" ,command=main_menu).grid(row=5, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    exp.mainloop()

def s_exp():    # shows the expiry date of the medicine entered
    global c, cur, s, exp, top
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if(i[1]==s.get()):
            q=i[6]
            d2=date(int('20'+q[8:10]),int(q[3:5]),int(q[0:2]))
            if d1>d2:
                Label(exp, text='EXPIRED! on '+i[6]).grid(row=3, column=2,pady=5, padx=5, ipadx=5,ipady=5)
                top=Tk()
                Label(top, text='EXPIRED!').pack()
            else:
                Label(exp, text=i[6]).grid(row=3, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    c.commit()

def exp_dt(): # shows medicine to expire in the coming week
    global c, cur, exp, top
    x=0
    z=1
    from datetime import datetime, timedelta 
    N = 7
    dt = datetime.now() + timedelta(days=N)
    d=str(dt)
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    d3 = date(int(d[0:4]),int(d[5:7]),int(d[8:10]))
    Label(exp,text='S.No'+'   '+'Name'+'     Qty.    '+'Exp_date').grid(row=6,column=0,columnspan=2)
    cur.execute("select * from med")
    for i in cur:
        s=i[6]
        d2=date(int('20'+s[8:10]),int(s[3:5]),int(s[0:2]))
        
        if d1<d2<d3:
            Label(exp,text=str(z)+'.      '+str(i[1])+'    '+str(i[3])+'    '+str(i[6])).grid(row=x+7,column=0,columnspan=2)
            x+=1
            z+=1
        elif d1>d2:
            top=Tk()
            Label(top,width=20, text=str(i[1])+' is EXPIRED!').pack()
    c.commit()
    
def billing(): # to create bills for customer-------------------------------------------------------------BILLING system
    global c, cur, apt, flag, t, name, name1, add, st, names, qty, sl, qtys, vc_id, n, namee, lb1
    t=0
    vc_id=''
    names=[]
    qty=[]
    sl=[]
    n=[]
    qtys=['']*10
    cur.execute("select *from med")
    for i in cur:
        n.append(i[1])
    c.commit()
    if flag=='st':
        st.destroy()
    else:
        apt.destroy()
    flag='st'
    st=Tk()
    st.title('BILLING SYSTEM')
    st.geometry("800x510")
    img = PhotoImage(file='3.png')
    label17 = Label(st, image=img)
    label17.place(x=1, y=1)
    Label(st,text='BILLING SYSTEM',  font="Verdana 12").grid(row=0,column=0,columnspan=7,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st,text='Enter Name: ',  font="Verdana 10").grid(row=1,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    name1=Entry(st,  font="Verdana 10")
    name1.grid(row=1, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st,text='Enter Address: ',  font="Verdana 10").grid(row=2,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    add=Entry(st,  font="Verdana 10" )
    add.grid(row=2, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st,text="Value Id (if available)",  font="Verdana 10").grid(row=3, column=0,pady=5, padx=5, ipadx=5,ipady=5)
    vc_id=Entry(st,  font="Verdana 10")
    vc_id.grid(row=3, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st,text='SELECT PRODUCT',width=25,relief='ridge',  font="Verdana 10").grid(row=7, column=0,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st,text=' RACK  QTY LEFT     COST          ',width=25,relief='ridge').grid(row=7, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,text='Add to bill',width=15,command=append2bill).grid(row=8, column=6,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st,text='QUANTITY',width=20,relief='ridge',  font="Verdana 10").grid(row=7, column=5,pady=5, padx=5, ipadx=5,ipady=5)
    qtys=Entry(st)
    qtys.grid(row=8,column=5,pady=5, padx=5, ipadx=5,ipady=5)
    refresh()
    Button(st,width=15,text='Main Menu', command=main_menu,  font="Verdana 10").grid(row=1,column=6,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=15,text='Refresh Stock', command=refresh,  font="Verdana 10").grid(row=3,column=6,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=15,text='Reset Bill', command=billing,  font="Verdana 10").grid(row=4,column=6,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=15,text='Print Bill', command=print_bill,  font="Verdana 10").grid(row=5,column=6,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=15,text='Save Bill', command=make_bill,  font="Verdana 10").grid(row=7,column=6,pady=5, padx=5, ipadx=5,ipady=5)
    
    st.mainloop()

def refresh():
    global cur, c, st, lb1, lb2, vsb
    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew=('scroll',event.delta,'units')
        lb2.ywiew=('scroll',event.delta,'units')
        return 'break'
    cx=0
    vsb=Scrollbar(orient='vertical',command=onvsb)
    lb1=Listbox(st,width=25, yscrollcommand=vsb.set)
    lb2=Listbox(st ,width=25,yscrollcommand=vsb.set)
    vsb.grid(row=8,column=2,sticky=N+S)
    lb1.grid(row=8,column=0)
    lb2.grid(row=8,column=1)
    lb1.bind('<MouseWheel>',onmousewheel)
    lb2.bind('<MouseWheel>',onmousewheel)
    cur.execute("select *from med")
    for i in cur:
        cx+=1
        lb1.insert(cx,str(i[0])+'. '+str(i[1]))
        lb2.insert(cx,' '+str(i[7])+'        '+str(i[3])+'             Rs '+str(i[4]))
    c.commit()
    lb1.bind('<<ListboxSelect>>', select_mn)

def select_mn(e): #store the selected medicine from listbox
    global st, lb1, n ,p, nm, sl1
    p=lb1.curselection()
    x=0
    sl1=''
    from datetime import date
    now=time.localtime()
    d1 = date(now[0],now[1],now[2])
    cur.execute("select * from med")
    for i in cur:
        if x==int(p[0]):
            sl1=int(i[0])
            break
        x+=1    
    c.commit()
    print (sl1)
    nm=n[x]
    print (nm)
    
def append2bill(): # append to the bill
    global st, names, nm , qty, sl,cur, c, sl1
    sl.append(sl1)
    names.append(nm)
    qty.append(qtys.get())
    print (qty)
    print (sl[len(sl)-1],names[len(names)-1],qty[len(qty)-1])
    
def blue(): # check if valued customer
    global st ,c, cur, named, addd, t, vc_id
    cur.execute("select * from cus")
    for i in cur:
        if vc_id.get()!='' and int(vc_id.get())==i[2]:
            named=i[0]
            addd=i[1]
            Label(st,text=named,width=20).grid(row=1, column=1)
            Label(st,text=addd,width=20).grid(row=2, column=1)
            Label(st,text=i[2],width=20).grid(row=3, column=1)
            Label(st, text='Valued Customer!').grid(row=4, column=1)
            t=1
            break
    c.commit()

def make_bill(): # makes bill
    global t, c, B, cur, st, names, qty, sl , named, addd, name1, add,det, vc_id
    price=[0.0]*10
    q=0
    det=['','','','','','','','']
    det[2]=str(sl)
    for i in range(len(sl)):
        print (sl[i],' ',qty[i],' ',names[i])
    for k in range(len(sl)):
        cur.execute("select * from med where sl_no=?",(sl[k],))
        for i in cur:
            price[k]=int(qty[k])*float(i[4])
            print (qty[k],price[k])
            cur.execute("update med set qty_left=? where sl_no=?",(int(i[3])-int(qty[k]),sl[k]))
        c.commit()
    det[5]=str(random.randint(100,999))
    B='bill_'+str(det[5])+'.txt'
    total=0.00
    for i in range(10):
        if price[i] != '':
            total+=price[i] #totalling
    m='\n\n\n'
    m+="===============================================\n"
    m+="                                  No :%s\n\n" % det[5]
    m+="          SFIT MEDIPHARM \n"
    m+="  PHARMACY MANAGEMENT SYSTEM\n\n"
    m+="-----------------------------------------------\n"
    if t==1:
        m+="Name: %s\n" % named
        m+="Address: %s\n" % addd
        det[0]=named
        det[1]=addd
        cur.execute('select * from cus')
        for i in cur:
            if i[0]==named:
                det[7]=i[2]
    else:
        m+="Name: %s\n" % name1.get()
        m+="Address: %s\n" % add.get()
        det[0]=name1.get()
        det[1]=add.get()
    m+="-----------------------------------------------\n"
    m+="Product                      Qty.       Price\n"
    m+="-----------------------------------------------\n"#47, qty=27, price=8 after 2
    for i in range(len(sl)):
        if names[i] != 'nil':
            s1=' '
            s1=(names[i]) + (s1 * (27-len(names[i]))) + s1*(3-len(qty[i])) +qty[i]+ s1*(15-len(str(price[i])))+str(price[i]) + '\n'
            m+=s1
    m+="\n-----------------------------------------------\n"
    if t==1:
        ntotal=total*0.8
        m+='Total'+(' '*25)+(' '*(15-len(str(total)))) + str(total)+'\n'
        m+="Valued customer Discount"+ (' '*(20-len(str(total-ntotal))))+'-'+str(total-ntotal)+'\n'
        m+="-----------------------------------------------\n"
        m+='Total'+(' '*25)+(' '*(12-len(str(ntotal)))) +'Rs '+ str(ntotal)+'\n'
        det[3]=str(ntotal)
    else:
        m+='Total'+(' '*25)+(' '*(12-len(str(total)))) +'Rs '+ str(total)+'\n'
        det[3]=str(total)
        
    m+="-----------------------------------------------\n\n"
    m+="Dealer 's signature:___________________________\n"
    m+="===============================================\n"
    print (m)
    p=time.localtime()
    det[4]=str(p[2])+'/'+str(p[1])+'/'+str(p[0])
    det[6]=m
    bill=open(B,'w')
    bill.write(m)
    bill.close()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill','val_id')
    cur.execute('insert into bills values(?,?,?,?,?,?,?,?)',(det[0],det[1],det[2],det[3],det[4],det[5],det[6],det[7]))
    c.commit()
    
def print_bill():
    win32api.ShellExecute (0,"print",B,'/d:"%s"' % win32print.GetDefaultPrinter (),".",0)
    
def show_rev(): # opens revenue window-----------------------------------------------------------------------TOTAL REVENUE
    global c, cur, flag,rev
    apt.destroy()
    cb=('cus_name','cus_add','items','Total_cost','bill_dt','bill_no','bill','val_id')
    flag='rev'
    rev=Tk()
    rev.geometry("800x430")
    img = PhotoImage(file='3.png')
    label17 = Label(rev, image=img)
    label17.place(x=1, y=1)
    total=0.0
    today=str(time.localtime()[2])+'/'+str(time.localtime()[1])+'/'+str(time.localtime()[0])
    Label(rev,text='Today: '+today,font="Verdana 12").grid(row=0,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    cur.execute('select * from bills')
    for i in cur:
        if i[4]==today:
            total+=float(i[3])
    print (total)
    Label(rev,width=22,text='Total revenue: Rs '+str(total), bg='black',fg='white',font="Verdana 12").grid(row=1,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    cx=0
    vsb=Scrollbar(orient='vertical')
    lb1=Listbox(rev,width=25, yscrollcommand=vsb.set)
    vsb.grid(row=2,column=1,sticky=N+S)
    lb1.grid(row=2,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    vsb.config( command = lb1.yview )
    cur.execute("select * from bills")
    for i in cur:
        if i[4]==today:
            cx+=1
            lb1.insert(cx,'Bill No.: '+str(i[5])+'    : Rs '+str(i[3]))
    c.commit()
    Button(rev,text='Main Menu',command=main_menu,font="Verdana 10").grid(row=15,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    rev.mainloop()


def search():   #search window medicine and symptom details---------------------------------SEARCH MEDICINE RACK & SYMPTOMS
    global c, cur, flag, st, mn, sym, flags
    flag='st'
    apt.destroy()
    cur.execute("Select * from med")
    symp=['nil']
    med_name=['nil']
    for i in cur:
        symp.append(i[5])
        med_name.append(i[1])
    st=Tk()
    st.title('SEARCH')
    st.geometry("800x430")
    img = PhotoImage(file='3.png')
    label17 = Label(st, image=img)
    label17.place(x=1, y=1)
    Label(st, text=' SEARCH FOR MEDICINE ',font='Verdana 12').grid(row=0, column=0,columnspan=3,pady=5, padx=5, ipadx=5,ipady=5)
    Label(st, text='Symptom Name').grid(row=3, column=0,pady=5, padx=5, ipadx=5,ipady=5)
    sym=Spinbox(st,values=symp,font='Verdana 10')
    sym.grid(row=3, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Button(st,width=15, text='Search', command=search_med,font='Verdana 10').grid(row=3, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    if flags=='apt1':
        Button(st,width=15, text='Main Menu', command=main_cus,font='Verdana 10').grid(row=6, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    else:
        Button(st,width=15, text='Main Menu', command=main_menu,font='Verdana 10').grid(row=6, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    st.mainloop()

def search_med():
    global c, cur, st, sym, columns
    cur.execute("select * from med")
    y=[]
    x=0
    for i in cur:
        if i[5]==sym.get():
            y.append(str(i[0])+'. '+str(i[1])+'  Rs '+str(i[4])+'    Rack : '+str(i[7])+'    Mfg : '+str(i[8]))
            x=x+1
    top=Tk()
    for i in range(len(y)):
        Label(top,text=y[i]).grid(row=i, column=0)
    Button(top,text='OK',command=top.destroy).grid(row=5, column=0)
    c.commit()
    top.mainloop()

def val_cus():  #to enter new valued customer-----------------------------------------------------------NEW VALUED CUSTOMER
    global val, flag, dbt, name_vc, add_vc, cur, c, vc_id
    apt.destroy()
    cur.execute("select * from cus")
    flag='val'
    val=Tk()
    val.geometry("800x430")
    img = PhotoImage(file='3.png')
    label17 = Label(val, image=img)
    label17.place(x=1, y=1)
    Label(val,text="ENTER VALUED CUSTOMER DETAILS",font='Verdana 12').grid(row=0,column=0,columnspan=3,pady=5, padx=5, ipadx=5,ipady=5)
    Label(val,text="Name: ",font='Verdana 10').grid(row=2,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    name_vc=Entry(val,font='Verdana 10')
    name_vc.grid(row=2, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Label(val,text="phone no: ",font='Verdana 10').grid(row=3,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    add_vc=Entry(val,font='Verdana 10')
    add_vc.grid(row=3, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Label(val,text="Value Id: ",font='Verdana 10').grid(row=4,column=0,pady=5, padx=5, ipadx=5,ipady=5)
    vc_id=Entry(val,font='Verdana 10')
    vc_id.grid(row=4, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Button(val,text='Submit',command=val_get,font='Verdana 10').grid(row=5, column=1,pady=5, padx=5, ipadx=5,ipady=5)
    Button(val,text='Main Menu',command=main_menu,font='Verdana 10').grid(row=5, column=2,pady=5, padx=5, ipadx=5,ipady=5)
    val.mainloop()

def val_get():  #to submit new valued customer details
    global name_vc, add_vc, val, dbt ,c, cur, apt, vc_id
    cur.execute("insert or replace  into cus values(?,?,?)",(name_vc.get(),add_vc.get(),vc_id.get()))
    l.execute("insert or replace into log values(?,?)",(name_vc.get(),vc_id.get()))
    cur.execute("select * from cus")
    for i in cur:
        print (i[0], i[1], i[2])
    c.commit()
    login.commit()
    
def again():    #for login window-----------------------------------------------------------------------------LOGIN WINDOW
    global un, pwd, flag, root, apt
    if flag=='apt':
        apt.destroy()
    root=Tk()
    root.geometry("920x620")
    root.title('MINI PROJECT')
    img = PhotoImage(file='1.png')
    label17 = Label(root, image=img)
    label17.place(x=0, y=0)


    Label(root, text="SFIT MEDIPHARM", bg="cyan", fg="black", font="Verdana 25",width=35).grid(row=0, column=0, columnspan=5,pady=9, padx=9, ipadx=80,ipady=5)

    Label(root, text="        PHARMACY STORE MANAGEMENT SYSTEM       ", bg="orange", fg="purple",width=40,font='Verdana 18').grid(row=2,
                                                                                                       column=0,
                                                                                                       columnspan=5,pady=3, padx=3, ipadx=50,ipady=3)
    Label(root, text="   The best health care experience !  ", bg="yellow", fg="red",font='Verdana 16').grid(row=3,
                                                                                         column=0,
                                                                                         columnspan=5,pady=9, padx=9, ipadx=40,ipady=3)
    Label(root, text='Username',width=12,bg='blue',font='Verdana 14').grid(row=7, column=0,pady=3, padx=3, ipadx=5,ipady=3)
    un=Entry(root,font='Verdana 11')
    un.grid(row=7, column=1,pady=5, padx=5, ipadx=20,ipady=7)
    Label(root, text='Password',width=12,bg='blue',font='Verdana 14').grid(row=9, column=0,pady=3, padx=3, ipadx=5,ipady=3)
    pwd=Entry(root,font='Verdana 11',show='*')
    pwd.grid(row=9, column=1,pady=10, padx=10, ipadx=20,ipady=7)
    Button(root,width=13,text='Enter',command=check,bg="green", fg="white",font='Verdana 12').grid(row=12, column=0,pady=20, padx=20, ipadx=20,ipady=2)
    Button(root,width=13,text='Close',command=root.destroy,bg="red", fg="white",font='Verdana 12').grid(row=12, column=1,pady=20, padx=20, ipadx=20,ipady=2)
    root.mainloop()
    
def check():    #for enter button in login window
    global un, pwd, login, l, root
    u=un.get()
    p=pwd.get()
    l.execute("select * from log")
    for i in l:     
        if i[0]==u and i[1]==p and u=='admin':
            root.destroy()
            open_win()
        elif i[0]==u and i[1]==p:
            root.destroy()
            open_cus()
    login.commit()

def main_menu(): #controls open and close of main menu window----------------------------------------RETURN TO MAIN MENU
    global sto, apt, flag, root, st, val, exp, st1,rev
    if flag=='sto':
        sto.destroy()
    if flag=='rev':
        rev.destroy()
    elif flag=='st':
        st.destroy()
    elif flag=='st1':
        st1.destroy()
    elif flag=='val':
        val.destroy()
    elif flag=='exp':
        exp.destroy()
    elif flag=='d':
        d.destroy()
    open_win()    

def main_cus():
    global st, flag, exp
    if flag=='exp':
        exp.destroy()
    elif flag=='st':
        st.destroy()
    open_cus()
    
def open_cus(): #OPENS MAIN MENU----------------------------------------------------------------------------MAIN MENU
    global apt, flag, flags
    flags='apt1'
    apt=Tk()
    apt.title("Interface")
    Label(apt, text="MEDPLUS CHEMIST AND DRUGGIST").grid(row=0,column=0)
    Label(apt, text='*'*40).grid(row=1,column=0)
    Label(apt, text='*  WELCOME  *').grid(row=2,column=0)
    Label(apt, text='-'*40).grid(row=3,column=0)
    Label(apt, text="Customer Services").grid(row=4,column=0)
    Label(apt, text='-'*40).grid(row=5,column=0)
    Button(apt,text='Search', width=15, command=search).grid(row=6,column=0)
    Button(apt,text='Expiry Check', width=15, command=exp_date).grid(row=7,column=0)
    
    Label(apt, text='-'*40).grid(row=8,column=0)    
    Button(apt,text='Logout',command=again1).grid(row=9, column=0)
    apt.mainloop()
def again1():
    global flags
    apt.destroy()
    flags=''
    again()
again()

