from .common_imports import *


def ecomm_sell(request):
    user_emailid_via_login_token = "temp@gmail.com "
    seller_contact_no = "7207371207"

    product_category = request.POST.get("product_category")

    if product_category:
        product_name = request.POST.get("product_name")
        Product_image = request.FILES.get("Product_image")
        GST_NO = request.POST.get("GST_NO")
        product_sub_category = request.POST.get("product_sub_category")
        selling_city = request.POST.get("selling_city")
        selling_state = request.POST.get("selling_state")
        selling_pincode = request.POST.get("selling_pincode")
        selling_price_per_item = request.POST.get("selling_price_per_item")

        actual_price_per_item = request.POST.get("actual_price_per_item")
        ecomm_user_pan_via_gst = request.POST.get("ecomm_user_pan_via_gst")
        ecomm_user_adr_via_gst = request.POST.get("ecomm_user_adr_via_gst")
        discount_percent = request.POST.get("discount_percent")
        selling_city_or_village = request.POST.get("selling_city_or_village")

        brand_name = request.POST.get("brand_name")
        other_value_added = request.POST.get("other_value_added")
        min_items = request.POST.get("min_items")
        retailer_name = request.POST.get("retailer_name")
        other_category_selections = request.POST.get("other_category_selections")

        new_ecomm_data = ecomm_product_details.objects.create(
            user_emailid_via_login_token=user_emailid_via_login_token,
            seller_contact_no=seller_contact_no,
            product_category=product_category,
            product_name=product_name,
            Product_image=Product_image,
            GST_NO=GST_NO,
            product_sub_category=product_sub_category,
            selling_city=selling_city,
            selling_state=selling_state,
            selling_pincode=selling_pincode,
            selling_price_per_item=selling_price_per_item,
            ecomm_user_pan_via_gst=ecomm_user_pan_via_gst,
            ecomm_user_adr_via_gst=ecomm_user_adr_via_gst,
            other_value_added=other_value_added,
            min_items=min_items,
            retailer_name=retailer_name,
            created_at=timezone.now(),
            other_category_selections=other_category_selections,
            brand_name=brand_name,
            actual_price=actual_price_per_item,
            discount_price=discount_percent,
            selling_city_or_village=selling_city_or_village,
        )

        new_ecomm_data.save()

    return render(request, "ecomm_post_ad.html")
