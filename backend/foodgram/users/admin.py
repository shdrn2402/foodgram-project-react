from django.contrib import admin
from users import models


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username",)
    list_filter = ("email", "username",)
    empty_value_display = "-пусто-",


admin.site.register(models.Follow)
admin.site.unregister(models.User)
admin.site.register(models.User, UserAdmin)
