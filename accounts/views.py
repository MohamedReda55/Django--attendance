from json.encoder import JSONEncoder
import random
from django.contrib.auth.forms import UserCreationForm
from django.http import request, response, HttpResponse, JsonResponse
from django.shortcuts import redirect, render,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Profile, qrcode_model,login_info, server_state,restart_state,login_inf
from .forms import SignupForm
from polls.models import Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login,logout
from django.contrib import messages
from datetime import datetime
import qrcode
import csv
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from django.contrib.sessions.models import Session
import sqlite3
import mysql.connector
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

#@csrf_exempt
def singnup(request):
        if request.user.is_superuser:        
            if request.user.is_authenticated:
                return redirect('/accounts/home/')
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
        else:
            return redirect("/accounts/signin/")
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/accounts/tables/')
    else:
            if request.method=='POST':    
                username=request.POST['username']
                password=request.POST['password']
                subject_name = request.POST['subject_name']
                subject_tmp=subject_name
                subject_tmp = subject_tmp.lower().replace(" ", "_")
              
                try:
                    info=User.objects.get(username=username)
                    # profile_info = Profile.objects.all().filter(user_id=info.id)
                    # print(profile_info)
                    data = list(Profile.objects.filter(user_id=info.id).values_list('subject_1_name', 'subject_2_name', "subject_3_name"))
                    print(data)
                    
                    if subject_tmp not in data[0]:
                        messages.error(
                            request, "invalid,please try again ")
                        return redirect("/accounts/signin/")
                except:
                    messages.error(
                        request,"invalid,please try again ")
                    return redirect("/accounts/signin/")
                print(data)
                # if profile_info.subject_1_name ==subject_name:
                    
                date = datetime.now().strftime("%m_%d")
                try:
                    
                   
                    
                    obj = login_inf.objects.get(subject_id="subject")
                    obj.subject_info=f"{subject_tmp}_{date}"
                    obj.subject_name = subject_tmp
                    obj.save()
                except:
                   b=login_inf(subject_id="subject")
                   b.save()
                   obj = login_inf.objects.get(subject_id="subject")
                   obj.subject_info = f"{subject_tmp}_{date}"
                   obj.subject_name=subject_tmp
                   obj.save()
                user=authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user) 
                    
                    
                    db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database = 'students'
                    )
                    db2 = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database = 'records'
                    )
                    
                    table_name=f"{subject_tmp}_{date}"
                    
                    cr = db.cursor()
                    cur=db2.cursor()
                    cur.execute(
                        f'CREATE TABLE IF NOT EXISTS {table_name} (date text,attendance text,absence text,weather_state text,wheather_c text )')
                    cr.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (ID text , name text  ,num INT AUTO_INCREMENT PRIMARY KEY)')
                    db.commit()
                    db2.commit()
                    
          
                    return redirect('/accounts/tables/')
                return redirect('/accounts/signup/')
            return render(request, 'registration/login.html')
def signout(request):
    logout(request)
    return render(request,'registration/logged_out.html')

@login_required(login_url='/accounts/signin')
def tables(request):
    try:
        obj = login_inf.objects.get(subject_id="subject")
        subject_name = obj.subject_name
    except:
        b=login_inf(subject_id="subject")
        b.save()
    obj = login_inf.objects.get(subject_id="subject")
    subject_name = obj.subject_name
    return render(request, 'table/table.html', {"subject_name": subject_name})
@login_required(login_url='/accounts/signin')
def home(request):
    try:
        obj = login_inf.objects.get(subject_id="subject")
        subject_name = obj.subject_name
    except:
        b = login_inf(subject_id="subject")
        b.save()
    obj = login_inf.objects.get(subject_id="subject")
    subject_name = obj.subject_name
  
    return render(request,"Home/home.html",{"subject_name":subject_name})
    #attendance_number=
def weather_data():

            headers = {
	                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            city = "kafr el sheikh"+" weather"
            city = city.replace(" ", "+")
            res = requests.get(
                f'https://www.google.com/search?q={city}&oq={city}&gl=eg&hl=en&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
            print("Searching...\n")
            soup = BeautifulSoup(res.text, 'html.parser')
            location = soup.select('#wob_loc')[0].getText().strip()
            time = soup.select('#wob_dts')[0].getText().strip()
            info = soup.select('#wob_dc')[0].getText().strip()
            weather = soup.select('#wob_tm')[0].getText().strip()
            BASE_DIR = Path(__file__).resolve().parent.parent
            dp = sqlite3.connect(f"{BASE_DIR}/record.db")
            cur = dp.cursor()
            date = datetime.now().strftime("%d/%m")
            attendance_num = Student.objects.filter().count()
            absence_num=380-attendance_num

            cur.execute(
                "create table if not exists inforamtion_system(date text,attendance text,absence text,weather_state text,weather_c) ")
            cur.execute("select * from inforamtion_system where date=? ",(date))
            if(cur.fetchall()):
                cur.execute("update inforamtion_system set attendance=?,absence=? where date=? ",
                            (attendance_num, absence_num, date))
                cur.execute(
                    "select * from inforamtion_system where date=? ", (date))

            else:
                cur.execute("insert into inforamtion_system(date,attendance,absence,weather_state,wheather_c)values(?,?,?,?,?)",
                            (date,attendance_num, absence_num,info,weather))
            dp.commit()    




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

    try:
        t = qrcode_model.objects.get(qrcode_id="subject")
    except:
        t = qrcode_model(qrcode_id="subject")
    t.qrcode_hash=hash_code
    t.qrcode_url=url
    t.check_code=check_code
    t.save()  

    return redirect('/accounts/qrcode/view')
def qrcode_page(request):
    try:
        obj = qrcode_model.objects.get(qrcode_id="subject")
    except:
        obj=qrcode_model(qrcode_id="subject")
    qrcode_img=obj.qrcode_img.url
    qrcode_url = obj.qrcode_url
    qrcode_check_code=obj.check_code
    return render(request,"qrcode/qrcode_page.html",{"img":qrcode_img,"url":qrcode_url,"code":qrcode_check_code})
@csrf_exempt
@login_required(login_url='/accounts/signin')
def post_data(request):
    # if request.is_ajax :#and request.method=="GET"
        # data = list(Student.objects.values_list('name_id', 'name'))
        obj = login_inf.objects.get(subject_id="subject")
        subject_name = obj.subject_name
        table_name=obj.subject_info
        db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database='students'
                        )
        cr = db.cursor()
        cr.execute(f"SELECT ID,Name FROM {table_name} ")
        data=cr.fetchall()
        date = datetime.now().strftime("%d/%m/%Y")
        time = datetime.now().strftime(" %I:%M:%S")
        for i in range(len(data)):
            data[i]=list(data[i])
        return JsonResponse( {"students": data,'subject_name': subject_name, 'date': date, 'time': time,"name":request.user.get_username()})    
     

@login_required(login_url='/accounts/signin')
def export_csv(request):
    pass
@login_required(login_url='/accounts/signin')
def csv_home(request):
    obj = login_inf.objects.get(subject_id="subject")
    subject_name = obj.subject_name
    table_name = obj.subject_info
    date = datetime.now().strftime("%d/%m/%Y")
    filename=f"{subject_name}_{date}"
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="{filename}".csv'
    writer = csv.writer(response)
    writer.writerow(['id', 'name'])
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database='students'
                        )
    cr = db.cursor()
    cr.execute(f"SELECT ID,Name FROM {table_name} ")
    users=cr.fetchall()
    date = datetime.now().strftime("%d/%m/%Y")
    # for i in range(len(data)):
    #         data[i]=list(data[i])
    

    for user in users:
        writer.writerow(user)
    return response
    # return render (request,"export/csv_export.html")


@login_required(login_url='/accounts/signin')
def start_server(request):
    try:
        obj = server_state.objects.get(server_id="server")
    except:
        b = server_state(server_id="server")
        b.save()
    obj = server_state.objects.get(server_id="server")
    obj.server_state=True
    obj.save()
    return JsonResponse({"server_state":True})
    


@login_required(login_url='/accounts/signin')
def stop_server(request):
    try:
        obj = server_state.objects.get(server_id="server")
    except:
        b=server_state(server_id="server")
        b.save()
    obj = server_state.objects.get(server_id="server")
    obj.server_state=False
    obj.save()
    
    return JsonResponse({"server_state": False})


@login_required(login_url='/accounts/signin')
def chart_json(request):
    obj = login_inf.objects.get(subject_id="subject")
    subject_name = obj.subject_name
    table_name=obj.subject_info
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database='students'
    )
    cr = db.cursor()
    cr.execute(f"SELECT max(num) FROM {table_name}")
    result = cr.fetchall()
    attendance_number = result[0][0]
    try:
        attendance_number = result[0][0]
        absence_number=384-attendance_number
    except:
        attendance_number = 0
        absence_number = 384-attendance_number
    return JsonResponse({"attendance_number": attendance_number, "absence_number": absence_number,"subject_name":subject_name})
@login_required(login_url='/accounts/signin')
def bar_page(request):
    obj = login_inf.objects.get(subject_id="subject")
    subject_name = obj.subject_name
    return render(request,"Bar_page/bar_page.html",{"subject_name":subject_name})

@login_required(login_url='/accounts/signin')
def server_check(request):
    try:
        obj = server_state.objects.get(server_id="server")
    except:
        b=server_state(server_id="server")
        b.save()
    obj = server_state.objects.get(server_id="server")
    server_check = obj.server_state
    return JsonResponse({"server_state": server_check})
@login_required(login_url='/accounts/signin')
def bar_data(request):
    obj=login_inf.objects.get(subject_id="subject")
    table_name=obj.subject_name
    db2 = mysql.connector.connect(
       host="localhost",
       user="root",
       password="root",
       database='records'
   )
   
    cur=db2.cursor()
    cur.execute(f"SELECT  date,attendance FROM {table_name} ")
    data = cur.fetchall()
    for i in range(len(data)):
            data[i]=list(data[i])
    
    attendance=list()
    for i in range(len(data)):
       attendance.append(data[i][1])
    
    return JsonResponse({"data":attendance})

# Build paths inside the project like this: BASE_DIR / 'subdir'.
    
@login_required(login_url='/accounts/signin')
def restart(request):
    # Student.objects.all().delete()
    obj=restart_state.objects.get(restart_id="is_restarted")
    obj.restart_state=True
    obj.save()
    return JsonResponse({"restart_state":True})
