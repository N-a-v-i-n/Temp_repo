from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token


@csrf_exempt
def app_adpost(request):
    token = request.POST.get("token")
    requestmobileno = request.POST.get("user_mobileno")
    try:
        if token and requestmobileno:
            getdatafromdb = users_credentials_app_token.objects.get(
                user_mobile_num=requestmobileno
            )
            print("data from db : ", getdatafromdb.user_token)
            if str(token) == str(getdatafromdb.user_token):
                # data = {
                #     # "token verified": True,
                #     "homepg data": ,
                # }
                return HttpResponse(json.dumps(data))

            else:
                return HttpResponse("Unauthorized")

    except:
        data = {"User not Found": True}
        return HttpResponse(json.dumps(data))

    return HttpResponse("hello")
