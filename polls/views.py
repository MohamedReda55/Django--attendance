# from django import views

from django.http import HttpResponse, response
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from accounts.models import qrcode_model,server_state,login_info
from .models import Student

class Main_view(View):
    #   polls/check/check.txt
   
        def submit(request,hash):
            get_data = qrcode_model.objects.get(qrcode_id="subject")
            if hash==get_data.qrcode_hash:
                obj = server_state.objects.get(server_id="server")
                if obj.server_state ==True:
                    if "submit" in request.session:
                    
                        return HttpResponse(f"you already submitted as {request.session['username']}")
                    obj = login_info.objects.get(subject_id="subject")
                    subject_name = obj.subject_name
                    return render(request,'submit.html',{"subject_name":subject_name})
                else:
                    return render(request,"state.html")
            else:
                raise response.Http404("wrong page")
      
        def post(request):
            if request.method=="POST":  
                 obj = server_state.objects.get(server_id="server")
                 if obj.server_state ==True:
                # if request.session.test_cookie_worked():
                #     request.session.delete_test_cookie()
                    obj = qrcode_model.objects.get(qrcode_id="subject")
                    if "submit" not in request.session: 
                        Name = request.POST['Student_Name']
                        ID = request.POST['Student_ID']
                        Check_code = request.POST['Student_Code']
                        if Check_code ==obj.check_code:
                            b = Student(name=Name,name_id=ID,check_code=Check_code)
                            b.save()
                            request.session["submit"] = True
                            request.session["username"]=Name
                            return redirect("/student/done")
                        else:
                            messages.warning(request, "wrong check code")
                            hash=obj.qrcode_hash
                            return redirect(f"/student/submit/{hash}")
                    else:
                      return render(request,"state.html")
                        # db = sqlite3.connect("students.db")
                        # cr = db.cursor()
                        # cr.execute(
                        #     "CREATE TABLE IF NOT EXISTS skills (username text,password text)")
                        
                        # # code=request.POST[]
                        # cr.execute(
                        #     f"INSERT INTO skills (username,password) values('{username}' ,'{password}')")
                        # db.commit()
                        # print(f"username:{username} ,password:{password}")
                        # return redirect("/student/done")



                # else:
                #     return HttpResponse("Please enable cookies and try again.")
                
            return redirect("submit")
        def home_page(request):
            try:
                username=request.session["username"]
            except:
                username=''
            return render(request, "thank.html",{"username":username})
    
