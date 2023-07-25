from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token


@csrf_exempt
def app_product(request, user_id, productid):
    access_for_contact_no = False
    limit_over_pop_up = False
    token = request.POST.get("token")
    requestmobileno = request.POST.get("user_mobileno")
    print("requestmobileno : ", requestmobileno)
    print("token : ", token)
    # try:
    if token and requestmobileno:
        try:
            getdatafromdb = users_credentials_app_token.objects.get(
                user_mobile_num=requestmobileno
            )
            print("user_iddddd : ", getdatafromdb.user_id.id)

        except:
            return HttpResponse("User not found")

        print("data from db : ", getdatafromdb.user_token)
        if str(token) == str(getdatafromdb.user_token) and str(user_id) == str(
            getdatafromdb.user_id.id
        ):
            current_user_details = users.objects.get(id=user_id)
            print("current_user_details : ", current_user_details)
            # below code will give owner account-id
            try:
                property_owner_email = (
                    property_details.objects.get(id=productid)
                ).user_emailid_via_login_token
            except:
                return HttpResponse("Product not found")
            user_id_request_for_view_contact_no = property_owner_email
            unlocked_contact_no_details = [
                x[0]
                for x in user_free_limits.objects.filter(
                    user_id=current_user_details.id
                )
                .values_list("unlocked_contact_no_for_product_id_is")
                .distinct()
            ]
            print("unlocked_contact_no_details", unlocked_contact_no_details)
            updating_request_count = users.objects.get(id=current_user_details.id)

            # CHeck for all unlocked product-id for the user
            if productid in unlocked_contact_no_details:
                access_for_contact_no = True
            else:
                access_for_contact_no = False

            # if user_id_request_for_view_contact_no:
            #     print(" User Account ID : ", current_user_details.id)
            #     print("db email : ", updating_request_count)
            #     if (
            #         str(updating_request_count.mobile_no) == str(requestmobileno)
            #         and updating_request_count.no_of_requests_to_view_contact_no <= 200
            #     ):
            #         update_user_free_limit_table = user_free_limits.objects.create(
            #             user_id=updating_request_count,
            #             product_id=property_details.objects.get(id=productid),
            #             unlocked_contact_no_for_product_id_is=productid,
            #             unlocked_at=timezone.now(),
            #         )
            #         update_user_free_limit_table.save()
            #         print(
            #             "Before user_request_count : ",
            #             updating_request_count.no_of_requests_to_view_contact_no,
            #         )

            #         updating_request_count.no_of_requests_to_view_contact_no = (
            #             updating_request_count.no_of_requests_to_view_contact_no + 1
            #         )
            #         print(
            #             "After user_request_count : ",
            #             updating_request_count.no_of_requests_to_view_contact_no,
            #         )
            #         updating_request_count.save()
            #         access_for_contact_no = True

            # # Updating send_text_to_owners table
            # property_owner = users.objects.get(
            #     email_id=user_id_request_for_view_contact_no
            # )

            # send_text_to_owners = send_text_to_owner.objects.create(
            #     request_user_id=current_user_details.id,
            #     receiver_user_id=users.objects.get(
            #         email_id=property_owner_email
            #     ),
            #     request_property_id=productid,
            #     request_user_mobile_no=current_user_details.mobile_no,
            #     request_user_email_id=current_user_details.email_id,
            #     request_user_time=timezone.now(),
            # )
            # send_text_to_owners.save()
            # try:
            # #sending text on mail as well
            #     product_id= property_details.objects.get(id=productID)
            #     send_to_mail= send_mail("Hey, Looking For Your Property !! ",f"Hello {property_owner.last_name},\ni'm {current_user_details.last_name}, I hope you are having a good week. \nI'm getting in touch to request a viewing of the property at {product_id.property_city}. please reach me out on this number '{current_user_details.mobile_no}' \nThank You. ",settings.EMAIL_HOST_USER,[current_user_details.email_id])

            #     print("Mail Has Been Sent")
            # except:
            #     pass

            # else:
            #     access_for_contact_no = False
            #     limit_over_pop_up = True

            (
                product_imgs,
                fetching_the_product_details,
                fetching_price_and_user_address,
            ) = fetching_img_property_details(productid)
            fetching_price_and_user_address = property_details.objects.filter(
                id=productid
            ).values(
                "monthly_rent",
                "property_city",
                "property_state",
                # "created_at",
                "id",
            )
            # fetching user info to show on product page
            fetching_owner_email_through_product_id = property_details.objects.filter(
                id=productid
            ).values("user_emailid_via_login_token")
            print("Product Owner Details : ", fetching_owner_email_through_product_id)
            fetching_all_user_data = users.objects.filter(
                email_id=fetching_owner_email_through_product_id[0][
                    "user_emailid_via_login_token"
                ]
            ).values(
                "id",
                "first_name",
                "last_name",
                "mobile_no",
                "user_profile_pic",
                # "created_at",
            )[
                :1
            ]
            fetch_house_appliances = [
                x
                for x in property_details.objects.filter(id=productid).values(
                    "appliance_TV",
                    "appliance_Fridge",
                    "appliance_sofa",
                    "appliance_bed",
                    "appliance_dresser",
                    "appliance_AC",
                    "appliance_washing_machine",
                    "appliance_water_heaters",
                    "appliance_fans",
                    "appliance_water_purifier",
                    "appliance_tubelights",
                    "appliance_Inventers",
                )
            ]
            # print()
            # print("fetching_the_product_details : ", fetching_the_product_details)
            # print("fetch_house_appliances : ", fetch_house_appliances)
            # print("product_imgs : ", product_imgs)
            # print("fetching_price_and_user_address : ", fetching_price_and_user_address[0])
            # print("fetching_all_user_data : ", fetching_all_user_data[0])
            # print("access_for_contact_no : ", access_for_contact_no)
            data = {
                "token verified": True,
                "property_data": fetching_the_product_details[0],
                "property_house_appliance": fetch_house_appliances,
                "property_img": product_imgs,
                "fetching_price_and_user_details": fetching_price_and_user_address[0],
                "user_data": fetching_all_user_data[0],
                "access_for_contact_no": access_for_contact_no,
                "limit_over_pop_up": limit_over_pop_up,
            }
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse("Unauthorized")

    else:
        return HttpResponse("Unauthorized")

    # except:
    #     data = {"User not Found": True}
    #     return HttpResponse(json.dumps(data))
