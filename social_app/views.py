from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse  # 重定向
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from social_app.models import Email, Data


# https://docs.djangoproject.com/en/3.1/topics/email/
# https://docs.djangoproject.com/en/3.1/ref/templates/api/#django.template.Template.render

# Create your views here.


islogin = False


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'Harry' and password == '12301230':
            global islogin
            islogin = True
            return redirect(reverse('show'))
        else:
            return render(request, 'login.html')

    

def verification(request, func):
    def wrapper(*args, **kwargs):
        global islogin
        if islogin:
            return func(*args, **kwargs)
        else:
            return render(request, 'nologin.html')
    return wrapper


@verification
def index(request, num):
    try:
        if result := Email.objects.get(get_id=num):
            result.times += 1
            result.save()
            Data.objects.create(num=result)
    except Exception as e:
        return redirect('https://shopee.tw/')

    return render(request, 'index.html')


#  郵件寄送
@verification
def mail(request):
    if request.method == 'GET':
        from social_app.models import Email
        data = Email.objects.all()
        return render(request, 'send.html', locals())
    else:
        subject, from_email = '蝦皮購物雙11開跑', settings.DEFAULT_FROM_EMAIL
        text_content = 'This is an important message.'

        from social_app.models import Email
        data = Email.objects.all()
        data_arr = list(data)
        from django.template import loader
        template = loader.get_template('mail.html')

        for e in data_arr:
            number = e.get_id
            html_content = template.render({'number': number})

            msg = EmailMultiAlternatives(
                subject, text_content, from_email, bcc=[e]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        return HttpResponse('寄送成功!')


# 郵件寄送 2
@verification
def remail(request):
    if request.method == "POST":
        data_list = request.POST.getlist('n')
        if data_list == []:
            return HttpResponse("沒有選取任何郵件")
        subject, from_email = '蝦皮購物雙11開跑', settings.DEFAULT_FROM_EMAIL
        text_content = 'This is an important message.'

        from social_app.models import Email
        template = loader.get_template('mail.html')

        for e in data_list:
            values = Email.objects.get(email=e)
            number = values.get_id
            html_conent = template.render({'number': number})
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, bcc=[e]
            )
            msg.attach_alternative(html_conent, "text/html")
            msg.send()
        return HttpResponse('寄送成功!')

    else:
        return HttpResponse('請不要直接訪問這個網址')


# 新增郵件
@verification
def set_add(request):
    if request.method == 'GET':
        data = Email.objects.all()
        return render(request, 'add.html', {'data': data})
    else:
        try:
            get_id = request.POST.get('id_add', '')
            get_id = int(get_id)
            name = request.POST.get('name', '')
            email = request.POST.get('mail', '')
            Email.objects.create(get_id=get_id, name=name, email=email)
            return redirect(reverse('show'))

        except IntegrityError as e:
            return HttpResponse('流水號重複!!!')
        except Exception as e:
            return HttpResponse('流水號只能是數字!!!')


# 刪除郵件
@verification
def set_delete(request):
    if request.method == 'GET':
        data = Email.objects.all()
        return render(request, 'delete.html', {'data': data})
    else:
        try:
            get_id = request.POST.get('id_del', '')
            get_id = int(get_id)
            name = request.POST.get('name', '')
            email = request.POST.get('mail', '')
            Email.objects.filter(get_id=get_id, name=name, email=email).delete()
            return redirect(reverse('show'))
        except Exception as e:
            return HttpResponse('流水號不能輸入文字')


# 顯示所有郵件資料
@verification
def show(request):
    data = Email.objects.all()
    return render(request, 'send.html', {'data': data})


# 選取寄送郵件
@verification
def select(request):
    data = Email.objects.all()
    return render(request, 'show.html', locals())


# 後台數據
@verification
def data(request):
    bg_data = Data.objects.all()
    return render(request, 'data.html', locals())


# 個人詳細資料
@verification
def personal(request, num):
    if values := Email.objects.get(get_id=num):
        pass
    pub = values.data.all()
    return render(request, 'personal.html', {'values': values, 'pub': pub})
