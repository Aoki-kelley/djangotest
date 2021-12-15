from django.urls import path

from . import views

urlpatterns = [
    path('leave_comment/', views.raise_wrong, name='leave_comment_wrong'),
    path('leave_comment/<gid>/', views.leave_comment, name='leave_comment'),
    path('reply_comment/', views.raise_wrong, name='reply_comment_wrong'),
    path('reply_comment/<cid>/', views.reply_comment, name='reply_comment'),
    path('reply_reply/', views.raise_wrong, name='reply_reply_wrong'),
    path('reply_reply/<rid>/', views.reply_reply, name='reply_reply'),
    path('comment_detail/', views.raise_wrong, name='comment_Detail_wrong'),
    path('comment_detail/<cid>/', views.comment_detail, name='comment_detail'),
    path('mine_comment_reply/', views.mine_comment_reply, name='mine_comment_reply'),
    path('delete/', views.raise_wrong, name='delete_wrong'),
    path('delete/<style>&<cr_id>/', views.delete, name='delete'),
]
