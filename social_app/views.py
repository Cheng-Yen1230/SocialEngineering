from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse  # 重定向
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from social_app.models import Email, Data
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# https://docs.djangoproject.com/en/3.1/topics/email/
# https://docs.djangoproject.com/en/3.1/ref/templates/api/#django.template.Template.render

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('show'))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    code = request.POST.get('code1', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active and code == '比目魚肌腺':
        auth.login(request, user)
        return redirect(reverse('show'))
    else:
        if request.user.is_authenticated:
            return redirect(reverse('show'))
        from random import sample
        code = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        rcode = ''.join(sample(code, 4))
        return render(request, 'login.html', {'rcode': rcode})


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
def show(request):
    data = Email.objects.all()
    return render(request, 'send.html', {'data': data})


# 選取寄送郵件
@login_required
def select(request):
    data = Email.objects.all()
    return render(request, 'show.html', locals())


# 後台數據
@login_required
def data(request):
    bg_data = Data.objects.all()
    return render(request, 'data.html', locals())


# 個人詳細資料
@login_required
def personal(request, num):
    if values := Email.objects.get(get_id=num):
        pass
    pub = values.data.all()
    return render(request, 'personal.html', {'values': values, 'pub': pub})
