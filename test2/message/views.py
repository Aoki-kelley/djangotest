import datetime
import random

from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse

from user.models import User
from .models import Message, Reply


class MessagePut(forms.Form):
    title = forms.fields.CharField(required=True, max_length=32)
    content = forms.fields.CharField(required=True, max_length=256)


class ReplyPut(forms.Form):
    content = forms.fields.CharField(required=True, max_length=256)


# 帖子详细
def detail(req, mid):
    # print(mid)
    # print(type(Message), type(Reply))
    try:
        message = Message.objects.get(id=mid)
        replies = Reply.objects.filter(mid_id=mid)
        data = {'message': message}
        username = req.COOKIES.get('is_login')
        if replies:
            data.update({'replies': replies})
        if username is not None:
            user = User.objects.get(username=username)
            username = user.username
            data.update({'is_login': 'is_login', 'username': username})
        return render(req, 'detail.html', data)
    except:
        return HttpResponse(status=404)


# 留言
def leave_massage(req):
    username = req.COOKIES.get('is_login')
    if req.COOKIES.get('is_login') is not None:
        uf = MessagePut(req.POST)
        if uf.is_valid():
            title = uf.cleaned_data['title']
            content = uf.cleaned_data['content']
            user = User.objects.get(username=username)
            # print(title, content)
            Message.objects.create(username=username,
                                   anonymity=user.anonymity,
                                   title=title,
                                   content=content,
                                   # date=(datetime.datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"))
                                   date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

        return redirect('/')
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)


# 随机留言
def message_random(req):
    messages = Message.objects.all()
    # print(messages)
    data = {}
    username = req.COOKIES.get('is_login')
    if username is not None:
        data.update({'username': username, 'is_login': 'is_login'})
    if messages:
        l = len(messages)
        index = random.randint(0, l - 1)
        # print(index)
        [messages[index]].reverse()
        result = [messages[index]]
        # print(result)
        data.update({'result': result})
        username = req.COOKIES.get('is_login')
        if username is not None:
            data.update({'username': username})
        return render(req, 'home.html', data)
    return render(req, 'home.html', data)


# 回复
def leave_reply(req, mid):
    username = req.COOKIES.get('is_login')
    if req.COOKIES.get('is_login') is not None:
        uf = ReplyPut(req.POST)
        if uf.is_valid():
            content = uf.cleaned_data['content']
            user = User.objects.get(username=username)
            Reply.objects.create(mid_id=mid,
                                 username=username,
                                 anonymity=user.anonymity,
                                 content=content,
                                 date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        return redirect('/message/detail/{0}/'.format(mid))
    else:
        data = {'login_no': 'login_no'}
        return render(req, 'login.html', data)
