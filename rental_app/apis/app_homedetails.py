from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token


@csrf_exempt
def app_homedetails(request):
    token = request.POST.get("token")
    requestmobileno = request.POST.get("user_mobileno")
    try:
        if token and requestmobileno:
            getdatafromdb = users_credentials_app_token.objects.get(
                user_mobile_num=requestmobileno
            )
            print("data from db : ", getdatafromdb.user_token)
            if str(token) == str(getdatafromdb.user_token):
                sendhomepgdata = [
                    x
                    for x in property_details.objects.all().values(
                        "id",
                        "property_city",
                        "property_state",
                        "property_pincode",
                        "monthly_rent",
                        "furnished_or_semi",
                        "rooms",
                    )
                ]
                # sendhomepgdata_images = []
                for x in sendhomepgdata:
                    try:
                        images_temp = (
                        images.objects.filter(property_name=x["id"])
                        .values("image")
                        .exclude(Is_image_safe=False)
                        ).first()
                        x.update(images_temp)
                    except:
                        pass

                data = {
                    # "token verified": True,
                    "homepg data": sendhomepgdata,
                }
                return HttpResponse(json.dumps(data))

            else:
                return HttpResponse("Unauthorized")

    except:
        data = {"User not Found": True}
        return HttpResponse(json.dumps(data))
