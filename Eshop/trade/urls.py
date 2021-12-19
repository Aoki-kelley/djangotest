from django.urls import path

from . import views

urlpatterns = [
    path('mine_goods/', views.mine_goods, name='mine_goods'),
    path('goods_create/', views.goods_create, name='goods_create'),
    path('change/', views.raise_wrong, name='goods_change_wrong'),
    path('change/<gid>/', views.change_goods, name='goods_change'),
    path('down/', views.raise_wrong, name='down_goods_wrong'),
    path('down/<gid>/', views.down_goods, name='down_goods'),
    path('up/', views.raise_wrong, name='up_goods_wrong'),
    path('up/<gid>/', views.up_goods, name='up_goods'),
    path('goods_detail/', views.raise_wrong, name='goods_detail_wrong'),
    path('goods_detail/<gid>/', views.goods_detail, name='goods_detail'),
    path('wish/', views.raise_wrong, name='wish_wrong'),
    path('wish/<gid>/', views.wish, name='wish'),
    path('mine_wish/', views.mine_wish, name='mine_wish'),
    path('order/', views.raise_wrong, name='order_wrong'),
    path('order/<gid>/', views.order, name='order'),
    path('mine_order/', views.mine_order, name='mine_order'),
    path('deal_order/', views.raise_wrong, name='deal_order_wrong'),
    path('deal_order/<oid>&<action>/', views.deal_order, name='deal_order'),
    path('search/', views.search, name='search')
]
