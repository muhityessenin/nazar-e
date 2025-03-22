from django.shortcuts import redirect, render, get_object_or_404

from .decorators import only_director
from .forms import *
from employee.models import Employee,Attendance,Notice,workAssignments
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def dashboard(request):
    current_id = request.user.username

    # Если директор — отправляем на отдельный шаблон
    if current_id == "123123":  # eID директора
        query = request.GET.get('q', '')
        if query:
            employees = Employee.objects.filter(
                Q(firstName__icontains=query) |
                Q(lastName__icontains=query) |
                Q(middleName__icontains=query) |
                Q(designation__icontains=query)
            )
        else:
            employees = Employee.objects.all()

        # считаем задачи по каждому сотруднику
        employees_with_tasks = []
        for emp in employees:
            assigned = workAssignments.objects.filter(taskerId=emp).count()
            done = workAssignments.objects.filter(taskerId=emp, isDone=True).count()
            employees_with_tasks.append({
                "employee": emp,
                "assigned": assigned,
                "done": done
            })

        return render(request, "employee/director_dashboard.html", {
            "employees": employees_with_tasks,
            "query": query
        })

    # Обычный сотрудник
    info = Employee.objects.filter(eID=current_id)
    assigned_tasks = workAssignments.objects.filter(taskerId__eID=current_id).count()
    completed_tasks = workAssignments.objects.filter(taskerId__eID=current_id, isDone=True).count()

    return render(request, "employee/index.html", {
        'info': info,
        'assigned_count': assigned_tasks,
        'done_count': completed_tasks
    })

@login_required(login_url='/')
def mark_done(request, wid):
    work = get_object_or_404(workAssignments, id=wid)
    if work.taskerId.eID == request.user.username:
        work.isDone = True
        work.save()
        messages.success(request, "Marked as done.")
    else:
        messages.error(request, "You cannot mark this task.")
    return redirect('/ems/mywork')

@login_required(login_url='/')
def attendance(request):
    attendance=Attendance.objects.filter(eId=request.user.username)
    return render(request,"employee/attendance.html",{"info":attendance})    

@login_required(login_url='/')
def notice(request):
    notices  = Notice.objects.all()
    return render(request,"employee/notice.html",{"notices":notices})

@login_required(login_url='/')
def noticedetail(request,id):
    noticedetail = Notice.objects.get(Id=id)
    return render(request,"employee/noticedetail.html",{"noticedetail":noticedetail})

@login_required(login_url='/')
def assignWork(request):
    context={}
    initialData = {
        "assignerId" : request.user.username,
    }
    flag = ""
    form = workform(request.POST or None, initial=initialData)
    if form.is_valid():
        currentTaskerId = request.POST["taskerId"]
        currentUserId = request.user.username
        if currentTaskerId == currentUserId:
            flag="Invalid ID Selected..."
        else:
            flag = "Work Assigned Successfully!!"
            form.save()

    context['form']=form
    context['flag'] = flag
    return render(request,"employee/workassign.html",context)

@login_required(login_url='/')
def mywork(request):
    work = workAssignments.objects.filter(taskerId=request.user.username)
    return render(request,"employee/mywork.html",{"work":work})

@login_required(login_url='/')
def workdetails(request,wid):
    workdetails = workAssignments.objects.get(id=wid);
    return render(request,"employee/workdetails.html",{"workdetails":workdetails})

@login_required(login_url='/')
def makeRequest(request):
    context={}
    initialData = {
        "requesterId" : request.user.username,
    }
    flag = ""
    requestForm = makeRequestForm(request.POST or None, initial=initialData)
    if request.method == 'POST':
        requestForm = makeRequestForm(request.POST)
        if requestForm.is_valid():
            currentRequesterId = request.POST["destinationEmployeeId"]
            currentUserId = request.user.username
            if currentRequesterId == currentUserId:
                flag="Invalid ID Selected..."
            else:
                flag="Request Submitted"
                requestForm.save()

    context['requestForm']=requestForm
    context['flag'] = flag
    return render(request,"employee/request.html",context)

@login_required(login_url='/')
def viewRequest(request):
    requests = Requests.objects.filter(destinationEmployeeId=request.user.username)
    return render(request,"employee/viewRequest.html",{"requests":requests})

@login_required(login_url='/')
def requestdetails(request,rid):
    requestdetail = Requests.objects.get(id=rid)
    return render(request,"employee/requestdetails.html",{"requestdetail":requestdetail})

@login_required(login_url='/')
def assignedworklist(request):
    works = workAssignments.objects.filter(assignerId=request.user.username).all()
    return render(request,"employee/assignedworklist.html",{"works":works})

@login_required(login_url='/')
def deletework(request, wid):
    obj = get_object_or_404(workAssignments, id=wid)
    obj.delete()
    return render(request,"employee/assignedworklist.html")

@login_required(login_url='/')
def updatework(request,wid):
    work = workAssignments.objects.get(id=wid)
    form = workform(request.POST or None, instance=work)
    flag = ""
    if form.is_valid():
        currentTaskerId = request.POST["taskerId"]
        currentUserId = request.user.username
        if currentTaskerId == currentUserId:
            flag="Invalid ID Selected..."
        else:
            flag = "Work Updated Successfully!!"
            form.save()
    return render(request,"employee/updatework.html", {'currentWork': work, "filledForm": form, "flag":flag})


from django.db.models import Q


@login_required(login_url='/')
@only_director
def director_dashboard(request):
    query = request.GET.get('q', '')
    if query:
        employees = Employee.objects.filter(
            Q(firstName__icontains=query) |
            Q(lastName__icontains=query) |
            Q(middleName__icontains=query) |
            Q(designation__icontains=query)
        )
    else:
        employees = Employee.objects.all()

    return render(request, "employee/director_dashboard.html", {"employees": employees, "query": query})
