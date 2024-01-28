from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Food)
admin.site.register(models.Review)
admin.site.register(models.Category)
admin.site.register(models.FoodWishList)
admin.site.register(models.FoodCardList)
admin.site.register(models.HistoryList)
