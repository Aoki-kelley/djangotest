from django import forms

from trade.models import Goods

choices = [(1, '小说'), (2, '文学'), (3, '艺术'), (4, '动漫/幽默'), (5, '娱乐时尚'),
           (6, '旅游'), (7, '地图/地理'), (8, '科学技术')]


class CreateGoods(forms.ModelForm):
    # image = forms.fields.ImageField(required=True)
    # title = forms.fields.CharField(required=True, max_length=16)
    # detail = forms.fields.CharField(widget=forms.Textarea, required=True)
    label = forms.fields.ChoiceField(required=True, choices=choices)

    # price = forms.fields.FloatField(required=True)
    # amount = forms.fields.IntegerField(required=True)
    class Meta:
        fields = ['image', 'title', 'detail', 'price', 'amount']
        model = Goods


class ChangeGoods(forms.ModelForm):
    price = forms.fields.FloatField(required=False)
    amount = forms.fields.IntegerField(required=False)

    class Meta:
        fields = ['detail']
        model = Goods


class OrderGoods(forms.Form):
    number = forms.fields.IntegerField(required=False)
