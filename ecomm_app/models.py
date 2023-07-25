from django.db import models
from datetime import timedelta
from django.utils import timezone


# Create your models here.


class ecomm_users(models.Model):
    first_name = models.CharField(max_length=30, default=None)
    last_name = models.CharField(max_length=30)
    email_id = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=12)
    Bio = models.CharField(max_length=200, default="Never Loose Hope !!")
    user_profile_pic = models.ImageField(upload_to="")
    user_password = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now(), null=True)
    no_of_requests_to_view_contact_no = models.IntegerField(default=0)
    no_of_free_ad_posted_count = models.IntegerField(default=0)
    no_of_paid_ad_posted_count = models.IntegerField(default=0)
    user_ad_posting_enrolled = models.BooleanField(default=False)
    user_ad_posting_enrolled_limit = models.IntegerField(default=0)
    user_ad_posting_enrolled_limit_expired_date = models.DateField(null=True)
    user_view_contact_enrolled = models.BooleanField(default=False)
    user_state_by_geo_loc = models.CharField(max_length=100, default="null")
    role = models.CharField(max_length=50, default="user")
    user_added_by_admin = models.CharField(max_length=100, default=None, null=True)

    is_user_updated_from_rental_app = models.BooleanField(default=False)

    user_last_log_location = models.TextField(max_length=100, default=None, null=True)
    user_last_log_location_district = models.TextField(
        max_length=100, default=None, null=True
    )

    user_last_log_coordinates = models.TextField(
        max_length=100, default=None, null=True
    )

    def __str__(self):
        return self.first_name


class ecomm_users_credentials_IPs(models.Model):
    user_id = models.ForeignKey(
        ecomm_users, on_delete=models.CASCADE, default=0, null=True
    )
    user_email_id = models.CharField(max_length=50, null=True)
    user_ip_address = models.CharField(max_length=100, default=None, null=True)
    user_token = models.CharField(max_length=100, null=True)
    createdAt = models.DateTimeField(default=timezone.now())
    user_state_by_geo_loc = models.CharField(max_length=100, default="null", null=True)
    user_current_locality = models.CharField(max_length=100, default="null", null=True)
    user_district = models.CharField(max_length=100, default="null", null=True)
    user_loc_coordinates = models.CharField(max_length=100, default="null", null=True)

    def __str__(self):
        return self.user_email_id


# class user_free_limits(models.Model):
#     user_id = models.ForeignKey(users, on_delete=models.CASCADE)
#     product_id = models.ForeignKey(property_details, on_delete=models.CASCADE)
#     unlocked_contact_no_for_product_id_is = models.IntegerField(default=0)
#     unlocked_at = models.DateTimeField(default=timezone.now(), null=True)


# class ad_posted_logs(models.Model):
#     user_details = models.ForeignKey(users, on_delete=models.CASCADE)
#     user_posted_ad_property_id = models.IntegerField(default=0)
#     user_posted_date = models.DateField(default=timezone.now(), null=True)

#     def __str__(self):
#         return self.user_details.email_id


class ecomm_product_details(models.Model):
    user_emailid_via_login_token = models.CharField(
        max_length=100, default=None, null=True
    )
    product_category = models.CharField(max_length=200, default=None, null=True)
    product_name = models.CharField(max_length=200)
    Product_image = models.ImageField(upload_to="", default=None, null=True)
    GST_NO = models.CharField(max_length=20, default=None, null=True)
    product_sub_category = models.CharField(max_length=100, default=None, null=True)

    selling_city = models.CharField(max_length=30, default=None, null=True)
    selling_state = models.CharField(max_length=30, default=None, null=True)
    selling_pincode = models.CharField(max_length=6, default=None, null=True)
    selling_price_per_item = models.IntegerField(default=None, null=True)
    seller_contact_no = models.IntegerField(max_length=20, default=None, null=True)

    ecomm_user_pan_via_gst = models.CharField(max_length=20, default=None, null=True)
    ecomm_user_adr_via_gst = models.TextField(max_length=100, default=None, null=True)

    brand_name = models.CharField(max_length=100, default=None, null=True)

    discount_price = models.IntegerField(default=None, null=True)
    actual_price = models.IntegerField(default=None, null=True)
    selling_city_or_village = models.CharField(max_length=100, default=None, null=True)

    other_value_added = models.CharField(max_length=100, default=None, null=True)
    other_category_selections = models.CharField(
        max_length=100, default=None, null=True
    )

    min_items = models.IntegerField(default=None, null=True)
    retailer_name = models.CharField(max_length=100, default=None, null=True)

    created_at = models.DateTimeField(default=timezone.now(), null=True)
    post_expire_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))
    ad_posted_by = models.CharField(max_length=50, default="user")

    def __str__(self):
        return self.user_emailid_via_login_token
