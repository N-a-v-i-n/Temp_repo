from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token


@csrf_exempt
def app_profile(request, user_id):
    token = request.POST.get("token")
    requestmobileno = request.POST.get("user_mobileno")
    password_not_match = False
    is_password_updated = False
    persons_viewed_contact_details=False
    try:
        if token and requestmobileno:
            try:
                getdatafromdb = users_credentials_app_token.objects.get(
                    user_mobile_num=requestmobileno
                )
                print("data from db : ", getdatafromdb.user_token)

                current_user_details = users.objects.get(id=user_id)
            except:
                return HttpResponse("User Not Found")

            if str(token) == str(getdatafromdb.user_token) and str(user_id) == str(
                getdatafromdb.user_id.id
            ):
                # Below code is to delete property_post from users_profile
                property_post_id = request.POST.get("delete_post")

                print("property_post_id: ", property_post_id)

                if property_post_id:
                    user_Added_properties = []
                    try:
                        user_Added_properties = [
                            x[0]
                            for x in property_details.objects.filter(
                                user_emailid_via_login_token=current_user_details.email_id
                            ).values_list("id")
                        ]
                        print("user_Added_properties : ", user_Added_properties)
                    except:
                        return HttpResponse("Unauthorize to delete")
                    if int(property_post_id) in user_Added_properties:
                        property_info = property_details.objects.get(
                            id=property_post_id
                        )

                        property_details.objects.filter(id=property_post_id).delete()

                        posted_imgs = images.objects.filter(
                            property_name=property_post_id
                        )
                        checkk = posted_imgs.values("image")
                        fetch_folder_name = (checkk[0]["image"]).split("/")

                        user_liked.objects.filter(
                            liked_property_ids=property_post_id
                        ).delete()

                        # update deleted post on db

                        new_deleted_data = Deleted_post_details.objects.create(
                            post_id=property_post_id,
                            post_user_email=current_user_details.email_id,
                            posted_user_contact_details=current_user_details.mobile_no,
                            post_address=property_info.property_city,
                            deleted_at=timezone.now(),
                        )
                        new_deleted_data.save()

                        # Also Delete Post Images From MediaFiles
                        import shutil

                        # check for any unused user images in the db i.e 'temp' name images:
                        if fetch_folder_name:
                            try:
                                shutil.rmtree(
                                    f"media/{fetch_folder_name[0]}/user_posts/{fetch_folder_name[2]}"
                                )

                            except:
                                pass

                        posted_imgs.delete()
                        print(f"property-ID {property_post_id} successfully deleted")
                    else:
                        return HttpResponse("Unauthorize to delete")

                # below code is to update password
                current_password = request.POST.get("current_password")

                if current_password:
                    new_password = request.POST.get("new_password")
                    # Check for current_password is valid or not
                    if str(current_password) == str(current_user_details.user_password):
                        current_user_details.user_password = new_password
                        current_user_details.save()
                        is_password_updated = True
                        print("Password Updated")
                    else:
                        print("Password miss match")
                        password_not_match = True

                # Below code is to update user_profile details
                profile_update = request.POST.get("profile_updating")
                print("Profile Update : ", profile_update)

                if profile_update:
                    # print('uSER EMAIL = ',user_email_fetched_based_on_user_token[0])
                    first_name = request.POST.get("first_name")

                    print("data received first_name : ", first_name)
                    last_name = request.POST.get("last_name")
                    # email_id=request.POST.get('email_id')
                    mobile_no = request.POST.get("mobile_no")
                    Bio = request.POST.get("Bio")

                    print(
                        "current_user_details.first_name : ",
                        current_user_details.first_name,
                    )
                    if first_name:
                        current_user_details.first_name = first_name
                    if last_name:
                        current_user_details.last_name = last_name
                    if mobile_no:
                        current_user_details.mobile_no = mobile_no
                        change_on_app_credential = (
                            users_credentials_app_token.objects.get(
                                user_email_id=current_user_details.email_id
                            )
                        )
                        change_on_app_credential.user_mobile_num = mobile_no
                        change_on_app_credential.save()
                    if Bio:
                        current_user_details.Bio = Bio

                    current_user_details.save()

                profile_pic_change = request.FILES.get("profile_pic")
                if profile_pic_change:
                    print("profile_pic_change : ", profile_pic_change)
                    allowed_formats = ["JPG", "PNG", "JPEG", "WEBP"]

                    user_side_img = Image.open(profile_pic_change)
                    if user_side_img.format.upper() in allowed_formats:
                        print()
                        print()
                        print()
                        print("Image Satisfied the Format")
                        try:
                            os.makedirs(f"media/{current_user_details.id}/profile_img")

                        except:
                            pass
                        profile_img_loc = f"media/{current_user_details.id}/profile_img/profile_pic.jpeg"
                        user_side_img.save(profile_img_loc)

                        new_image = users.objects.get(
                            email_id=current_user_details.email_id
                        )
                        new_image.user_profile_pic = profile_img_loc
                        new_image.save()
                        print("Profile Pic Updated !!")
                    else:
                        return HttpResponse("Profile Picture Format errror")
                    # fetching email_id from user_token

                fetching_all_user_data = users.objects.filter(
                    email_id=current_user_details.email_id
                ).values(
                    "first_name",
                    "last_name",
                    "email_id",
                    "mobile_no",
                    "Bio",
                    "user_profile_pic",
                )[
                    :1
                ]
                print("user details on db, ", fetching_all_user_data)
                # Fetching property_details on user_email

                user_property_details = list(
                    map(
                        lambda x: x[0],
                        property_details.objects.filter(
                            user_emailid_via_login_token=current_user_details.email_id
                        ).values_list("id"),
                    )
                )
                print(user_property_details)

                user_selling_property_images = []
                try:
                    for x in user_property_details:
                        # formate:-  >   {1: 'WhatsApp_Image_2023-03-04_at_18.08.06_1.jpeg', 2: 'WhatsApp_Image_2023-03-04_at_18.07.44_1.jpeg'}

                        # user_selling_property_images[x] = (
                        #     images.objects.filter(property_name=x).values_list("image")[
                        #         :1
                        #     ]
                        # )[0][0]
                        user_selling_property_images.append({x:
                            (
                            images.objects.filter(property_name=x).values_list("image")[
                                :1
                            ]
                        )[0][0]
                        })
                except:
                    pass

                # user_selling_property_images=list(map(lambda x:x,[images.objects.filter(property_name=x).values('image') for x in user_property_details]))
                print("user_selling_property_images : ", user_selling_property_images)
                print("user data : ", fetching_all_user_data)
                if user_selling_property_images == {}:
                    user_selling_property_images = False
                
                try:
                    persons_viewed_contact_details=(send_text_to_owner.objects.filter(receiver_user_id=user_id).values('request_user_id')).distinct()
                    print("persons_viewed_contact_details : ",len(persons_viewed_contact_details))
                except:
                    pass

                print()
                print()
                print()
                print("fetching_all_user_data : ", fetching_all_user_data)
                print("user_selling_property_images : ", user_selling_property_images)

                data = {
                    "user_data": fetching_all_user_data[0],
                    "user_property_details": user_selling_property_images,
                    "user_verifed": True,
                    "password_not_match": password_not_match,
                    "is_password_updated": is_password_updated,
                    "persons_viewed_contact_details":len(persons_viewed_contact_details),
                }
                return HttpResponse(json.dumps(data))

            else:
                return HttpResponse("Unauthorized")

    except:
        return HttpResponse("Something went wrong")

    return HttpResponse("Unauthorized")
