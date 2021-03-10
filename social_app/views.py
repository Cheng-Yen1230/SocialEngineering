from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse  # 重定向
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from social_app.models import Email, Data
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from social_app.forms import captcha_class


# https://docs.djangoproject.com/en/3.1/topics/email/
# https://docs.djangoproject.com/en/3.1/ref/templates/api/#django.template.Template.render

# Create your views here

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('show'))
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        captcha_ = captcha_class(request.POST)
        if captcha_.is_valid():
            auth.login(request, user)
            return redirect(reverse('show'))
        else:
            error = '驗證碼錯誤'
            captcha = captcha_class()
            return render(request, 'login.html', {'error': error, "captcha": captcha})
    else:
        if request.user.is_authenticated:
            return redirect(reverse('show'))
        else:
            captcha = captcha_class()
            return render(request, "login.html", {"captcha": captcha})


@login_required
def about(request):
    return render(request, 'about.html')


def index(request, num):
    try:
        from django.db.models import F
        if result := Email.objects.get(get_id=num):
            result.times = F('times') + 1
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
    response = request.method
    if response == "GET":
        bg_data = Data.objects.select_related('num')
    else:
        
        from django.http import HttpResponse
        import csv
        import codecs

        response = HttpResponse(content_type='text/csv')
        response.write(codecs.BOM_UTF8)
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        writer = csv.writer(response)
        writer.writerow(['流水號', '姓名', '信箱', '訪問時間'])
        d = Data.objects.all()
        for i in d:
            writer.writerow([i.num.get_id, i.num.name, i.num.email, i.pub_time])

        return response
    return render(request, 'data.html', locals())


# 個人詳細資料
@login_required
def personal(request, num):
    if values := Email.objects.get(get_id=num):
        pass
    pub = values.data.all()
    return render(request, 'personal.html', {'values': values, 'pub': pub})
