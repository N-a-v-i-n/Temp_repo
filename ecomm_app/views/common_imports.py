from django.shortcuts import render, HttpResponseRedirect

from ecomm_app.models import (
    ecomm_product_details,
    ecomm_users,
    ecomm_users_credentials_IPs,
)

from django.shortcuts import HttpResponse
import random, datetime
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone
import re, math
import json
import secrets
import socket
from django.contrib.auth.tokens import default_token_generator
from rental_app.automate_sell import adding_rents_house
from rental_app.images_validations import images_validate
from django.http import HttpResponseBadRequest

from PIL import Image, ImageDraw, ImageFont
import os, sys
import random, datetime, base64
from django.utils import timezone
from django.shortcuts import HttpResponse
