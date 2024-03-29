from django.contrib import admin

from sellers.models import (
    Balance,
    CarShowRoom,
    Dealer,
    DealerCar,
    Discount,
    DiscountCar,
    ShowroomCar,
)

admin.site.register(Balance)
admin.site.register(CarShowRoom)
admin.site.register(Discount)
admin.site.register(Dealer)
admin.site.register(ShowroomCar)
admin.site.register(DealerCar)
admin.site.register(DiscountCar)
