from .common_imports import *
from rental_app.views.common_imports import *
import urllib

from django.views.decorators.csrf import csrf_exempt


def getIP(request):
    try:
        x_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_for is not None:
            ip = x_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    except urllib.error.HTTPError as err:
        print(f"A HTTPError was thrown: {err.code} {err.reason}")
        pass


def homepage(request):
    client_ip_address = getIP(request)
    user_not_match = False
    user_already_exist = False
    is_user_logged_in = False
    print("client_ip_address : ", client_ip_address)
    user_otp_token = request.COOKIES.get("otp_token")
    user_email_id = request.COOKIES.get("email_id")
    user_current_locality = request.GET.get("user_current_location")
    user_district = request.GET.get("user_current_location_district")
    user_state = request.GET.get("user_current_state_via_coordinates")
    coordinates = request.GET.get("user_current_coordinates")

    print()
    print()
    print()
    print()
    print("user_current_locality : ", user_district)

    if user_otp_token:
        print("browser_token : ", user_otp_token)

        validate1 = token_validations(user_otp_token, request, "ecomm_app")

        print("is token_match_via ecomm app cred : ", validate1)

        if validate1:
            is_user_logged_in = True

        elif (
            not validate1
        ):  # The below logic is to check if user logined via rental_app and check for token in rental_app credentials
            validate2 = token_validations(user_otp_token, request, "rental_app")
            print("is token_match_via rental app cred : ", validate1)

            if validate2:
                is_user_logged_in = True

    if user_email_id:
        try:
            check_user_exist_on_ecomm_app = ecomm_users.objects.get(
                email_id=user_email_id
            )
        except Exception as temp:
            take_all_user_info_from_rental_app = users.objects.get(
                email_id=user_email_id
            )
            if take_all_user_info_from_rental_app:
                create_user = ecomm_users.objects.create(
                    first_name=take_all_user_info_from_rental_app.first_name,
                    last_name=take_all_user_info_from_rental_app.last_name,
                    email_id=take_all_user_info_from_rental_app.email_id,
                    mobile_no=take_all_user_info_from_rental_app.mobile_no,
                    Bio=take_all_user_info_from_rental_app.Bio,
                    user_profile_pic=take_all_user_info_from_rental_app.user_profile_pic,
                    user_password=take_all_user_info_from_rental_app.user_password,
                    created_at=take_all_user_info_from_rental_app.created_at,
                    no_of_requests_to_view_contact_no=take_all_user_info_from_rental_app.no_of_requests_to_view_contact_no,
                    no_of_free_ad_posted_count=take_all_user_info_from_rental_app.no_of_free_ad_posted_count,
                    no_of_paid_ad_posted_count=take_all_user_info_from_rental_app.no_of_paid_ad_posted_count,
                    user_ad_posting_enrolled=take_all_user_info_from_rental_app.user_ad_posting_enrolled,
                    user_ad_posting_enrolled_limit=take_all_user_info_from_rental_app.user_ad_posting_enrolled_limit,
                    user_ad_posting_enrolled_limit_expired_date=take_all_user_info_from_rental_app.user_ad_posting_enrolled_limit_expired_date,
                    user_view_contact_enrolled=take_all_user_info_from_rental_app.user_view_contact_enrolled,
                    user_state_by_geo_loc=take_all_user_info_from_rental_app.user_state_by_geo_loc,
                    role=take_all_user_info_from_rental_app.role,
                    user_added_by_admin=take_all_user_info_from_rental_app.user_added_by_admin,
                    is_user_updated_from_rental_app=True,
                )

                create_user.save()
        except:
            return HttpResponseBadRequest()

    # update_brand_name = ecomm_product_details.objects.filter(
    #     product_category="Constructions"
    # ).update(brand_name="zuari")

    # Login_From DAta

    user_email = request.POST.get("login_email_id")

    if user_email:
        password = request.POST.get("login_email_password")

        print("user email : ", user_email)

        print("user password : ", password)

        # Checking User Credentials
        try:
            user_details = ecomm_users.objects.get(email_id=user_email)

            print("user_details : ", user_details)

        except:
            data = {"user_not_match": True}

            return render(request, "index.html", data)

        check_email = ecomm_users.objects.filter(email_id=user_email).values(
            "email_id", "user_password"
        )

        print(check_email)

        if check_email and str(password) == str(check_email[0]["user_password"]):
            print("User Login success")

            ## Taking users ip address and passing a token ND BOTH TOKEN nd IP address are stored in db

            gen_token = token_gen()

            new_user_credentials = ecomm_users_credentials_IPs.objects.create(
                user_id=user_details,
                user_email_id=user_email,
                user_ip_address=client_ip_address,
                user_token=gen_token,
                createdAt=timezone.now(),
                user_state_by_geo_loc=user_state,
                user_loc_coordinates=coordinates,
                user_district=user_district,
                user_current_locality=user_current_locality,
            )

            new_user_credentials.save()

            response = HttpResponseRedirect("/ecomm")

            # removing the secure in cookies due to check that cookie existing on header.html for sell btn

            response.set_cookie("otp_token", gen_token, max_age=84600)

            response.set_cookie("email_id", user_email, max_age=84600)

            # response.set_cookie('email_id',user_email,secure=True,httponly=True,max_age=84600)

            return response

        else:
            data = {"user_not_match": True}

            return render(request, "index.html", data)

    # SignUp Form Integrations

    email = request.POST.get("email_id")

    mobile_no = request.POST.get("mobile_no")

    Is_Exist = mobile_no_r_email_existance(email, mobile_no)

    print("User_Exists : ", Is_Exist)

    if email:
        if Is_Exist == False:
            print()

            print()

            print()

            print()

            first_name = request.POST.get("first_name")

            last_name = request.POST.get("last_name")

            # email_id=request.POST.get('email_id')

            # mobile_no=request.POST.get('mobile_no')

            password = request.POST.get("login_email_password")

            # Bio=request.POST['Bio']

            new_data = users(
                first_name=first_name,
                last_name=last_name,
                email_id=email,
                mobile_no=mobile_no,
                user_password=password,
                # Bio=Bio,
                created_at=timezone.now(),
                user_state_by_geo_loc=user_state,
            )

            new_data.save()

            print()

            print()

            print("signup success for : ", email)

            # after signup user should be logined_state

            ## Taking users ip address and passing a token ND BOTH TOKEN nd IP address are stored in db

            gen_token = token_gen()

            new_user_credentials = users_credentials_IPs.objects.create(
                user_id=new_data,
                user_email_id=new_data.email_id,
                user_ip_address=client_ip_address,
                user_token=gen_token,
                createdAt=timezone.now(),
                user_state_by_geo_loc=user_state,
                user_loc_coordinates=coordinates,
                user_district=user_district,
                user_current_locality=user_current_locality,
            )

            new_user_credentials.save()

            response = HttpResponseRedirect("/ecomm")

            # removing the secure in cookies due to check that cookie existing on header.html for sell btn

            response.set_cookie("otp_token", gen_token, max_age=84600)

            response.set_cookie(
                "email_id",
                new_data.email_id,
                max_age=84600,
            )

            return response

        else:
            data = {"user_already_exist": True}

            return render(request, "ecomm_homepage.html", data)

    # randam_name = ["Murukambattu", "Chittoor", "Tirupathi"]

    # instant_update = ecomm_product_details.objects.filter(product_category="Fashion")
    # instant_update.update(selling_city=random.choice(randam_name))
    local_cities = False
    local_cities_filter = request.POST.get("local_cities")

    print()
    print()
    print()
    print()
    print()
    print()
    print()
    print("local_cities_filter : ", local_cities_filter)

    if local_cities_filter:
        local_cities = local_cities_filter.split(",")
        print("local_cities : ", local_cities)
        # user_current_locality = request.POST.get("user_current_location")
        # user_district = request.POST.get("user_current_location_district")
        try:
            update_user_with_loc = ecomm_users.objects.get(email_id=user_email_id)
            update_user_with_loc.user_last_log_location = user_current_locality
            update_user_with_loc.user_last_log_coordinates = coordinates
            update_user_with_loc.user_last_log_location_district = user_district
            update_user_with_loc.save()
        except:
            pass

    get_home_category_data = get_ecomm_product_data(
        "Home Appliances", local_cities, user_state, is_user_logged_in
    )

    get_fasion_category_data = get_ecomm_product_data(
        "Fashion", local_cities, user_state, is_user_logged_in
    )

    get_electical_category_data = get_ecomm_product_data(
        "Electricals", local_cities, user_state, is_user_logged_in
    )

    get_electronic_category_data = get_ecomm_product_data(
        "Electrioncs", local_cities, user_state, is_user_logged_in
    )

    get_medical_category_data = get_ecomm_product_data(
        "Medical Equipments", local_cities, user_state, is_user_logged_in
    )

    get_construction_category_data = get_ecomm_product_data(
        "Constructions", local_cities, user_state, is_user_logged_in
    )

    get_automotive_category_data = get_ecomm_product_data(
        "AutoMotive", local_cities, user_state, is_user_logged_in
    )

    get_Other_category_data = get_ecomm_product_data(
        "Others", local_cities, user_state, is_user_logged_in
    )

    print(" get_construction_category_data : ", get_construction_category_data)

    print("user_district : ", user_district)

    print("user_state : ", user_state)

    print("is_user_logged_in : ", is_user_logged_in)

    data = {
        "home_category": get_home_category_data,
        "fasion_category": get_fasion_category_data,
        "electical_category": get_electical_category_data,
        "electronic_category": get_electronic_category_data,
        "medical_category": get_medical_category_data,
        "construction_category": get_construction_category_data,
        "automotive_category": get_automotive_category_data,
        "Other_category": get_Other_category_data,
        "user_current_loc": user_current_locality
        if user_current_locality != "undefined"
        else False,
        "user_district": user_district if user_district != "undefined" else False,
        "user_status": is_user_logged_in,
        "user_state": user_state,
    }

    print(f"user email : {user_email_id} and \nUser Token is : {user_otp_token}")
    return render(request, "ecomm_homepage.html", data)


# ======================= Common Functions =======================================


@csrf_exempt
def homepg_for_api(request):
    user_current_locality = request.POST.get("user_current_location")
    user_district = request.POST.get("user_current_location_district")
    user_state = request.POST.get("user_current_state_via_coordintes")
    coordinates = request.POST.get("user_current_coordinates")

    user_status = request.POST.get("user_status")  # Show User is Logined in or not

    local_cities = False
    local_cities_filter = request.POST.get("local_cities")

    if user_state is not "None":
        local_cities = local_cities_filter.split(",")
        print("local_cities : ", local_cities)
        # user_current_locality = request.POST.get("user_current_location")
        # user_district = request.POST.get("user_current_location_district")
        try:
            update_user_with_loc = ecomm_users.objects.get(email_id=user_email_id)
            update_user_with_loc.user_last_log_location = user_current_locality
            update_user_with_loc.user_last_log_coordinates = coordinates
            update_user_with_loc.user_last_log_location_district = user_district
            update_user_with_loc.save()
        except:
            pass

        get_home_category_data = get_ecomm_product_data(
            "Home Appliances", local_cities, user_state, user_status
        )

        get_fasion_category_data = get_ecomm_product_data(
            "Fashion", local_cities, user_state, user_status
        )

        get_electical_category_data = get_ecomm_product_data(
            "Electricals", local_cities, user_state, user_status
        )

        get_electronic_category_data = get_ecomm_product_data(
            "Electrioncs", local_cities, user_state, user_status
        )

        get_medical_category_data = get_ecomm_product_data(
            "Medical Equipments", local_cities, user_state, user_status
        )

        get_construction_category_data = get_ecomm_product_data(
            "Constructions", local_cities, user_state, user_status
        )

        get_automotive_category_data = get_ecomm_product_data(
            "AutoMotive", local_cities, user_state, user_status
        )

        get_Other_category_data = get_ecomm_product_data(
            "Others", local_cities, user_state, user_status
        )

        # print(" get_construction_category_data : ", get_construction_category_data)

        # print("user_district : ", user_district)

        # print("user_state : ", user_state)

        # print()
        # print()
        # print()
        # print(" coordinates : ", coordinates)
        # print("user_current_locality : ", user_district)
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print("local_cities_filter : ", local_cities_filter)
        print("user_status : ", user_status)
        data = {
            "home_category": get_home_category_data,
            "fasion_category": get_fasion_category_data,
            "electical_category": get_electical_category_data,
            "electronic_category": get_electronic_category_data,
            "medical_category": get_medical_category_data,
            "construction_category": get_construction_category_data,
            "automotive_category": get_automotive_category_data,
            "Other_category": get_Other_category_data,
            "user_current_loc": user_current_locality
            if user_current_locality != "undefined"
            else False,
            "user_district": user_district if user_district != "undefined" else False,
            "user_state": user_state,
        }
        return HttpResponse(json.dumps(data))
    return HttpResponse("Status oK")


def get_ecomm_product_data(pt_category, local_cities, user_state, user_status):
    final_filtered_data = []

    if local_cities:
        print("searching by local cities")
        for x in set(local_cities):
            # print("x : ", x)
            store_reference = (
                (
                    ecomm_product_details.objects.filter(
                        product_category=pt_category
                    ).values(
                        "selling_price_per_item",
                        "selling_state",
                        "selling_city",
                        "retailer_name",
                        "min_items",
                        "product_name",
                        "Product_image",
                        "ecomm_user_adr_via_gst",
                        "selling_pincode",
                        "seller_contact_no",
                        "discount_price",
                        "actual_price",
                        "product_sub_category",
                        "brand_name",
                    )
                )
                .filter(selling_city=str(x))
                .order_by("-id")[:20]
            )

            if store_reference:
                print("store_reference : ", store_reference)
                for x in store_reference:
                    final_filtered_data.append(x)

    if final_filtered_data == []:
        print("searching by user state")

        # print("x : ", x)
        store_reference = (
            (
                ecomm_product_details.objects.filter(
                    product_category=pt_category
                ).values(
                    "selling_price_per_item",
                    "selling_state",
                    "selling_city",
                    "retailer_name",
                    "min_items",
                    "product_name",
                    "Product_image",
                    "ecomm_user_adr_via_gst",
                    "selling_pincode",
                    "seller_contact_no",
                    "discount_price",
                    "actual_price",
                    "product_sub_category",
                    "brand_name",
                )
            )
            .filter(selling_state=str(user_state))
            .order_by("-id")[:20]
        )

        if store_reference:
            print("Yes store_ref true")
            for x in store_reference:
                final_filtered_data.append(x)

    if final_filtered_data == []:
        print("searching all data")
        final_data = []
        store_reference = (
            ecomm_product_details.objects.filter(product_category=pt_category)
            .values(
                "selling_price_per_item",
                "selling_state",
                "selling_city",
                "retailer_name",
                "min_items",
                "product_name",
                "Product_image",
                "ecomm_user_adr_via_gst",
                "selling_pincode",
                "seller_contact_no",
                "discount_price",
                "actual_price",
                "product_sub_category",
                "brand_name",
            )
            .order_by("-id")[:20]
        )
        for x in store_reference:
            final_filtered_data.append(x)

    #
    # if user_status != "True":
    #     for x in final_filtered_data:
    #         # print("XXXXXXXXXX : ", str(x["seller_contact_no"])[:6] + "XXXX")
    #         x["seller_contact_no"] = str(x["seller_contact_no"])[:6] + "XXXX"

    print("final`_filtered_data : ", final_filtered_data)

    return final_filtered_data
