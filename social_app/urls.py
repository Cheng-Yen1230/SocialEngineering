from . import views
from django.urls import path

urlpatterns = [

    path('<int:num>/test', views.index, name='index'),
    path('data', views.data, name='data'),
    path('email', views.show, name='show'),
    path('send', views.mail, name='mail'),
    path('add_mail', views.set_add, name='add_'),
    path('del_mail', views.set_delete, name='del_'),
    path('select', views.select, name='select'),
    path('remail', views.remail, name='remail'),
    path('personal/<int:num>', views.personal, name='content'),
    path('', views.login, name='login'),

]
