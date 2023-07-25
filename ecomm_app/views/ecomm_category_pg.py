from .common_imports import *
from rental_app.views.common_imports import *
import urllib


def ecomm_category_pg(request, categoryName):
    data_not_found = False

    url_params_state = request.GET.get("State")
    if url_params_state == "None":
        get_all_state_category = (
            ecomm_product_details.objects.filter(product_category=categoryName).values(
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
                "product_sub_category",
                "brand_name",
                "discount_price",
                "actual_price",
            )
        ).order_by("-id")

    print("url_params_state : ", url_params_state)
    print("categoryName : ", categoryName)

    if url_params_state != "None":
        get_all_state_category = (
            (
                ecomm_product_details.objects.filter(
                    product_category=categoryName
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
                    "product_sub_category",
                    "brand_name",
                    "discount_price",
                    "actual_price",
                )
            )
            .filter(selling_state=str(url_params_state))
            .order_by("-id")
        )

    fetch_sub_category, brand_names = sub_category(categoryName)
    print("fetch_sub_category : ", fetch_sub_category)

    # below code to Filter datas:-
    filtered_data = []
    filter_data_given = request.GET.get("filter_active")
    print("filter_data_given : ", filter_data_given)
    if filter_data_given:
        state_selection = request.GET.get("State")
        city_selection = request.GET.get("city_selection")
        sub_categories_selected = []
        for x in fetch_sub_category:
            temp = request.GET.get(x)
            if temp:
                # print(f"{x} :", temp)
                sub_categories_selected.append(x)

        max_min_radio = request.GET.get("max_min_radio")
        Min_Range = request.GET.get("Min_Range")
        Max_Range = request.GET.get("Max_Range")

        filter_brand_names = []
        for x in brand_names:
            temp2 = request.GET.get(x[0])
            if temp2:
                filter_brand_names.append(x[0])

        print("state_selection : ", state_selection)
        print("city_selection : ", city_selection)
        print("max_min_radio : ", max_min_radio)
        print("Min_Range : ", Min_Range)
        print("Max_Range : ", Max_Range)

        # if state wise exist:-
        from django.db.models import Q

        if state_selection:
            temp_filter_data = []
            data_state = (
                ecomm_product_details.objects.filter(
                    Q(product_category=str(categoryName))
                    & Q(selling_state=str(state_selection))
                ).values(
                    "product_category",
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
                    "product_sub_category",
                    "brand_name",
                    "discount_price",
                    "actual_price",
                )
            ).order_by("-id")

            print(
                "temp_filter_data : ",
            )
            if data_state:
                temp_filter_data.append(data_state)

            if temp_filter_data:
                filtered_data = temp_filter_data[0]

            else:
                data_not_found = True

        else:
            filtered_data.append(get_all_state_category)

        # if city wise exist:-
        if city_selection and city_selection != "City":
            print("City : ")
            temp_city1_filter_data = []

            for x in filtered_data:
                if str(x["selling_city"]) == str(city_selection):
                    temp_city1_filter_data.append(x)

            if temp_city1_filter_data:
                filtered_data = temp_city1_filter_data
            else:
                data_not_found = True

        if sub_categories_selected:
            temp_sub_Category_filter_data = []
            for x in filtered_data:
                for y in sub_categories_selected:
                    if str(y) == str(x["product_sub_category"]):
                        temp_sub_Category_filter_data.append(x)

            print("temp_sub_Category_filter_data : ", temp_sub_Category_filter_data)

            if temp_sub_Category_filter_data:
                filtered_data = temp_sub_Category_filter_data

            else:
                data_not_found = True
        print("filter_brand_names : ", filter_brand_names)
        if filter_brand_names:
            temp_brand_name_filter_data = []
            for x in filtered_data:
                for y in filter_brand_names:
                    if str(y) == str(x["brand_name"]):
                        temp_brand_name_filter_data.append(x)

            print("temp_brand_name_filter_data : ", temp_brand_name_filter_data)

            if temp_brand_name_filter_data:
                filtered_data = temp_brand_name_filter_data

            else:
                data_not_found = True

    print("filtered_data : ", filtered_data)

    data = {
        "get_all_state_category": filtered_data
        if filter_data_given
        else get_all_state_category,
        "fetch_sub_category": fetch_sub_category,
        "brand_names": [x[0] for x in brand_names],
        "data_not_found": data_not_found,
    }

    return render(request, "ecomm_category_pg.html", data)


# --------------- OTHER METHODS ------------------


def sub_category(main_category):
    Home_Appliances = [
        "Kitchen Appliances",
        "Kitchenware",
        "Home Furnishing",
        "Home Decoratives",
        "Furniture",
        "Others",
    ]

    Medical_Equipments = [
        "Tablets & Syrups",
        "Syringes",
        "Nebulizer",
        "Thermometer",
        "Sphygmomanometer",
        "Hospital bed",
        "Stethoscope",
        "Wheelchair",
        "Scalpel",
        "Operating table",
        "Electrocardiography",
        "Defibrillation",
        "Ventilator",
        "Surgical instrument",
        "Others",
    ]

    Electrioncs = [
        "Mobiles & Tablets",
        "Mobile & Tablet Accessories",
        "Tv's and Laptop's",
        "Headphones & Earphones",
        "Speakers & Soundbars",
        "Watches",
        "Storage",
        "Computers Peripherals",
        "Cameras & Accessories",
        "Active and Passive Equipments",
        "Others",
    ]

    Fashion = [
        "Men's Topwear",
        "Men's Activewear",
        "Men's Footwear",
        "Men's Accessories",
        "Men's Bottomwear",
        "Indian Ethnicwear",
        "Women's Footwear",
        "Women's Accessories",
        "Others",
    ]

    AutoMotive = [
        "Bike Accessories",
        "Car Accessories",
        "Auto Accessories",
        "Transport Accessories",
        "Others",
    ]

    Electricals = [
        "Wires & Cables",
        "Distribution Boards",
        "Industrial Switches & Controls",
        "Micro Drives",
        "Switch and Sockets",
        "Circuit Breakers and Fuses",
        "Power Generation and Transformers",
        "Relays and contactors",
        "Others",
    ]
    Constructions = [
        "Cement",
        "Bricks",
        "Soil",
        "Water",
        "Steel",
        "Bitumen",
        "Concrete",
        "Structured Steel",
        "Binding Wires",
        "Fly Ash",
        "Aggregate",
        "Blocks",
        "Timber",
        "Nails",
        "Lime",
        "Bamboo",
        "Pipes",
        "Glasses",
        "Tiles",
        "Marble",
        "Mud",
        "Metal Steel",
        "Tar",
        "Chipborad",
        "Rope",
        "Stone",
        "Green Cement",
        "Granite",
        "Primer",
        "Paints",
        "Gypsum",
        "Gypsum Board",
        "Ceramics",
        "Copper",
        "Sanitary and Fittings",
        "Gravel",
        "Others",
    ]
    categories = {
        "Home Appliances": Home_Appliances,
        "Medical Equipments": Medical_Equipments,
        "Electrioncs": Electrioncs,
        "Fashion": Fashion,
        "AutoMotive": AutoMotive,
        "Electricals": Electricals,
        "Constructions": Constructions,
    }
    print(type(categories))

    for keys, values in categories.items():
        if str(main_category) == str(keys):
            brand_names = ecomm_product_details.objects.filter(
                product_category=main_category
            ).values_list("brand_name")

            return values, set(brand_names)
