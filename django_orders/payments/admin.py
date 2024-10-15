from django.contrib import admin

from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=...):
        return False

    def has_delete_permission(self, request, obj=...):
        return False


admin.site.register(Payment, PaymentAdmin)
