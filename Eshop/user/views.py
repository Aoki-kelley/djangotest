import datetime
import os
import re

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from trade.models import Goods
from trade.forms import SearchGoods
from user.models import User, VerificationCode
from user.tasks import SendEmailTask

from user.forms import *


def raise_wrong(req):  # 错误挂起
    return HttpResponse(status=404)


def check(l_s):  # 传入被检测字符串列表
    p = re.compile(r'^[A-Za-z0-9-]{1,8}')
    for s in l_s:
        result = p.match(s)
        if result is None:
            return False
    return True


def home(req):
    goods_list = Goods.objects.filter(status='on').order_by('-date')
    paginator = Paginator(goods_list, 2)
    page_num = int(req.GET.get('page', 1))
    page_goods = paginator.get_page(page_num)
    data = {'page_goods': page_goods, 'now_page': page_num}
    username = req.COOKIES.get('is_login')
    if username is not None and User.objects.filter(username__exact=username, status='on'):
        user = User.objects.filter(username__exact=username, status='on')[0]
        data.update({'is_login': 'is_login', 'image': user.image, 'form': SearchGoods()})
    return render(req, 'home.html', data)


def send_again(req, username, label='register'):
    # if req.method == 'GET':
    # return raise_wrong(req)
    # else:
    if label == 'register':
        try:
            user = User.objects.filter(username__exact=username, email_proved__exact='off')[0]
            email = user.email[0: int(len(user.email.split('@')[0]) / 2)] + '*****@' + user.email.split('@')[1]
            send_task = SendEmailTask()
            send_task.run(user.email, username, label)
            data = {'ok': 'ok', 'username': username, 'email': email}
            return render(req, 'email_reg.html', data)
        except IndexError:
            return raise_wrong(req)
    elif label == 'reset_password':
        try:
            user = User.objects.filter(username__exact=username, email_proved__exact='on')[0]
            send_task = SendEmailTask()
            send_task.run(user.email, username, label)
            data = {'ok': 'ok', 'form': PasswordChange(), 'username': username, 'email': user.email}
            return render(req, 'reset_password.html', data)
        except IndexError:
            return raise_wrong(req)
    else:
        return raise_wrong(req)


def register(req, role):
    form = UserReg()
    data = {'form': form}
    if role in ['seller', 'buyer']:
        data.update({'role': role})
    if req.method == 'POST':
        uf = UserReg(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            p_again = uf.cleaned_data['p_again']
            email = uf.cleaned_data['email']
            # captcha = uf.cleaned_data['captcha']
            l_s = [username, password, p_again]
            # judge = len(password) > 6 and len(p_again) > 6
            # if check(l_s) and judge and re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            if check(l_s) and re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
                user = User.objects.filter(username__exact=username)
                email_ext = User.objects.filter(email=email, email_proved='on', role=role)
                if user or email_ext:
                    if user:
                        data.update({'name_exist': 'name_exist'})
                        return render(req, 'register.html', data)
                    elif email_ext:
                        data.update({'email_exist': 'email_exist'})
                        return render(req, 'register.html', data)
                else:
                    if password != p_again:
                        data.update({'p_not_same': 'p_not_same'})
                        return render(req, 'register.html', data)
                    else:  # 添加到数据库
                        try:
                            send_task = SendEmailTask()
                            send_task.run(email, username)
                            User.objects.create(username=username,
                                                password=password,
                                                email=email,
                                                role=role)
                            data.update({'username': username, 'email': email, 'ok': 'ok'})
                            return render(req, 'email_reg.html', data)
                        except:
                            data.update({'username': username, 'email': email, 'error': 'error'})
                            return render(req, 'email_reg.html', data)
            else:
                data.update({'error': 'error'})
                return render(req, 'register.html', data)
        else:
            # print(3)
            data.update({'error': 'error'})
            return render(req, 'register.html', data)
    else:
        if role in ['seller', 'buyer']:
            data.update({'role': role})
            return render(req, 'register.html', data)
        else:
            return raise_wrong(req)


def email_prove(req, username):  # 邮箱验证
    if req.method == 'POST':
        time_limit = 5  # 验证码有效时长(分钟)
        uf = CodeProve(req.POST)
        target = VerificationCode.objects.get(username__exact=username)
        data = {'username': target.username, 'email': target.email}
        if uf.is_valid():
            code = uf.cleaned_data['code']
            user = User.objects.get(username__exact=username)
            time_now = datetime.datetime.now()
            gap = (time_now - target.date).total_seconds() / 60
            # print(gap)
            if gap > time_limit:
                data.update({'time_out': 'time_out'})
                # target.delete()
                return render(req, 'email_reg.html', data)
            else:
                if code == target.code:
                    user.status = 'on'
                    user.email_proved = 'on'
                    user.save()
                    target.delete()
                    ret = redirect('/')
                    ret.set_cookie('is_login', username, 14400)
                    return ret
                else:
                    data.update({'code_wrong': 'code_wrong'})
                    return render(req, 'email_reg.html', data)
        else:
            data.update({'code_wrong': 'code_wrong'})
            return render(req, 'email_reg.html', data)
    else:
        data = {'email_change': 'email_change', 'username': username}
        return render(req, 'email_reg.html', data)


def login(req):  # 登录
    data = {'form': UserLog()}
    if req.method == 'POST':
        uf = UserLog(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # captcha = uf.cleaned_data['captcha']
            l_s = [username, password]
            if check(l_s):  # 合法性检验
                try:
                    user = User.objects.get(username__exact=username, password__exact=password)
                    if user.status == 'on':
                        if user.email_proved == 'on':
                            ret = redirect('/')
                            ret.set_cookie('is_login', username, 14400)
                            return ret
                        else:
                            data = {'username': user.username, 'email': user.email, 'illegal': 'illegal'}
                            return render(req, 'email_reg.html', data)
                    else:
                        data.update({'status_off': 'status_off'})
                        return render(req, 'login.html', data)
                except:
                    data.update({'error': 'error'})
                    return render(req, 'login.html', data)

        else:
            data.update({'error': 'error'})
            return render(req, 'login.html', data)
    else:
        return render(req, 'login.html', data)


def logout(req):  # 退出登录
    if req.COOKIES.get('is_login') is not None:
        ret = redirect('/')
        ret.delete_cookie('is_login')
        return ret
    else:
        return raise_wrong(req)


def mine(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        user = User.objects.filter(username__exact=username, status='on')[0]
        # print(result)
        data = {'user': user}
        return render(req, 'mine.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def reset_name(req):  # 用户名重设
    username = req.COOKIES.get('is_login')
    if username is not None and User.objects.filter(username__exact=username, status='on'):
        if req.method == 'POST':
            uf = ResetName(req.POST)
            data = {}
            if uf.is_valid():
                new_name = uf.cleaned_data['new_name']
                password = uf.cleaned_data['password']
                l_s = [new_name]
                target = User.objects.filter(username__exact=username, password__exact=password)
                if target:
                    user = target[0]
                    if check(l_s):
                        if User.objects.filter(username__exact=new_name):
                            data.update({'name_exist': 'name_exist'})
                            return render(req, 'reset_name.html', data)
                        else:
                            user.username = new_name
                            user.save()
                            ret = redirect('/user/login/')
                            ret.delete_cookie('is_login')
                            return ret
                else:
                    data.update({'pwd_wrong': 'pwd_wrong'})
                    return render(req, 'reset_name.html', data)
            else:
                data.update({'error': 'error'})
                return render(req, 'reset_name.html', data)
        else:
            return render(req, 'reset_name.html')
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def reset_password(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        user = User.objects.filter(username__exact=username, status='on')[0]
        if user:
            email = user.email[0: int(len(user.email.split('@')[0]) / 2)] + '*****@' + user.email.split('@')[1]
            data = {'username': username, 'email': email}
            if req.method == 'POST':
                uf = PasswordChange(req.POST)
                time_limit = 5
                if uf.is_valid():
                    new_password = uf.cleaned_data['new_password']
                    p_again = uf.cleaned_data['p_again']
                    code = uf.cleaned_data['code']
                    l_s = [new_password, p_again]
                    # judge = len(new_password) > 6 and len(p_again) > 6
                    # if check(l_s) and judge:
                    if check(l_s):
                        time_now = datetime.datetime.now()
                        target = VerificationCode.objects.filter(username__exact=username)[0]
                        gap = (time_now - target.date).total_seconds() / 60
                        if gap > time_limit:
                            data.update({'time_out': 'time_out'})
                            # target.delete()
                            return render(req, 'reset_password.html', data)
                        else:
                            if code == target.code:
                                user.password = new_password
                                user.save()
                                target.delete()
                                ret = redirect('/user/login/')
                                ret.delete_cookie('is_login')
                                return ret
                            else:
                                data.update({'wrong': 'wrong'})
                                return render(req, 'reset_password.html', data)
                else:
                    # print(3)
                    data.update({'wrong': 'wrong'})
                    return render(req, 'reset_password.html', data)
            else:
                return render(req, 'reset_password.html', data)
        else:
            data = {'login_no': 'login_no', 'form': UserLog}
            return render(req, 'login.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def reset_image(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        data = {'form': ImageChange()}
        if req.method == 'POST':
            uf = ImageChange(req.POST, req.FILES)
            if uf.is_valid():
                user = User.objects.filter(username__exact=username, status='on')[0]
                path = 'media/user_image/{id}.png'.format(id=user.id)
                if os.path.exists(path):
                    os.remove(path)
                image = uf.cleaned_data['image']
                ext = image.name.split(".")[-1].lower()
                image.name = str(user.id) + '.' + ext
                # print(image.name)
                user.image = image
                user.save()
                return redirect('/user/mine/')
            else:
                return render(req, 'reset_image.html', data)
        else:
            return render(req, 'reset_image.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def add_money(req):
    username = req.COOKIES.get('is_login')
    if username is not None:
        try:
            user = User.objects.filter(username__exact=username, status='on', role='buyer')[0]
            data = {'form': AddMoney(), 'user': user}
            if req.method == 'POST':
                uf = AddMoney(req.POST)
                if uf.is_valid():
                    money = uf.cleaned_data['money']
                    judge = len((str(money).split('.')[1])) <= 2
                    if 10 <= money <= 10000 and judge:
                        user.money = money + user.money
                        user.save()
                        return redirect('/user/mine/')
                    else:
                        data.update({'error': 'error'})
                        return render(req, 'add_money.html', data)
                else:
                    data.update({'error': 'error'})
                    return render(req, 'add_money.html', data)
            else:
                return render(req, 'add_money.html', data)
        except IndexError:
            return raise_wrong(req)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def forget_pwd(req):
    if req.method == 'POST':
        uf = ForgetPwd(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            email = uf.cleaned_data['email']
            try:
                User.objects.filter(username__exact=username, status='on', email=email, email_proved='on')[0]
            except IndexError:
                return render(req, 'forget_pwd.html', {'wrong': 'wrong', 'form': ForgetPwd()})
            return send_again(req, username, 'reset_password')
    else:
        return render(req, 'forget_pwd.html', {'form': ForgetPwd()})
