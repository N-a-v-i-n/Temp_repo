"""house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


# state_city_py
import all_states_cities

# from rental_app import views
from rental_app.views import (
    homepage,
    product,
    signup,
    login,
    liked,
    profile,
    update_property,
    help_support,
    plans,
    pageNotFound,
    sell,
    terms_and_conditions,
    privacy_policy,
    admin_user,
)

from ecomm_app.views import (
    ecomm_homepage,
    ecomm_post_ad,
    ecomm_category_pg,
    ecomm_product,
)

from django.conf import settings
from django.conf.urls.static import static

# app api's -------------------------
from rental_app.apis import (
    app_login,
    app_signup,
    app_homedetails,
    app_product,
    app_profile,
    app_adpost,
    delete_post,
    add_property,
    app_chat,
    app_liked
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage.homepage),
    path("<int:page_no>", homepage.homepage),
    path("product/", product.product),
    path("signup/", signup.signup),
    path("login/", login.login),
    path("product/<int:productID>", product.product),
    path("sell/", sell.sell),
    # path('success/',views.success,name='success'),
    path("liked/", liked.favour),
    path("profile/", profile.profile),
    path("update/<int:productID>", update_property.update_property),
    path("help_support/", help_support.help_support),
    # path('paymentGW/',payment_gateway.payment_gateway),
    path("plans/", plans.plans),
    # path('paymenthandler/', payment_gateway.paymenthandler, name='paymenthandler'),
    path("paymenthandler/", plans.paymenthandler, name="paymenthandler"),
    path("pageNotFound/", pageNotFound.pageNotFound),
    path("sell/images/", sell.images_files),
    path("terms&conditions/", terms_and_conditions.terms_And_conditons),
    path("privacy-policy", privacy_policy.privacy_policy),
    path("admin-user/", admin_user.admin_user),
    path("admin-user/upload/", admin_user.admin_user_upload),
    # ------------------------------------------------------------------------------
    path("ecomm/", ecomm_homepage.homepage),
    path("ecomm-sell/", ecomm_post_ad.ecomm_sell),
    path("ecomm/<categoryName>/", ecomm_category_pg.ecomm_category_pg),
    path("ecomm-product/", ecomm_product.ecomm_product),
    # -------------------------------------------------------------------------------
    path(
        "search_for_citites_92839890104958379482983023/<stateName>",
        all_states_cities.search_for_citites,
    ),
    path("ecomm111111/38108042840kajsnkackja/", ecomm_homepage.homepg_for_api),
    # ------------------app api's----------------------------------------------------
    path("api-rental/login/", app_login.app_login),
    path("api-rental/signup/", app_signup.app_signup),
    path("api-rental/home/", app_homedetails.app_homedetails),
    path("api-rental/product/<user_id>&<int:productid>", app_product.app_product),
    path("api-rental/adpost/", app_adpost.app_adpost),
    path("api-rental/profile/<int:user_id>", app_profile.app_profile),
    path("api-rental/delete_post/<int:user_id>&<int:post_id>", delete_post.delete_post),
    path("api-rental/add_post/<int:user_id>", add_property.add_property),
    path("api-rental/add_post_images/<int:user_id>", add_property.images_files),
    path("api-rental/appchat/<int:user_id>", app_chat.Appchat),
    path("api-rental/appchat-event/<int:user_id>", app_chat.Appchat_Event),
    path("api-rental/appliked/<int:user_id>", app_liked.Appliked),





]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',views.homepage),
#     path('<int:page_no>',views.homepage),
#     path('product/', views.product),
#     path('signup/',views.signup),
#     path('login/',views.login),
#     path('product/<int:productID>',views.product),
#     path('sell/',views.sell),
#     path('success/',views.success,name='success'),
#     path('liked/',views.favour),
#     path('profile/',views.profile),
#     path('update/<int:productID>',views.update_property),
#     path('help_support/',views.help_support),

# ]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
