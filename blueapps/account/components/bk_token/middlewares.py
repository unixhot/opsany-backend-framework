# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib import auth
import json
import os

from django.conf import settings

from base.models import UserInfo

try:
    from django.utils.deprecation import MiddlewareMixin
except Exception:
    MiddlewareMixin = object
from config import BK_URL, APP_CODE, SECRET_KEY
from blueapps.account.conf import ConfFixture
from blueapps.account.handlers.response import ResponseHandler, JsonResponse
from blueapps.account.components.bk_token.forms import AuthenticationForm
from component.status_code import error, ErrorStatusCode
ENV = {"development": "", "production": "o", "testing": "t"}
logger = logging.getLogger('component')


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        """
        Login paas by two ways
        1. views decorated with 'login_exempt' keyword
        2. User has logged in calling auth.login
        """
        from component.base_views import _get_ops_language_from_cookie

        request.COOKIES.update(**{"bk_token_username": None})
        request.COOKIES.update(**{"bk_esb_username": None})
        try:
            request.COOKIES.update(**{"bk_token": settings.BK_TOKEN})
        except:
            pass

        # request.COOKIES.update(**{"opsany_language": "english"})

        if hasattr(request, 'is_wechat') and request.is_wechat():
            return None

        if hasattr(request, 'is_bk_jwt') and request.is_bk_jwt():
            return None

        if getattr(view, 'login_exempt', False):
            return None
        form = AuthenticationForm(request.COOKIES)
        login_out_url = "https%3A//" + BK_URL.split("https://")[-1] + "/" \
                        + ENV.get(os.getenv("BK_ENV", "development")) + "/{}/&is_from_logout=1".format(APP_CODE)
        if form.is_valid():
            bk_token = form.cleaned_data['bk_token']
            user = None
            if bk_token:
                user = auth.authenticate(request=request, bk_token=bk_token)
            if not user:
                if self._check_app_token(request):
                    return None
                return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN, login_out_url, language=_get_ops_language_from_cookie(request)))
            if user.username and user.is_active:
                request.COOKIES.update(**{"bk_token_username": user.username})
                return None
            return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN, login_out_url, language=_get_ops_language_from_cookie(request)))

        if self._check_app_token(request):
            return None

        if request.path_info == "/":
            handler = ResponseHandler(ConfFixture, settings)
            return handler.build_401_response(request)
        else:
            return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN, login_out_url, language=_get_ops_language_from_cookie(request)))

    def _check_app_token(self, request):
        headers = request.headers
        app_code = headers.get("X-APP-CODE")
        app_token = headers.get("X-APP-TOKEN")
        if APP_CODE == app_code and app_token == SECRET_KEY:
            try:
                data = json.loads(request.body)
            except:
                data = {}
            bk_esb_username = request.GET.get("operator") or request.POST.get("operator") or data.get(
                "operator")
            query = UserInfo.objects.filter(username=bk_esb_username).first()
            if query:
                if query.username and query.is_activate:
                    request.COOKIES.update(**{"bk_esb_username": bk_esb_username})
                    return True
        return False

    def process_response(self, request, response):
        return response
