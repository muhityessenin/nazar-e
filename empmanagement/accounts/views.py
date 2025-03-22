from django.shortcuts import render
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from employee.models import Employee
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def login_user(request):
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]
        user = authenticate(request,username=id,password=password)
        if user is not None:
            login(request , user)
            return redirect("/ems/dashboard")
        else:
            messages.error(request,"Invalid Credentials")
            return redirect("/")

    return render(request,"employee/Login.html")


def logout_user(request):
    logout(request)
    return redirect("/")


def signup(request):
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]
        cnfpass = request.POST["cnfpass"]

        # Дополнительные поля для сотрудника
        firstName = request.POST["firstName"]
        middleName = request.POST.get("middleName", "")
        lastName = request.POST["lastName"]
        phoneNo = request.POST["phoneNo"]
        email = request.POST["email"]
        addharNo = request.POST["addharNo"]
        dOB = request.POST["dOB"]
        designation = request.POST["designation"]
        salary = request.POST["salary"]
        joinDate = request.POST["joinDate"]

        if password == cnfpass:
            if User.objects.filter(username=id).exists():
                messages.info(request, "Employee Already Registered")
                return redirect("/signup")
            else:
                # Создаем нового пользователя
                user = User.objects.create_user(username=id, password=password)
                user.save()
                # Создаем новую запись сотрудника
                Employee.objects.create(
                    eID=id,
                    firstName=firstName,
                    middleName=middleName,
                    lastName=lastName,
                    phoneNo=phoneNo,
                    email=email,
                    addharNo=addharNo,
                    dOB=dOB,
                    designation=designation,
                    salary=salary,
                    joinDate=joinDate
                )
                messages.info(request, "Registered Successfully")
                return redirect("/signup")
        else:
            messages.info(request, "Password Doesn't Match")
            return redirect("/signup")

    return render(request, "employee/signup.html")
