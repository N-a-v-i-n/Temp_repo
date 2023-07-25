from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
import secrets
from rental_app.models import users_credentials_app_token


@csrf_exempt
def app_signup(request):
    data1 = request.POST.get("user_mobileno")
    data2 = request.POST.get("user_password")

    if data1 and data2:
        user_emailid = request.POST.get("user_emailid")
        user_mobile_no = data1
        user_password = data2
        user_platform = request.POST.get("user_platform")
        # Checking User Credentials

        Is_Exist = mobile_no_r_email_existance(user_emailid, user_mobile_no)

        if Is_Exist == False:
            user_coordinates = request.POST.get("user_coordinates")
            user_mobiles_details = request.POST.get("user_mobile_details")

            new_data = users.objects.create(
                email_id=user_emailid,
                mobile_no=user_mobile_no,
                user_password=user_password,
                created_at=timezone.now(),
                user_platform=user_platform,
            )

            new_data.save()

            ## Taking users ip address and passing a token ND BOTH TOKEN nd IP address are stored in db

            gen_token = secrets.token_hex(12)

            new_user_credentials = users_credentials_app_token.objects.create(
                user_id=new_data,
                user_email_id=new_data.email_id,
                user_ip_address="none",
                user_token=gen_token,
                createdAt=timezone.now(),
                user_state_by_geo_loc="none",
                user_coordinates=user_coordinates if user_coordinates else "None",
                user_mobile_data=user_mobiles_details
                if user_mobiles_details
                else "None",
                user_mobile_num=user_mobile_no,
            )

            new_user_credentials.save()

            data = {"status": True, "login_token": gen_token, "user_id": new_data.id}

            return HttpResponse(json.dumps(data))

        else:
            data = {"user_found": True}

            return HttpResponse(json.dumps(data))

    return HttpResponseBadRequest()
