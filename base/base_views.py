import json

from django.http import JsonResponse

from component.base_views import BaseView
from component.status_code import success, SuccessStatusCode, error, ErrorStatusCode
from base import get_user_query_from_cookie
from base.models import UserInfo
from component.esb_api import EsbApi


class DeployMenuStrategyCtrl(BaseView):
    # @user_sync
    def get(self, request):
        """ 获取当前平台使用者的菜单列表 """
        token = request.COOKIES.get("bk_token")
        esb_obj = EsbApi(token)
        res_data = esb_obj.get_user_menu()  # 调用ESB接口获取到当前用户的在资源平台的菜单列表
        return JsonResponse(success(SuccessStatusCode.MENU_GET_SUCCESS, res_data[0] if res_data else {}, language=self.ops_language()))


class GuideCtrl(BaseView):
    def get(self, request):
        """ 获取当前平台使用指南"""
        token = request.COOKIES.get("bk_token")
        platform_code = request.GET.get("platform_code", "")
        if not platform_code:
            return JsonResponse(error(ErrorStatusCode.MUST_INPUT_MESSAGE, language=self.ops_language()))
        esb_obj = EsbApi(token)
        res_data = esb_obj.guide(platform_code)
        return JsonResponse(res_data, safe=False)


# 获取当前用户信息
class GetUserInfoCtrl(BaseView):

    # @user_sync
    def get(self, request):
        """
        获取当前用户信息
        """
        token = request.COOKIES.get("bk_token")
        user_query = get_user_query_from_cookie(request)
        if not user_query:
            UpdateDirectorView()._update_director(request)
            user_query = get_user_query_from_cookie(request)
        if not user_query:
            return JsonResponse(error(ErrorStatusCode.NOT_HAVE_USER_INFO, language=self.ops_language()))
        data = user_query.to_user_info_dict()
        language_theme_config = EsbApi(token).get_language_theme_config(user_query.username)
        data.update(language_theme_config)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data, language=self.ops_language()))


# 获取用户搜藏信息
class GetNavCollectionView(BaseView):
    """
    获取用户搜藏信息
    """

    def get(self, request):
        token = request.COOKIES.get("bk_token")
        end_data = EsbApi(token).get_nav_and_collection()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data, language=self.ops_language()))


# 用户搜藏
class CollectionNavView(BaseView):
    """
    用户搜藏
    """

    def post(self, request):
        token = request.COOKIES.get("bk_token")
        data = json.loads(request.body)
        nav_id = data.get("nav_id")
        end_data = EsbApi(token).collection_nav(nav_id)
        if isinstance(end_data, dict):
            successcode = end_data.pop("api_code")
            return JsonResponse({"code": 200, "successcode": successcode, "message": end_data.get("message"),
                                 "data": end_data.get("data")
                                 })
        else:
            return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN, language=self.ops_language()))


# 获取用户站内信
class GetUserMessageView(BaseView):
    """
    获取用户站内信
    """

    def get(self, request):
        kwargs = request.GET.dict()
        page = int(kwargs.pop("current", 1))
        per_page = int(kwargs.pop("pageSize", 10))
        token = request.COOKIES.get("bk_token")
        data = EsbApi(token).get_user_message_info(page, per_page)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data, language=self.ops_language()))


# 全部已读站内信
class ReadAllMessageView(BaseView):
    """全部已读站内信"""

    def get(self, request):
        bk_token = request.COOKIES.get("bk_token")
        res = EsbApi(bk_token).read_all_message()
        return JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS, res, language=self.ops_language()))


class CopyrightConfigView(BaseView):
    def get(self, request):
        """
        底部版权信息
        """
        token = request.COOKIES.get("bk_token")
        end_data = EsbApi(token).get_copyright_config()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data, language=self.ops_language()))


class HomePageView(BaseView):
    def get(self, request):
        dic = {}
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, dic, language=self.ops_language()))


class HomePageLeftView(BaseView):
    def get(self, request):
        """
        概览页左侧最近查看和最近参与
        :param request:
        :return:
        """
        data = request.GET.dict()
        dic = {}
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, dic, language=self.ops_language()))


class UpdateDirectorView(BaseView):
    def get(self, request):
        return self._get_or_post(request)

    def post(self, request):
        return self._get_or_post(request)

    def _get_or_post(self, request):
        status, message = self._update_director(request)
        if not status:
            return JsonResponse(error(ErrorStatusCode.CUSTOM_ERROR, custom_message="没有拉取到用户信息", language=self.ops_language()))
        return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS, language=self.ops_language()))

    def _update_director(self, request):
        # all_user_list = esb.get_all_users()
        token = request.COOKIES.get("bk_token")
        esb = EsbApi(token=token)
        all_user_list = esb.get_user_group_sync()
        user_list = all_user_list.get("user_list", []) or []
        if not user_list:
            return False, "没有拉取到用户信息"

        temp_user_list = []
        for each_user in user_list:
            used_field = {}
            used_field["phone"] = each_user.get("phone")
            used_field["username"] = each_user.get("username")
            used_field["email"] = each_user.get("email")
            used_field["ch_name"] = each_user.get("chname")
            used_field["role"] = each_user.get("bk_role")
            # if not UserInfo.objects.filter(username=each_user["bk_username"]).count():
            obj_user = UserInfo.fetch_one(username=each_user["username"])
            if not obj_user:
                obj_user = UserInfo.objects.create(**used_field)
            else:
                obj_user.update(**used_field)
                # obj_user = UserInfo.objects.select_for_update().filter(username=each_user["bk_username"])
                # with transaction.atomic():

            temp_user_list.append(used_field["username"])
        local_all_users = UserInfo.objects.all()
        deleted_user_list = []
        for each in local_all_users:
            if each.username not in temp_user_list:
                deleted_user_list.append(each.username)
        UserInfo.objects.filter(username__in=deleted_user_list).update(is_activate=False)
        return True, "Success"



