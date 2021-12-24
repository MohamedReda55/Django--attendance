
from django.urls import path, re_path
# from django.conf.urls import url 
from . import views
# from accounts.models import qrcode_model
# hash_read = open(f"static/qr_code/hash.txt", "r")
# hash = hash_read.read()
# t = qrcode_model.objects.get(qrcode_id="subject")
# print(t.qrcode_hash)
app_name="home"
urlpatterns = [
    re_path(r'submit/(?P<hash>[0-9a-zA-Z]{20})', views.Main_view.submit, name='submit'),
    path('store',views.Main_view.post,name="store"),
    path('done', views.Main_view.home_page, name='done'),
]
