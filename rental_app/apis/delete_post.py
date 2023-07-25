from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token


@csrf_exempt
def delete_post(request, user_id,post_id):
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

            if str(token) == str(getdatafromdb.user_token) and str(user_id) == str(getdatafromdb.user_id.id):
                
                property_post_id = post_id

                print("property_post_id: ", property_post_id)
                Is_user_auth_to_delete=[x[0] for x in property_details.objects.filter(user_emailid_via_login_token=current_user_details.email_id).values_list('id')]
                print("Is_user_auth_to_delete : ",Is_user_auth_to_delete)
                if property_post_id in Is_user_auth_to_delete:
                    try: 
                        property_info = property_details.objects.get(id=property_post_id)
                    except:
                        return HttpResponse("Invalid Details")

                    property_details.objects.filter(id=property_post_id).delete()
                    posted_imgs = images.objects.filter(property_name=property_post_id)
                    checkk = posted_imgs.values("image")
                    fetch_folder_name = (checkk[0]["image"]).split("/")

                    user_liked.objects.filter(liked_property_ids=property_post_id).delete()

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

                    return HttpResponse(f"property-ID {property_post_id} successfully deleted")

                else:
                    return HttpResponse("Unauthorized to delete")
            else:
                return HttpResponse("Unauthorized")

    except:
         return HttpResponse("something went wrong")