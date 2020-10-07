from django.contrib import admin
from . models import Owner


class OwnerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Owner, OwnerAdmin)
