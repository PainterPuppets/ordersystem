from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']



class DishAdmin(admin.ModelAdmin):
    list_display = ['dishname', 'fprice', 'sales', 'isHot']
    ordering =  ['-sales']
    search_fields = ['dishname']
    def isHot(self, Dish):
        return Dish.sales > 100
    isHot.short_description = 'hot'
    isHot.boolean = True


admin.site.register(User, UserAdmin)
admin.site.register(Dish, DishAdmin)
