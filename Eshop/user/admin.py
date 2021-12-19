from django.contrib import admin
from user.models import *
from trade.models import *


# Register your models here.
# admin.site.register([User, Goods, ])


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'status', 'email_proved')
    list_editable = ['status']
    list_filter = ['role', 'status']

    def to_off(self, request, queryset):
        queryset.update(status='off')

    def to_on(self, request, queryset):
        queryset.update(status='on')

    to_off.short_description = '冻结用户'
    to_on.short_description = '取消冻结'
    actions = [to_off, to_on]


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ('title', 'label', 'date', 'status')
    list_editable = ['status']
    list_filter = ['label', 'date', 'status']

    def to_off(self, request, queryset):
        queryset.update(status='off')

    def to_on(self, request, queryset):
        queryset.update(status='on')

    to_off.short_description = '下架商品'
    to_on.short_description = '上架商品'
    actions = [to_off, to_on]

# admin.site.register([UserAdmin])
