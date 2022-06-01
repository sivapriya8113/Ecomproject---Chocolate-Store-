'''from django.contrib import admin

# Register your models here.
from .models import Chocolates, Category

admin.site.register(Chocolates)
admin.site.register(Category)

'''

from django.contrib import admin

from . import models


class AdminInfo(admin.ModelAdmin):
    model = models.Chocolates
    actions = ['delete_model']

    def delete_queryset(self, request, queryset):
        print('========================delete_queryset========================')

        print(queryset)
        for obj in queryset:
            obj.is_deleted=True
            obj.save()
admin.site.register(models.Chocolates, AdminInfo)
