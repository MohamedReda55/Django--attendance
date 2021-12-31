# from django import views

from django.http import HttpResponse, response
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from accounts.models import qrcode_model,server_state,login_inf
from .models import Student
from accounts.models import restart_state
import time
import mysql.connector
class Main_view(View):
    #   polls/check/check.txt
   
        def submit(request,hash):
              
                try:
                    get_data = qrcode_model.objects.get(qrcode_id="subject")
                except:
                    c=qrcode_model(qrcode_id="subject")
                    c.save()
                get_data = qrcode_model.objects.get(qrcode_id="subject")
                if hash==get_data.qrcode_hash:
                    try:
                            obj = server_state.objects.get(server_id="server")
                    except:
                             v=server_state(server_id="server")
                             v.save()
                    obj = server_state.objects.get(server_id="server")
                    if obj.server_state ==True:
                        if "submit" in request.session:
                            try:
                                restart_value = restart_state.objects.get(
                                    restart_id="res")
                            except:
                                b = restart_state(restart_id="res")
                                b.save()
                            restart_value = restart_state.objects.get(
                                restart_id="res")
                            if restart_value.restart_state:
                                del request.session['submit']
                                del request.session['username']
                                restart_value.restart_state=False
                                restart_value.save()
                                return redirect(f"/student/submit/{get_data.qrcode_hash}")
                            return HttpResponse(f"you already submitted as {request.session['username']}")
                        obj = login_inf.objects.get(subject_id="subject")
                        subject_name = obj.subject_name
                        return render(request, 'submit.html', {"subject_name": subject_name.replace("_", " ")})
                    else:
                        return render(request,"time_up.html")
                else:
                    raise response.Http404("wrong page")
      
        def post(request):
            if request.method=="POST":  
                try: 
                    obj = server_state.objects.get(server_id="server")
                except:
                    v=server_state(server_id="server")
                    v.save()
                obj = server_state.objects.get(server_id="server")
                if obj.server_state ==True:
                        try:
                            obj = qrcode_model.objects.get(qrcode_id="subject")
                        except:
                            c=qrcode_model(qrcode_id="subject")
                            c.save()
                        # restart_value = restart_state.objects.get(restart_id="is_restarted")
                        obj = qrcode_model.objects.get(qrcode_id="subject")
                        if "submit" not in request.session: 
                            Name = request.POST['Student_Name']
                            ID = request.POST['Student_ID']
                            Check_code = request.POST['Student_Code']
                            
                            if Check_code ==obj.check_code:
                                
                                
                                # time_now = time.time()
                                # time_to=time_now+5400
                                # b = Student(name=Name, name_id=ID,
                                #             check_code=Check_code)
                                # b.save()
                                b=login_inf.objects.get(subject_id="subject")
                                table_name = b.subject_info
                                db = mysql.connector.connect(
                                    host="localhost",
                                    user="root",
                                    password="root",
                                    database='students'
                                )
                                print(table_name)
                                sql = "INSERT INTO "+table_name+"(ID , name) VALUES(%s,%s)"
                                cr = db.cursor()
                                cr.execute(sql,(str(ID),Name))
                                db.commit()
                                request.session["submit"] = True
                                request.session["username"]=Name
                                return redirect("/student/done")
                            else:
                                messages.warning(request, "wrong check code")
                                hash=obj.qrcode_hash
                                return redirect(f"/student/submit/{hash}")
                        else:
                            
                            return HttpResponse(f"you already submitted as {request.session['username']}")
                                         
                else:
                   
                    return render(request, "time_up.html")
            return redirect("submit")
        def home_page(request):
            try:
                username=request.session["username"]
            except:
                username=''
            return render(request, "thanks_page.html",{"username":username})
    
