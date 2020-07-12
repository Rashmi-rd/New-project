from django.contrib import admin
from django.conf.urls import url
from . import views


urlpatterns = [
    url('^$', views.register, name="register"),
    url('^login/$', views.user_login, name="login"),
    url('^user_dash/$', views.user_dash, name="user_dash"),
    url('^admin_panel/$', views.admin_page, name="admin_panel"),
    url('^delete/$', views.DeleteUser.as_view(), name="delete"),
    url('^picdelete/$', views.DeletePic.as_view(), name="DeletePic"),
    url('^disapprove/$', views.DisapproveUser.as_view(), name="disapprove"),
    url('^approve/$', views.ApproveUser.as_view(), name="approve"),
    url('^logout/$', views.user_logout, name="logout"),
]