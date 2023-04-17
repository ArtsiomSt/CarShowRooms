from django.contrib import admin

from .models import Car, CarBrand


class CarAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "car_brand")


admin.site.register(Car, CarAdmin)
admin.site.register(CarBrand)
