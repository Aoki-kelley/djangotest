from django.http import HttpResponse
from django.shortcuts import render, redirect

from trade.models import Goods
from user.forms import UserLog
from user.models import User
from .forms import *

import datetime


def raise_wrong(req):  # 错误挂起
    return HttpResponse(status=404)


def leave_comment(req, gid):
    if req.method == 'GET':
        return raise_wrong(req)
    else:
        if not str(gid).isdigit():
            return raise_wrong(req)
        else:
            username = req.COOKIES.get('is_login')
            if username is not None and User.objects.filter(username__exact=username, status='on', role='buyer'):
                user = User.objects.filter(username__exact=username, status='on', role='buyer')[0]
                uf = LeaveComment(req.POST)
                if uf.is_valid():
                    title = uf.cleaned_data['title']
                    content = uf.cleaned_data['content']
                    Comment.objects.create(goods=gid, title=title, content=content,
                                           date=datetime.datetime.now(), user_id=user.id)
                return redirect('/trade/goods_detail/{gid}/'.format(gid=gid))
            else:
                data = {'login_no': 'login_no', 'form': UserLog()}
                return render(req, 'login.html', data)


def reply_comment(req, cid):
    if req.method == 'GET':
        return raise_wrong(req)
    else:
        if not str(cid).isdigit():
            return raise_wrong(req)
        else:
            username = req.COOKIES.get('is_login')
            if username is not None and User.objects.filter(username__exact=username, status='on'):
                uf = LeaveReply(req.POST)
                if uf.is_valid():
                    content = uf.cleaned_data['content']
                    comment = Comment.objects.filter(id=cid)[0]
                    user = User.objects.filter(username__exact=username, status='on')[0]
                    if user.role == 'seller':
                        floor = -1
                    else:
                        floor = 0
                    Reply.objects.create(content=content, date=datetime.datetime.now(), from_user=user.id,
                                         to_user=comment.user.id, floor=floor, comment_id=cid)
                return redirect('/comment/comment_detail/{cid}/'.format(cid=cid))
            else:
                data = {'login_no': 'login_no', 'form': UserLog()}
                return render(req, 'login.html', data)


def reply_reply(req, rid):
    if req.method == 'GET':
        data = {'form': LeaveReply(), 'rid': rid}
        return render(req, 'reply_reply.html', data)
    else:
        if not str(rid).isdigit():
            return raise_wrong(req)
        else:
            username = req.COOKIES.get('is_login')
            if username is not None and User.objects.filter(username__exact=username, status='on'):
                uf = LeaveReply(req.POST)
                if uf.is_valid():
                    content = uf.cleaned_data['content']
                    user = User.objects.filter(username__exact=username, status='on')[0]
                    reply = Reply.objects.filter(id=rid)[0]
                    if user.role == 'seller':
                        floor = 2
                    else:
                        floor = 1
                    Reply.objects.create(content=content, date=datetime.datetime.now(), from_user=user.id,
                                         to_user=reply.from_user, floor=floor, comment_id=reply.comment_id, )
                    return redirect('/comment/comment_detail/{cid}/'.format(cid=reply.comment_id))
            else:
                data = {'login_no': 'login_no', 'form': UserLog()}
                return render(req, 'login.html', data)


def comment_detail(req, cid):
    if not str(cid).isdigit():
        return raise_wrong(req)
    else:
        username = req.COOKIES.get('is_login')
        if username is not None and User.objects.filter(username__exact=username, status='on'):
            try:
                comment = Comment.objects.filter(id=cid)[0]
                user = User.objects.filter(username__exact=username, status='on')[0]
                goods = Goods.objects.filter(id=comment.goods)[0]
            except IndexError:
                return raise_wrong(req)
            replies = Reply.objects.filter(comment_id=cid).order_by('floor')
            data = {'form': LeaveReply(), 'comment': comment, 'replies': [],
                    'goods': goods, 'user': user, 'cid': cid}
            if list(replies):
                for reply in replies:
                    from_user = User.objects.filter(id=reply.from_user)[0]
                    to_user = User.objects.filter(id=reply.to_user)[0]
                    data['replies'].append((reply, from_user, to_user))
            return render(req, 'detail_comment.html', data)
        else:
            data = {'login_no': 'login_no', 'form': UserLog()}
            return render(req, 'login.html', data)


def mine_comment_reply(req):
    username = req.COOKIES.get('is_login')
    if username is not None and User.objects.filter(username__exact=username, status='on'):
        user = User.objects.filter(username__exact=username, status='on')[0]
        data = {'comments': [], 'replies': [], 'user': user}
        comments = Comment.objects.filter(user=user)
        replies = Reply.objects.filter(from_user=user.id)
        if comments:
            for cm in comments:
                goods = Goods.objects.filter(id=cm.goods)[0]
                data['comments'].append((cm, goods))
        if replies:
            for rp in replies:
                goods = Goods.objects.filter(id=rp.comment.goods)[0]
                data['replies'].append((rp, goods))
        return render(req, 'mine_comment_reply.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def delete(req, style, cr_id):
    username = req.COOKIES.get('is_login')
    if username is not None and User.objects.filter(username__exact=username, status='on'):
        if style == 'comment':
            try:
                target = Comment.objects.filter(id=cr_id)[0]
            except IndexError:
                return raise_wrong(req)
            target.delete()
            return redirect('/comment/mine_comment_reply/')
        elif style == 'reply':
            try:
                target = Reply.objects.filter(id=cr_id)[0]
            except IndexError:
                return raise_wrong(req)
            target.delete()
            return redirect('/comment/mine_comment_reply/')
        else:
            return raise_wrong(req)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)
