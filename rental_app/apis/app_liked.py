from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token


@csrf_exempt
def Appliked(request, user_id):
        try:
            current_user = users.objects.get(id=user_id)
        except:
            print("entered")
            current_user=False

        if current_user:
            fetched_liked_id = [
                x
                for x in user_liked.objects.filter(user_email=current_user.email_id)
                .values("liked_property_ids")
                .distinct()
            ]
            print("fetched_liked_id :__________",fetched_liked_id)
            if fetched_liked_id:
                all_in_one = []
                for x in fetched_liked_id:
                    tempstore_ref={}
                    tempstore_ref.update([x for x in property_details.objects.filter(id=x['liked_property_ids']).values('id','property_city','property_state','rooms','monthly_rent','furnished_or_semi')][0])
                    tempstore_ref.update([x for x in images.objects.filter(property_name=x['liked_property_ids']).values('image').distinct()][0])
                    # print("tempstore_ref : ",tempstore_ref)
                    all_in_one.append({f"ID-{x['liked_property_ids']}":tempstore_ref})
                print("all_in_one : ",all_in_one)               
                data = {
                    "Favourate-items":all_in_one ,
                }

                return HttpResponse(json.dumps(data))
            
            else:
                 return HttpResponse("No data Found")
        else:
            return HttpResponse("User not found")