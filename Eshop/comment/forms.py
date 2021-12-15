from django import forms
from comment.models import *


class LeaveComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']


class LeaveReply(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
