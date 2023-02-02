from django.shortcuts import render, redirect
import mysql.connector as sql
from django.contrib import messages


con = sql.connect(host="localhost", user="root", passwd="0003", database="test")
cursor= con.cursor()

# Create your views here.

loggedIn = False

def index(request):
    if loggedIn:
        cursor.execute("select empid from employee")
        result = cursor.fetchall()
        data = [x[0] for x in result]
        return render(request, "home.html", {'idList':list(data)})
    else:
        return redirect('login/')


def logout(request):
    global loggedIn
    loggedIn = False
    return redirect('/login/')


def login(request):
    global loggedIn
    if request.method == "POST":
        passwd = request.POST['passwd']
        if passwd == "kanha@8827":
            loggedIn = True
            return redirect('/')
    if loggedIn:
        return redirect('/')
    return render(request, "login.html")
 

def addEmp(request):
    if request.method == 'POST':
        empid = request.POST['empid']
        cursor.execute("select empid from employee")
        for x in cursor.fetchall():
            if x[0] == empid.lower():
                messages.error(request,f"Employee With ID {empid} Already Exists!")
        else:
            empname = request.POST['empname']
            emppost = request.POST['emppost']
            empgen = request.POST['empgen']
            empsal = request.POST['empsal']
            empmob = request.POST['empmob']
            query = f"insert into employee values ('{empid.lower()}', '{empname}', '{emppost}', '{empgen}', '{empsal}', '{empmob}')"
            cursor.execute(query)
            messages.info(request, "Employee Added Successfully.")
            con.commit()

        
    return render(request, "addEmp.html")


def updateEmp(request, empid):
    query = f"select * from employee where empid = '{empid}'"
    cursor.execute(query)
    result = cursor.fetchall();
    if request.method == 'POST':
        empname = request.POST['empname']
        emppost = request.POST['emppost']
        empgen = request.POST['empgen']
        empsal = request.POST['empsal']
        empmob = request.POST['empmob']
        query = f"update employee set empname='{empname}', emppost='{emppost}', empgen='{empgen}', empsal='{empsal}', empmob='{empmob}' where empid='{empid}'"        
        cursor.execute(query)
        con.commit()
        messages.info(request, "Data Updated Successfully.")

        cursor.execute(f"select * from employee where empid = '{empid}'")
        result = cursor.fetchall();
        return render(request, "updateEmp.html", {'empList':list(result[0])})

    return render(request, "updateEmp.html", {'empList':list(result[0])})


def showEmp(request):
    query = "select * from employee"
    cursor.execute(query)
    result=cursor.fetchall()
    return render(request, "showEmp.html", {'empList':result})


def delEmp(request):
    result = [(".......", ".......", ".......", ".......", ".......", ".......")]

    if request.method == "POST":
        empid = request.POST['empid']
        cursor.execute(f"select * from employee where empid = '{empid}'")
        result = cursor.fetchall();

    if result != []:
        return render(request, "delEmp.html", {'empList':list(result[0])})
    else:
        result = [(".......", ".......", ".......", ".......", ".......", ".......")]
        return render(request, "delEmp.html", {'empList':list(result[0])})

def delEmpID(request, empid):
    cursor.execute(f"delete from employee where empid='{empid}'")
    con.commit()
    return redirect('/')

