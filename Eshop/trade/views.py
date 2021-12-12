import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from trade.models import *
from trade.forms import *
from user.forms import *


def raise_wrong(req):  # 错误挂起
    return HttpResponse(status=404)


def is_signed_int(s):  # str s
    for i in s:
        if '0' <= i <= '9':
            continue
        else:
            return False
    else:
        return True


def mien_goods(req):
    username = req.COOKIES.get('is_login')
    target = User.objects.filter(username__exact=username, status='on', role='seller')
    if username is not None and target:
        user = target[0]
        data = {'username': username}
        if Goods.objects.filter(seller__exact=user.id):
            result = Goods.objects.filter(seller__exact=user.id)
            data.update({'result': result})
        else:
            data.update({'no_goods': 'no_goods'})
        return render(req, 'mine_goods.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def goods_create(req):  # 商品创建
    username = req.COOKIES.get('is_login')
    if username is not None:
        data = {'form': CreateGoods()}
        if req.method == 'POST':
            uf = CreateGoods(req.POST, req.FILES)
            if uf.is_valid():
                image = uf.cleaned_data['image']
                title = uf.cleaned_data['title']
                detail = uf.cleaned_data['detail']
                label = uf.cleaned_data['label']
                price = uf.cleaned_data['price']
                amount = uf.cleaned_data['amount']
                date_now = datetime.datetime.now()
                user = User.objects.filter(username__exact=username, status='on')[0]
                labels = [(1, '小说'), (2, '文学'), (3, '艺术'), (4, '动漫/幽默'), (5, '娱乐时尚'),
                          (6, '旅游'), (7, '地图/地理'), (8, '科学技术')]
                # print(uf.cleaned_data)
                last_goods = Goods.objects.last()
                if last_goods is None:
                    ext = image.name.split(".")[-1].lower()
                    image.name = str(1) + '.' + ext
                else:
                    ext = image.name.split(".")[-1].lower()
                    image.name = str(last_goods.id + 1) + '.' + ext
                lb = labels[int(label) - 1][1]
                if 0 < float(price) <= 999999 and len((str(price).split('.')[1])) <= 2:
                    Goods.objects.create(image=image, title=title, detail=detail, label=lb,
                                         price=price, amount=amount, date=date_now, seller_id=user.id)
                    return redirect('/trade/mine_goods/')
                else:
                    data.update({'error': 'error'})
                    return render(req, 'goods_create.html', data)
            else:
                data.update({'error': 'error'})
                return render(req, 'goods_create.html', data)
        else:
            return render(req, 'goods_create.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def change_goods(req, gid):
    if not gid.isdigit():
        return raise_wrong(req)
    else:
        username = req.COOKIES.get('is_login')
        if username is not None:
            target = Goods.objects.filter(id=gid)
            if req.method == 'POST':
                detail = req.POST.get('detail')
                price = req.POST.get('price')
                amount = req.POST.get('amount')
                goods = target[0]
                if price:
                    if 0 < float(price) <= 999999 and len((str(price).split('.')[1])) <= 2:
                        goods.price = price
                        goods.save()
                    else:
                        data = {'goods': target[0], 'form': ChangeGoods(), 'error_p': 'error_p'}
                        return render(req, 'goods_change.html', data)
                if amount:
                    if 0 < int(amount) < 999999 and is_signed_int(amount):
                        goods.amount = amount
                        goods.save()
                    else:
                        data = {'goods': target[0], 'form': ChangeGoods(), 'error_a': 'error_a'}
                        return render(req, 'goods_change.html', data)
                if detail:
                    goods.detail = detail
                    goods.save()
                return redirect('/trade/mine_goods/')
            else:
                if target:
                    data = {'goods': target[0], 'form': ChangeGoods()}
                    return render(req, 'goods_change.html', data)
                else:
                    return raise_wrong(req)
        else:
            data = {'login_no': 'login_no', 'form': UserLog()}
            return render(req, 'login.html', data)


def down_goods(req, gid):
    if not gid.isdigit():
        return raise_wrong(req)
    else:
        username = req.COOKIES.get('is_login')
        if username is not None:
            target = Goods.objects.filter(id=gid)
            if target:
                goods = target[0]
                goods.status = 'off'
                goods.save()
                return redirect('/trade/mine_goods/')
            else:
                return raise_wrong(req)
        else:
            data = {'login_no': 'login_no', 'form': UserLog()}
            return render(req, 'login.html', data)


def up_goods(req, gid):
    if not gid.isdigit():
        return raise_wrong(req)
    else:
        username = req.COOKIES.get('is_login')
        if username is not None:
            target = Goods.objects.filter(id=gid)
            if target:
                goods = target[0]
                goods.status = 'on'
                goods.save()
                return redirect('/trade/mine_goods/')
            else:
                return raise_wrong(req)
        else:
            data = {'login_no': 'login_no', 'form': UserLog()}
            return render(req, 'login.html', data)


def goods_detail(req, gid):
    if not gid.isdigit():
        return raise_wrong(req)
    else:
        username = req.COOKIES.get('is_login')
        if username is not None and User.objects.filter(username__exact=username, status='on'):
            user = User.objects.filter(username__exact=username, status='on')[0]
            target = Goods.objects.filter(id=gid)
            seller = User.objects.filter(id=target[0].seller_id)[0]
            in_wish = list(Wish.objects.filter(user_id=user.id, goods=gid))
            # print(list(in_wish))
            if target:
                goods = target[0]
                data = {'goods': goods, 'user': user, 'seller': seller.username, 'in_wish': in_wish}
                if in_wish:
                    data.update({'in_wish': 'in_wish'})
                return render(req, 'detail_goods.html', data)
            else:
                return raise_wrong(req)
        else:
            data = {'login_no': 'login_no', 'form': UserLog()}
            return render(req, 'login.html', data)


def wish(req, gid):
    if not gid.isdigit():
        return raise_wrong(req)
    else:
        username = req.COOKIES.get('is_login')
        if username is not None and User.objects.filter(username__exact=username, status='on', role='buyer'):
            user = User.objects.filter(username__exact=username, status='on', role='buyer')[0]
            goods = Goods.objects.filter(id=gid)[0]
            Wish.objects.create(user_id=user.id, goods=gid, seller=goods.seller.id, date=datetime.datetime.now())
            return redirect('/trade/goods_detail/{gid}/'.format(gid=gid))
        else:
            data = {'login_no': 'login_no', 'form': UserLog()}
            return render(req, 'login.html', data)


def mine_wish(req):
    username = req.COOKIES.get('is_login')
    if username is not None and User.objects.filter(username__exact=username, status='on', role='buyer'):
        try:
            user = User.objects.filter(username__exact=username, status='on', role='buyer')[0]
            user_id = user.id
        except IndexError:
            return raise_wrong(req)
        data = {'wish_list': []}
        wishes = Wish.objects.filter(user_id=user_id)
        if not list(wishes):
            return render(req, 'mine_wish.html')
        else:
            for wh in wishes:
                goods = Goods.objects.filter(id=wh.goods)[0]
                data['wish_list'].append((goods, wh.date))
            return render(req, 'mine_wish.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def order(req, gid):
    if not gid.isdigit():
        return raise_wrong(req)
    else:
        username = req.COOKIES.get('is_login')
        if username is not None and User.objects.filter(username__exact=username, status='on', role='buyer'):
            if req.method == 'GET':
                try:
                    goods = Goods.objects.filter(id=gid, status='on')[0]
                except IndexError:
                    return raise_wrong(req)
                return render(req, 'confirm_order.html',
                              {'goods': goods, 'form': OrderGoods(), 'seller': goods.seller.username})
            else:
                uf = OrderGoods(req.POST)
                goods = Goods.objects.filter(id=gid, status='on')[0]
                buyer = User.objects.filter(username__exact=username, status='on', role='buyer')[0]
                data = {'goods': goods, 'form': OrderGoods()}
                if uf.is_valid():
                    number = int(uf.cleaned_data['number'])
                    # print(number, type(number))
                    if number > 0:
                        if number > goods.amount:
                            data.update({'too_larger': 'too_larger'})
                            return render(req, 'confirm_order.html', data)
                        else:
                            if buyer.money < (goods.price * number):
                                data.update({'money_not_enough': 'money_not_enough'})
                                return render(req, 'confirm_order.html', data)
                            else:
                                seller = User.objects.filter(id=goods.seller.id, role='seller')[0]
                                if seller.status == 'off':
                                    data.update({'seller_off': 'seller_off'})
                                    return render(req, 'confirm_order.html', data)
                                else:
                                    Order.objects.create(goods=goods.id, title=goods.title, seller=seller.id,
                                                         buyer=buyer.id, date=datetime.datetime.now(), amount=number,
                                                         price=goods.price, status='not_deal')
                                    buyer.money -= goods.price * number
                                    buyer.save()
                                    return redirect('/trade/mine_order/')
                    else:
                        data.update({'wrong': 'wrong'})
                        return render(req, 'confirm_order.html', data)
                else:
                    data.update({'wrong': 'wrong'})
                    return render(req, 'confirm_order.html', data)
        else:
            data = {'login_no': 'login_no', 'form': UserLog()}
            return render(req, 'login.html', data)


def mine_order(req):
    username = req.COOKIES.get('is_login')
    if username is not None and User.objects.filter(username__exact=username, status='on'):
        user = User.objects.filter(username__exact=username, status='on')[0]
        if user.role == 'buyer':
            try:
                buyer = User.objects.filter(username__exact=username, status='on', role='buyer')[0]
            except IndexError:
                return raise_wrong(req)
            data = {'order_list': [], 'buyer_role': 'buyer_role'}
            orders = Order.objects.filter(buyer=buyer.id)
            if not list(orders):
                return render(req, 'mine_order.html')
            else:
                for od in orders:
                    goods = Goods.objects.filter(id=od.goods)[0]
                    data['order_list'].append((goods, od))
                return render(req, 'mine_order.html', data)
        else:
            try:
                seller = User.objects.filter(username__exact=username, status='on', role='seller')[0]
            except IndexError:
                return raise_wrong(req)
            data = {'order_list': [], 'seller_role': 'seller_role'}
            orders = Order.objects.filter(seller=seller.id)
            if not list(orders):
                return render(req, 'mine_order.html')
            else:
                for od in orders:
                    goods = Goods.objects.filter(id=od.goods)[0]
                    data['order_list'].append((goods, od))
                return render(req, 'mine_order.html', data)
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)


def deal_order(req, oid):
    username = req.COOKIES.get('is_login')
    if username is not None and User.objects.filter(username__exact=username, status='on'):
        user = User.objects.filter(username__exact=username, status='on')[0]
        if user.role == 'buyer':
            try:
                od = Order.objects.filter(id=oid)[0]
                seller = User.objects.filter(id=od.seller, status='on', role='seller')[0]
                goods = Goods.objects.filter(id=od.goods)[0]
            except IndexError:
                return raise_wrong(req)
            od.status = 'off'
            od.save()
            goods.amount -= od.amount
            goods.save()
            seller.money += float(od.amount * od.price)
            return redirect('/trade/mine_order/')
        else:
            try:
                od = Order.objects.filter(id=oid)[0]
            except IndexError:
                return raise_wrong(req)
            od.status = 'on'
            od.save()
            return redirect('/trade/mine_order/')
    else:
        data = {'login_no': 'login_no', 'form': UserLog()}
        return render(req, 'login.html', data)
