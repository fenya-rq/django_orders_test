from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Order
from services import OrderAdminRequest


class OrderAdmin(admin.ModelAdmin):
    """
    Admin class for managing Orders in the admin interface.
    Adds custom behavior for handling order confirmations.
    """

    readonly_fields = (
        "total_cost",
        "status",
        "create_dt",
        "confirm_dt",
        "custom_button",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        """
        Adds custom URLs to handle button actions for approving orders.
        Returns the modified URL list, adding a custom URL for approval.
        """
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:order_id>/approve/",
                self.admin_site.admin_view(self.custom_action_view),
                name="approve",
            ),
        ]
        return custom_urls + urls

    def custom_button(self, obj):
        """
        Renders a custom button for confirming orders if the order status
        is 'Оплачен'. The button redirects to the approval action view.
        """
        if obj.status != "Оплачен":
            return ""
        url = reverse("admin:approve", args=[obj.id])
        return format_html('<a class="button" href="{}">Подтвердить заказ</a>', url)

    custom_button.short_description = "Подтверждение"
    custom_button.allow_tags = True

    def custom_action_view(self, request, order_id):
        """
        Handles the approval action for a specific order, updating its
        status and sending data to an external service. Displays a success
        or warning message based on the outcome.
        """
        order = Order.objects.get(pk=order_id)
        order.update_confirm_date()
        order.update_confirmation_status()
        external_request = self.request_to_external(order)
        if external_request:
            self.message_user(request, f"Заказ № {order_id} подтвержден")
        else:
            self.message_user(
                request,
                f"Возникла проблема с отправкой данных Заказа № {order_id} клиенту.",
                level=messages.WARNING,
            )
        return redirect(request.META.get("HTTP_REFERER"))

    @staticmethod
    def request_to_external(order) -> bool:
        """
        Sends a request with order data to an external service. Returns
        True if successful, otherwise returns False.
        """
        return OrderAdminRequest(order).send_request()


admin.site.register(Order, OrderAdmin)
