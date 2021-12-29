import random
from django.contrib.auth.forms import UserCreationForm
from django.http import request, response, HttpResponse, JsonResponse
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, qrcode_model,login_info, server_state
from .forms import SignupForm
from polls.models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login,logout
from django.contrib import messages
import sqlite3
from datetime import datetime
import qrcode
import csv
from pathlib import Path

from django.contrib.sessions.models import Session

BASE_DIR = Path(__file__).resolve().parent.parent

#@csrf_exempt
def singnup(request):
    if request.user.is_authenticated:
        return redirect('/accounts/tables/')
    else:
        if request.method=='POST':
            
            user_form=SignupForm(request.POST)
            # profile_form=ProfileForm(request.POST)
            if user_form.is_valid() :
                user_form.save()
                username = user_form.cleaned_data['username']
           
                # myform=profile_form.save(commit=False)
                # myform.fo
                # subject1=myform.cleaned_data["subject_1_name"]
                # user = Profile.objects.get(username=username)
                # password = user_form.cleaned_data['password1']
                messages.success(request,f"Account was created for {username}")
                # user=authenticate(username=username,password=password)
                # login(request,user)
                return redirect('/accounts/signin/')
            
        # else:
        form1=SignupForm()
        # form2=ProfileForm()
        return render(request,'registration/signup.html',{'form1':form1,'form2':''})
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/accounts/tables/')
    else:
            if request.method=='POST':    
                username=request.POST['username']
                password=request.POST['password']
                subject_name = request.POST['subject_name']
                obj = login_info.objects.get(subject_id="subject")
                obj.subject_name=subject_name
                obj.save()
                
                
                
                user=authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    print("done")
                    return redirect('/accounts/tables/')
                return redirect('/accounts/signup/')
            return render(request, 'registration/login.html')
def signout(request):
    logout(request)
    return render(request,'registration/logged_out.html')

@login_required(login_url='/accounts/signin')
def tables(request):
    
    return render(request, 'table/table.html')
def test(request):
    pass
    # Session.objects.all().delete()
    session_key = 'submit'
    session = Session.objects.get(session_key=session_key)
    Session.objects.filter(session_key=session).delete()
    # Session.objects.all().delete()
    
    session_key2 = 'username'
    session2 = Session.objects.get(session_key=session_key2)
    Session.objects.filter(session_key=session2).delete()
    # Session.objects.all().delete()
    return render(request,'profile/home.html')


@login_required(login_url='/accounts/signin')
def home(request):
    obj = login_info.objects.get(subject_id="subject")
    subject_name = obj.subject_name
    return render(request,"Home/home.html",{"subject_name":subject_name})
    #attendance_number=


@login_required(login_url='/accounts/signin')
def qrcode_generate(request):
 

    DIGITS = ['0', '1', '2', '3', '4', '5',     '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    # Simp=["!","@","#","$","%","&"]
    COMBINED_LIST = DIGITS + LOCASE_CHARACTERS
    hash_code = ''
    check_code=''
    # http://192.168.1.3:8080/student/login
    for i in range(20):
        hash_code += random.choice(COMBINED_LIST)
    for i in range(6):
        check_code += random.choice(COMBINED_LIST)
    host_ip = request.get_host()
    url = f"http://{host_ip}/student/submit/{hash_code}"

    t = qrcode_model.objects.get(qrcode_id="subject")
    t.qrcode_hash=hash_code
    t.qrcode_url=url
    t.check_code=check_code
    t.save()  

    return redirect('/accounts/qrcode/view')
def qrcode_page(request):
    obj = qrcode_model.objects.get(qrcode_id="subject")
    qrcode_img=obj.qrcode_img.url
    qrcode_url = obj.qrcode_url
    qrcode_check_code=obj.check_code
    return render(request,"qrcode/qrcode_page.html",{"img":qrcode_img,"url":qrcode_url,"code":qrcode_check_code})
@csrf_exempt
@login_required(login_url='/accounts/signin')
def post_data(request):
    # if request.is_ajax :#and request.method=="GET"
        data = list(Student.objects.values_list('name_id', 'name'))
        
        obj = login_info.objects.get(subject_id="subject")
        subject_name = obj.subject_name
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime(" %I:%M:%S")
        for i in range(len(data)):
            data[i]=list(data[i])
        return JsonResponse( {"students": data,'subject_name': subject_name, 'date': date, 'time': time,"name":request.user.get_username()})    
     

@login_required(login_url='/accounts/signin')
def export_csv(request):
    pass
    # response=HttpResponse(content_type='text/csv')
    # response['Content-Disposition']='attachment; filenmae="users.csv'
    # writer=csv.writer(response)
    # writer.writerow(['username','password'])
    # # BASE_DIR = Path(__file__).resolve().parent.parent
    # # db = sqlite3.connect("{BASE_DIR}\\students.db")
    # # cr = db.cursor()
    # # cr.execute("select * from skills")
    # # data = cr.fetchall()
    # users = data
    # print(users)
    # for user in users:
    #     writer.writerow(user)
    # return response
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filenmae="users.csv'
    # writer = csv.writer(response)
    # writer.writerow(['username', 'password'])
    # users = list(Student.objects.values_list('name_id', 'name'))
    # for i in range(len(users)):
    #         users[i]=list(users[i])

    # for user in users:
    #     writer.writerow(user)
    # return response

@login_required(login_url='/accounts/signin')
def csv_home(request):
    obj = login_info.objects.get(subject_id="subject")
    subject_name = obj.subject_name
    date = datetime.now().strftime("%d/%m/%Y")
    filename=f"{subject_name}_{date}"
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filenmae="{filename}".csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'name'])
    users = list(Student.objects.values_list('name_id', 'name'))

    for user in users:
        writer.writerow(user)
    return response
    # return render (request,"export/csv_export.html")


@login_required(login_url='/accounts/signin')
def start_server(request):
    obj = server_state.objects.get(server_id="server")
    obj.server_state=True
    obj.save()
    return JsonResponse({"server_state":True})
    


@login_required(login_url='/accounts/signin')
def stop_server(request):
    obj = server_state.objects.get(server_id="server")
    obj.server_state=False
    obj.save()
    return JsonResponse({"server_state": False})


@login_required(login_url='/accounts/signin')
def chart_json(request):
    data = list(Student.objects.values_list('name_id', 'name'))
    attendance_number=len(data)
    absence_number=384-attendance_number
    obj = login_info.objects.get(subject_id="subject")
    subject_name = obj.subject_name
    return JsonResponse({"attendance_number": attendance_number, "absence_number": absence_number,"subject_name":subject_name})
login_required(login_url='/accounts/signin')
def bar_page(request):
    
        return render(request,"Bar_page/bar_page.html")
<<<<<<< HEAD
    
=======
    
>>>>>>> 7237b0273c93167139959cb9556fbff16031532d
