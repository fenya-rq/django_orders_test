from django.contrib import admin

from .models import Order, OrderStatus


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ("total_cost", "status", "create_dt", "confirm_dt")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderStatusAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
