from django.contrib import admin

from .models import ecomm_product_details, ecomm_users, ecomm_users_credentials_IPs


class ecomm_product(admin.ModelAdmin):
    list_display = ["selling_state", "product_category", "selling_pincode"]


class ecomm_credentials(admin.ModelAdmin):
    list_display = ["user_ip_address", "user_token", "createdAt"]


# Register your models here.

admin.site.register(ecomm_product_details, ecomm_product)
admin.site.register(ecomm_users)
admin.site.register(ecomm_users_credentials_IPs, ecomm_credentials)
