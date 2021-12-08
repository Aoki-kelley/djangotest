import datetime
import re
import uuid

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse

from message.models import Message, Reply
from .models import User, VerificationCode


class UserReg(forms.Form):
    username = forms.fields.CharField(max_length=32, required=True)
    password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)
    p_again = forms.fields.CharField(widget=forms.PasswordInput(), required=True)


class UserLog(forms.Form):
    username = forms.fields.CharField(max_length=32, required=True)
    password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)


class ResetName(forms.Form):
    newname = forms.fields.CharField(max_length=32, required=True)
    password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)


class EmailReg(forms.Form):
    email = forms.fields.EmailField(required=True)
    password = forms.fields.CharField(widget=forms.PasswordInput(), required=True)


class CodeProve(forms.Form):
    code = forms.fields.CharField(max_length=32, required=True)


# 错误挂起
def raise_wrong():
    return HttpResponse(status=404)


# 合法性检验
def check(l_s):  # 传入被检测字符串列表
    p = re.compile(r'^[A-Za-z0-9_-]*?')
    for s in l_s:
        result = p.match(s)
        if result is None:
            return False
    return True


# 注册
def register(req):
    if req.method == 'POST':
        uf = UserReg(req.POST)
        if uf.is_valid():
            # 获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            p_again = uf.cleaned_data['p_again']
            l_s = [username, password, p_again]
            if check(l_s):  # 合法性检验
                user = User.objects.filter(username__exact=username)
                if user:
                    data = {'name_exist': 'name_exist'}
                    return render(req, 'register.html', data)
                else:
                    if password != p_again:
                        data = {'p_not_same': 'p_not_same'}
                        return render(req, 'register.html', data)
                    else:
                        # 添加到数据库
                        User.objects.create(username=username,
                                            password=password,
                                            anonymity=str(uuid.uuid1())[0:7].upper())
                        data = {'ok': 'ok'}
                        return render(req, 'login.html', data)
            else:
                data = {'error': 'error'}
                return render(req, 'register.html', data)
        else:
            data = {'error': 'error'}
            return render(req, 'register.html', data)
    else:
        return render(req, 'register.html')


# 登陆
def login(req):
    if req.method == 'POST':
        uf = UserLog(req.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            l_s = [username, password]
            if check(l_s):  # 合法性检验
                # 获取的表单数据与数据库进行比较
                user = User.objects.filter(username__exact=username, password__exact=password)
                if user:
                    # 比较成功，跳转,写入浏览器cookie,失效时间为14400
                    ret = redirect('/user/jump/')
                    ret.set_cookie('is_login', username, 14400)
                    return ret
                else:
                    # 比较失败，还在login
                    data = {'error': 'error'}
                    return render(req, 'login.html', data)
            else:
                data = {'error': 'error'}
                return render(req, 'login.html', data)
        else:
            data = {'error': 'error'}
            return render(req, 'login.html', data)
    else:
        return render(req, 'login.html')


# 登陆成功
def jump(req):
    if req.COOKIES.get('is_login') is not None:
        return render(req, 'jump.html')
    else:
        # data = {'login_no': 'login_no'}
        return redirect('/user/login/')


# 退出登录
def logout(req):
    if req.COOKIES.get('is_login') is not None:
        ret = redirect('/')
        # 清理cookie里保存username
        ret.delete_cookie('is_login')
        return ret
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 跳转主页
def home(req):
    # username = req.COOKIES.get('is_login')
    # print(username)
    result = Message.objects.all().order_by('-date')
    '''for message in result:
        username = message.username
        user = User.objects.get(username=username)
        print(message)'''
    # print(result)
    '''paginator = Paginator(result, 8)
    page_num = req.GET.get('page', 1)
    page_of_messages=paginator.get_page(page_num)'''
    data = {'result': result}
    username = req.COOKIES.get('is_login')
    if username is not None:
        user = User.objects.get(username=username)
        username = user.username
        data.update({'is_login': 'is_login', 'username': username})
        # print(data)
        return render(req, 'home.html', data)
    else:
        data.update({'not_login': 'not_login'})
        return render(req, 'home.html', data)


# 个人主页
def mine(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        user = User.objects.get(username=username)
        result = Message.objects.filter(username=username)
        # print(result)
        data = {'user': user, 'result': result}
        # print(user.email)
        if user.email != 'NONE':
            data.update({'email_have': 'email_have'})
        return render(req, 'mine.html', data)
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 用户名重设
def reset_name(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        if req.method == 'POST':
            uf = ResetName(req.POST)
            data = {}
            if uf.is_valid():
                newname = uf.cleaned_data['newname']
                password = uf.cleaned_data['password']
                l_s = [newname]
                user = User.objects.get(username__exact=username, password__exact=password)
                message = Message.objects.filter(username__exact=username)
                reply = Reply.objects.filter(username__exact=username)
                if user:
                    if check(l_s):
                        if User.objects.filter(username__exact=newname):
                            data.update({'name_exist': 'name_exist'})
                            return render(req, 'reset_name.html', data)
                        else:
                            user.username = newname
                            user.save()
                            for i in range(len(message)):
                                message[i].username = newname
                                message[i].save()
                            for i in range(len(reply)):
                                reply[i].username = newname
                                reply[i].save()
                            ret = redirect('/user/login/')
                            # 清理cookie里保存username
                            ret.delete_cookie('is_login')
                            return ret
                    else:
                        # print(1)
                        data.update({'error': 'error'})
                        return render(req, 'reset_name.html', data)
                else:
                    # print(2)
                    data.update({'error': 'error'})
                    return render(req, 'reset_name.html', data)
            else:
                # print(3)
                data.update({'error': 'error'})
                return render(req, 'reset_name.html', data)
        else:
            return render(req, 'reset_name.html')
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 匿名重设
def reset_ano(req):
    if req.COOKIES.get('is_login') is not None:
        username = req.COOKIES.get('is_login')
        user = User.objects.get(username=username)
        user.anonymity = str(uuid.uuid1())[0:7].upper()
        user.save()
        return redirect('/user/mine/')
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 邮箱验证界面
def email_reg(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        if req.method == 'POST':
            uf = EmailReg(req.POST)
            if uf.is_valid():
                email = uf.cleaned_data['email']
                password = uf.cleaned_data['password']
                user = User.objects.filter(username__exact=username, password__exact=password)
                if user:
                    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
                        target = VerificationCode.objects.filter(username__exact=username)
                        if target:
                            target.code = ''
                            target.save()
                        else:
                            VerificationCode.objects.create(email=email, code='',
                                                            date=datetime.datetime.now(), username=username)
                        data = {'ok': 'ok'}
                        return render(req, 'email_reg.html', data)
                    else:
                        data = {'error': 'error'}
                        return render(req, 'email_reg.html', data)
                else:
                    data = {'error': 'error'}
                    return render(req, 'email_reg.html', data)
            else:
                data = {'error': 'error'}
                return render(req, 'email_reg.html', data)
        else:
            return render(req, 'email_reg.html')
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 发送验证码
def send_code(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        target = VerificationCode.objects.get(username__exact=username)
        # print(target)
        email = target.email
        target.code = str(uuid.uuid1())[0:5].upper()
        target.date = datetime.datetime.now()
        target.save()
        data = {'email': email}
        status = send_mail(subject='Verification Code', message=target.code,
                           from_email=settings.EMAIL_FROM, recipient_list=[email])
        if status:
            data.update({'ok': 'ok'})
            return render(req, 'send_code.html', data)
        else:
            data.update({'error': 'error'})
            return render(req, 'send_code.html', data)
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 验证邮箱
def email_prove(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        time_limit = 5  # 验证码有效时长(分钟)
        uf = CodeProve(req.POST)
        target = VerificationCode.objects.get(username__exact=username)
        if uf.is_valid():
            code = uf.cleaned_data['code']
            user = User.objects.get(username__exact=username)
            time_now = datetime.datetime.now()
            gap = (time_now - target.date).total_seconds() / 60
            # print(gap)
            if gap > time_limit:
                data = {'time_out': 'time_out', 'email': target.email}
                # target.delete()
                return render(req, 'send_code.html', data)
            else:
                if code == target.code:
                    user.email = target.email
                    user.save()
                    target.delete()
                    return redirect('/user/mine/')
                else:
                    data = {'code_wrong': 'code_wrong', 'email': target.email}
                    return render(req, 'send_code.html', data)
        else:
            data = {'code_wrong': 'code_wrong', 'email': target.email}
            return render(req, 'send_code.html', data)
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 删贴
def delete(req, mid):
    if req.COOKIES.get('is_login') is not None:
        username = req.COOKIES.get('is_login')
        user = User.objects.get(username=username)
        target = Message.objects.get(id=mid)
        if target.username == username:
            target.delete()
        '''result = Message.objects.filter(username=username)
        # print(result)
        data = {'anonymity': user.anonymity, 'result': result}
        # print(user.email)
        if user.email != 'NONE':
            data.update({'email_have': 'email_have'})
        return render(req, 'mine.html', data)'''
        return redirect('/user/mine/')
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)
