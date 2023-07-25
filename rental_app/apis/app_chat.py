from ..views.common_imports import *
from django.views.decorators.csrf import csrf_exempt
from rental_app.models import users_credentials_app_token
from django.db.models import Q



@csrf_exempt
def Appchat(request, user_id):

    token = request.POST.get("token")
    requestmobileno = request.POST.get("user_mobileno")

    if token and requestmobileno:
        current_user = users.objects.get(id=user_id)
        try:
            getdatafromdb = users_credentials_app_token.objects.get(
                user_mobile_num=requestmobileno
            )
            print("data from db : ", getdatafromdb.user_token)

            
        except:
            return HttpResponse("User Not Found")

        if str(token) == str(getdatafromdb.user_token) and str(user_id) == str(getdatafromdb.user_id.id):

            current_user_details = current_user

            temp_storeref= [x for x in send_text_to_owner.objects.filter(
                receiver_user_id=current_user_details.id
            ).values(
                "request_user_time", "request_user_mobile_no", "request_property_id"
            )
            ]
            print("convert  ::: ",temp_storeref)
            
            get_all_received_noti=temp_storeref
            for x in range(len(temp_storeref)):
                convert_datetime_to_str=str(temp_storeref[x]['request_user_time']+timezone.timedelta(minutes=330))
                # print("============================= Before : ",timezone.datetime(2023, 7, 12, 8, 23, 49, 492839))

                # print("============================= After : ",temp_storeref[x]['request_user_time']+timezone.timedelta(minutes=330))
                get_all_received_noti[x]['request_user_time']=convert_datetime_to_str    
            print("get_all_received_noti : ",get_all_received_noti)       
            checking_for_message_update = get_all_received_noti

            print("checking_for_message_update : ", checking_for_message_update)

            if checking_for_message_update:
                print("Heell01")
                message_data_temp = [x for x in checking_for_message_update]
                print("Heell02")

                message_data = [x for x in checking_for_message_update]

                list_of_product = list()
                try:
                    for x in range(len(message_data)):
                        
                        list_of_product = [
                            x
                            for x in property_details.objects.filter(
                                id=message_data_temp[x]["request_property_id"]
                            ).values("property_name", "property_city", "monthly_rent","property_state","furnished_or_semi","rooms")
                        ]
                        print("List_of_PD : ",list_of_product)
                        property_images = (
                            images.objects.filter(
                                property_name=message_data_temp[x][
                                    "request_property_id"
                                ]
                            ).values("image")
                        ).distinct()
                        if list_of_product:
                            message_data[x].update(list_of_product[0])
                            message_data[x].update(property_images[0])
                        else:
                            message_data[x].update({"Property_Deleted" : True})
                            
                except Exception as temp:
                    pass
                print("message_data : ", message_data)

                data={
                    "Message data" : message_data
                }

                return HttpResponse(json.dumps(data))
            else:
                data={
                        "Message data" : False
                    }
                return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("User no found")

    return HttpResponse("Unauthorized")




@csrf_exempt
def Appchat_Event(request, user_id):
    
    try:
        current_user = users.objects.get(id=user_id)
        print("User Found")
        token = request.POST.get("token")
        requestmobileno = request.POST.get("user_mobileno")
    except:
        return HttpResponse("User Not Found")
    
    if token and requestmobileno:
        current_user = users.objects.get(id=user_id)
        try:
            getdatafromdb = users_credentials_app_token.objects.get(
                user_mobile_num=requestmobileno
            )
            print("data from db : ", getdatafromdb.user_token)

            
        except:
            return HttpResponse("User Not Found")

        if str(token) == str(getdatafromdb.user_token) and str(user_id) == str(getdatafromdb.user_id.id):


            if current_user:
                
                update_send_text_table=send_text_to_owner.objects.filter(Q(receiver_user_id=current_user),Q(reciever_seen=False))
                print("Updated Message table",update_send_text_table.values())
                if update_send_text_table:
                    update_send_text_table.update(reciever_seen=True)
                    print("Updated Message table",update_send_text_table)
                    return HttpResponse("Event Suceess")
                else:
                    return HttpResponse("No text Received")

            return HttpResponse("Event Unsuccess")
        else:
            return HttpResponse("Unauthorized Token")
    
    elif current_user:
        print("Current user : ",current_user)
        User_recived_text=send_text_to_owner.objects.filter(Q(receiver_user_id=current_user),Q(reciever_seen=False ))
        print("Updated Message table",User_recived_text)
        data={
            "unseen_text_len" : len(User_recived_text)
        }
        return HttpResponse(json.dumps(data))

    