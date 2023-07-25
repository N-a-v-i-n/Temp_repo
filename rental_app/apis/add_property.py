from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token


@csrf_exempt
def add_property(request, user_id):

    token = request.POST.get("token")
    requestmobileno = request.POST.get("user_mobileno")
    password_not_match = False
    is_password_updated = False
    persons_viewed_contact_details=False
    current_user = users.objects.get(id=user_id)

    if request.method == "GET":
            import shutil

            # check for any unused user images in the db i.e 'temp' name images:
            unused_images = (
                (images.objects.filter(user_email_id=current_user.email_id))
                .filter(property_name="temp")
                .values("image")
            )

            # delete the folder from media dir using shell-utilities 'shutil'
            if unused_images:
                try:
                    folder_id = (unused_images[0]["image"]).split("/")
                    shutil.rmtree(f"media/{folder_id[0]}/user_posts/{folder_id[2]}")

                except:
                    pass

                # also delete from db

                (images.objects.filter(user_email_id=current_user.email_id)).filter(
                    property_name="temp"
                ).delete()

            print("unused images are deleted : ", unused_images)
            return HttpResponse("Previour temp data deleted")

    # try:
    if token and requestmobileno:
        try:
            getdatafromdb = users_credentials_app_token.objects.get(
                user_mobile_num=requestmobileno
            )
            print("data from db : ", getdatafromdb.user_token)

            
        except:
            return HttpResponse("User Not Found")

        if str(token) == str(getdatafromdb.user_token) and str(user_id) == str(getdatafromdb.user_id.id):

            if request.method == "POST":
                # below code to check for free limit posted
                if current_user.no_of_free_ad_posted_count < 100:
                    post_adding = post_Ads(request,current_user)

                    print("post_adding 1", post_adding)

                    migrate_images_table = (
                        (images.objects.filter(user_email_id=current_user.email_id))
                        .filter(property_name="temp")
                        .update(property_name=post_adding)
                    )

                    # updating user posted ad counts through finding user via email filter

                    current_user.no_of_free_ad_posted_count += 1
                    current_user.save()

                    # print('expire_date : ',expire_date)
                    data = {
                        "Data_Stored_Success": True,
                    }

                    return HttpResponse(json.dumps(data))
                # if free limit over message
                elif (
                    current_user.no_of_paid_ad_posted_count
                    < current_user.user_ad_posting_enrolled_limit
                ):
                    post_adding = post_Ads(request, current_user)

                    print("post_adding 2 : ", post_adding)

                    migrate_images_table = (
                        (images.objects.filter(user_email_id=current_user.email_id))
                        .filter(property_name="temp")
                        .update(property_name=post_adding)
                    )
                    print()
                    print()
                    print()
                    print("checking", migrate_images_table)

                    # property_name = post_adding[1]

                    # updating user posted ad counts through finding user via email filter

                    current_user.no_of_paid_ad_posted_count += 1
                    current_user.save()

                    # print('expire_date : ',expire_date)
                    data = {
                        "Data_Stored_Success": True,
                    }

                    return HttpResponse(json.dumps(data))

                else:
                    data = {"User_free_post_limit_over": True}

                    return HttpResponse(json.dumps(data))

        else:
            return HttpResponse("Unauthorized to Add")
    else:
        return HttpResponse("Unauthorized")

    # except:
    #      pass


def post_Ads(request, current_user):
    # try:
    property_name = request.POST.get("property_name").lower()

    print(property_name)
    # property_images_temp = request.FILES.getlist("property_images1")

    # print()
    # print()
    # print("check : ", property_images_temp)
    property_type = request.POST.get("property_type").lower()
    property_city = request.POST.get("property_city").lower()
    property_state = request.POST.get("property_state").lower()
    # property_located_in_city=request.POST.get('property_located_in_city')
    property_pincode = request.POST.get("property_pincode").lower()
    property_distict = request.POST.get("property_distict").lower()
    property_floor = request.POST.get("property_floor").lower()
    property_rooms = request.POST.get("property_rooms")
    monthly_rent = request.POST.get("monthly_rent").lower()
    # monthly_maintance=request.POST.get('monthly_maintance')
    # required_doc=request.POST.get('required_doc')
    # advance_amount=request.POST.get('advance_amount')
    # contact_no=0
    house_area = request.POST.get("house_area").lower()
    furnished_or_semi = request.POST.get("furnished_or_semi")
    # tenure_period=request.POST.get('tenure_period')
    parking = request.POST.get("parking").lower()
    # variable_or_fixed=request.POST.get('variable_or_fixed')

    # newlyy added fileds are : -
    appliance_tv = True if request.POST.get("appliance_tv") else False
    appliance_fridge = True if request.POST.get("appliance_fridge") else False
    appliance_sofa = True if request.POST.get("appliance_sofa") else False
    appliance_bed = True if request.POST.get("appliance_bed") else False
    appliance_dresser = True if request.POST.get("appliance_dresser") else False
    appliance_ac = True if request.POST.get("appliance_ac") else False
    appliance_washing_machine = (
        True if request.POST.get("appliance_washing_machine") else False
    )
    appliance_water_heater = (
        True if request.POST.get("appliance_water_heater") else False
    )
    appliance_water_purifier = (
        True if request.POST.get("appliance_water_purifier") else False
    )
    appliance_fans = True if request.POST.get("appliance_fan") else False
    appliance_tubelights = (
        True if request.POST.get("appliance_tubelights") else False
    )
    appliance_Inventers = True if request.POST.get("appliance_Inventers") else False

    new_data = property_details(
        user_emailid_via_login_token=current_user.email_id,
        property_distict=property_distict,
        property_name=property_name,
        property_type=property_type,
        property_city=property_city,
        property_state=property_state,
        property_pincode=property_pincode,
        # property_located_in_city=property_located_in_city,
        property_floor=property_floor,
        rooms=property_rooms,
        monthly_rent=monthly_rent,
        # monthly_maintance=monthly_maintance,
        # required_doc=required_doc,
        # advance_amount=advance_amount,
        # contact_no=contact_no,
        house_area=house_area,
        furnished_or_semi=furnished_or_semi,
        # tenure_period=tenure_period,
        parking=parking,
        # variable_or_fixed=variable_or_fixed,
        # newlyy added fields are :-
        appliance_TV=appliance_tv,
        appliance_Fridge=appliance_fridge,
        appliance_sofa=appliance_sofa,
        appliance_bed=appliance_bed,
        appliance_dresser=appliance_dresser,
        appliance_AC=appliance_ac,
        appliance_washing_machine=appliance_washing_machine,
        appliance_water_heaters=appliance_water_heater,
        appliance_fans=appliance_fans,
        appliance_water_purifier=appliance_water_purifier,
        appliance_tubelights=appliance_tubelights,
        appliance_Inventers=appliance_Inventers,
        created_at=timezone.now(),
        post_expire_date=timezone.now() + datetime.timedelta(days=30),
    )
    new_data.save()

    # Updating user posted logs table
    update_user_ad_posted_logs = ad_posted_logs.objects.create(
        user_details=current_user,
        user_posted_ad_property_id=new_data.id,
        user_posted_date=timezone.now(),
    )
    update_user_ad_posted_logs.save()
    print("Post_ad fun run")
    # data={
    #     "Success":'true',
    #     "new_data" : new_data.id
    # }
    return (json.dumps(new_data.id))

    # except:
    #     return "Failure"

@csrf_exempt
def images_files(request,user_id):
    import base64
    from PIL import Image, ImageDraw, ImageFont

    token = request.POST.get("token")
    requestmobileno = request.POST.get("user_mobileno")
    password_not_match = False
    is_password_updated = False
    persons_viewed_contact_details=False

    # try:
    if token and requestmobileno:
        try:
            getdatafromdb = users_credentials_app_token.objects.get(
                user_mobile_num=requestmobileno
            )
            print("data from db : ", getdatafromdb.user_token)

            current_user = users.objects.get(id=user_id)
            print("Getted in", current_user, "token : ",token, "User mobile no : ",requestmobileno)

        except:
            return HttpResponse("User Not Found")

        if str(token) == str(getdatafromdb.user_token) and str(user_id) == str(getdatafromdb.user_id.id):
            property_images_temp = request.FILES.getlist("temp")
            # property_images_temp1=request.POST.get('base_file')

            # print("asdaihsja : ",property_images_temp)
            # print("kjksnax : ",property_images_temp1)

            users_previous_product_id = [
                x[0]
                for x in property_details.objects.filter(
                    user_emailid_via_login_token=current_user.email_id
                ).values_list("id")
            ]
            users_previous_product_id.sort(reverse=True)

            try:
                id = f"{current_user.id}/user_posts/{current_user.id}.pre_{(users_previous_product_id[:1])[0]}"
                print("Getted in 1")


            except:
                id = f"{current_user.id}/user_posts/{current_user.id}.pre_{0}"
                print("Getted in 2")

            validate = images_validate(property_images_temp[0], id)
            print("output from validate", validate)

            if validate:
                new_images = images.objects.create(
                    image=validate[0], user_email_id=current_user.email_id
                )
                new_images.save()
                result_response = validate[1]
                try:
                    try:
                        safe = round((result_response["predictions"]["safe"]))
                        print("safe : ", bool(safe))
                        if bool(safe):
                            update_image = images.objects.get(id=new_images.id)
                            update_image.Is_image_safe = True
                            update_image.save()

                        print("Image Saved")

                    except:
                        unsafe = round((result_response["predictions"]["unsafe"]))
                        print("unsafe : ", bool(unsafe))

                        if bool(unsafe):
                            entry_on_unsafe_table = unsafe_images.objects.create(
                                image_id=new_images,
                                unsafe_img=True,
                                created_at=timezone.now(),
                                unsafe_reason=result_response,
                            )
                            entry_on_unsafe_table.save()
                except Exception as error:
                    new_error_save = failure_response.objects.create(
                        failure_message=error,
                        other_responses=result_response,
                        failure_user_details=current_user,
                        created_At=timezone.now(),
                    )
                    new_error_save.save()

                return HttpResponse("Image saved on db Success")
        else:
            return HttpResponse("Not Match")
    else:
        return HttpResponse("enter prper credentials")
