from django.urls import path
from . import views
app_name="accounts"
urlpatterns=[
    path('signup/',views.singnup,name="signup"),
    path('signin/',views.login_page,name='logins'),
    path('logout',views.signout,name='logout'),
    path('tables/', views.tables, name='tables'),
    path("home", views.home, name="home"),
    path('post/ajax/data',views.post_data,name='post_data'),
    path('post/ajax/info', views.chart_json, name='chart_json'),
    # path('test', views.test, name='test'),
    path("qrcode/generate", views.qrcode_generate,name="qrcode_generate"),
    path("qrcode/view",views.qrcode_page,name="qrcode_page"),
    # path("export",views.export_csv,name="export_csv"),
    path("csv_home", views.csv_home, name="csv_home"),
    path("server/start", views.start_server, name="start_server"),
    path("server/stop", views.stop_server, name="stop_server"),
    path("bar", views.bar_page, name="bar"),
    path("bar/data", views.bar_data, name="bar_data"),
    path("post/ajax/server/state", views.server_check, name="server_state"),
    
    
             
]