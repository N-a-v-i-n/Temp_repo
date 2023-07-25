from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
import secrets
from rental_app.models import users_credentials_app_token


@csrf_exempt
def app_login(request):
    data1 = request.POST.get("user_mobileno")
    data2 = request.POST.get("user_password")

    print("data1 : ", data1)
    print("data2 : ", data2)

    if data1 and data2:
        user_mobile_no = data1
        user_password = data2
        user_coordinates = request.POST.get("user_coordinates")
        user_mobiles_details = request.POST.get("user_mobile_details")

        # Checking User Credentials
        try:
            user_details = users.objects.get(mobile_no=user_mobile_no)

            print("user_details : ", user_details)

        except:
            data = {"user_not_found": True}

            return HttpResponse(json.dumps(data))

        check_already_logined = users_credentials_app_token.objects.filter(
            user_mobile_num=user_mobile_no
        )
        check_already_logined.delete()

        if str(user_password) == str(user_details.user_password):
            print("User Login success")

            ## Taking users ip address and passing a token ND BOTH TOKEN nd IP address are stored in db

            gen_token = secrets.token_hex(12)

            new_user_credentials = users_credentials_app_token.objects.create(
                user_id=user_details,
                user_email_id=user_details.email_id,
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

            data = {
                "status": True,
                "login_token": gen_token,
                "user_id": user_details.id,
            }

            return HttpResponse(json.dumps(data))

        else:
            data = {"user_not_found": True}

            return HttpResponse(json.dumps(data))

    return HttpResponse("no data found")
