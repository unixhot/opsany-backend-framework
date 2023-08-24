from django.views import View

from component.esb_api import EsbApi

from config import DEFAULT_LANGUAGE


class BaseView(View):
    def ops_language(self):
        return _get_ops_language_from_cookie(self.request)

class BaseObject:
    def __init__(self, request=None):
        self.http_request = request

    def ops_language(self):
        return _get_ops_language_from_cookie(self.http_request)


def _get_ops_language_from_cookie(request):
    """
    获取返回值语言顺序：
    1. 请求头COOKIES获取平台语言
    2. 去工作台个人中心配置的语言
    3. 系统配置初始默认语言
    """
    from base.models import UserInfo
    cookie_ops_language_key = "opsany_language"
    # chinese_simplified chinese_traditional english
    language = ""
    if request:
        language = request.COOKIES.get(cookie_ops_language_key) or request.headers.get(cookie_ops_language_key)
        # if (not language) or (language not in ["chinese_simplified", "chinese_traditional", "english"]):
        if (not language):
            bk_token_username = request.COOKIES.get("bk_token_username")
            user_query = UserInfo.fetch_one(username=bk_token_username)
            if user_query:
                language_theme_config = EsbApi().get_language_theme_config(bk_token_username)
                language = language_theme_config.get("")
    if not language:
        language = DEFAULT_LANGUAGE
    return language

