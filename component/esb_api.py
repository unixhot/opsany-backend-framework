# -*- coding: utf-8 -*-
"""
Copyright © 2012-2020 OpsAny. All Rights Reserved.
"""  # noqa
import re

import requests
import json

# forms.CharField
import settings
from config import APP_CODE, SECRET_KEY, BK_URL


class EsbApi(object):
    def __init__(self, token=None):
        self.token = token if token else ""
        self.app_code = APP_CODE
        self.app_secret = SECRET_KEY
        self.url = BK_URL
        self.headers = {
            "Cookie": "bk_token={}".format(self.token)
        }

    def get_nav_and_collection(self):
        API = "/api/c/compapi/workbench/get_nav_and_collection/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        dt = {}
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return dt

    def collection_nav(self, nav_id):
        API = "/api/c/compapi/workbench/post_collection/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "nav_id": nav_id
        }
        URL = self.url + API
        response = requests.post(url=URL, data=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            return end_data
        return None

    def get_user_message_info(self, current=1, pageSize=10):
        API = "/api/c/compapi/workbench/get_message_info/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "current": str(current),
            "pageSize": str(pageSize)
        }
        URL = self.url + API
        response = requests.post(url=URL, data=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            data = end_data.get("data")
            return data
        return None

    def get_user_info(self):
        API = "/api/c/compapi/v2/bk_login/get_user/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        dt = {}
        if end_data.get("result"):
            dt["phone"] = end_data.get("data").get("phone")
            dt["username"] = end_data.get("data").get("bk_username")
            dt["email"] = end_data.get("data").get("email")
            dt["ch_name"] = end_data.get("data").get("chname")
            dt["role"] = end_data.get("data").get("bk_role")
        return dt

    def get_user_menu(self):
        API = "/api/c/compapi/rbac/post_menu_tree/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "platform_cname": self.app_code,
        }
        URL = self.url + API
        response = requests.post(url=URL, data=json.dumps(req), headers=self.headers, verify=False)
        end_data = json.loads(response.text)

        return end_data.get("data")

    def guide(self, platform_code):
        API = "/api/c/compapi/workbench/guide/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "platform_code": platform_code
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        else:
            return end_data.get("response")

    def get_user_info_from_workbench(self):
        """从工作台ESB获取用户信息"""
        API = "/api/c/compapi/workbench/get_user_info_from_workbench/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
        }
        URL = self.url + API
        response = requests.post(url=URL, data=json.dumps(req), headers=self.headers, verify=False, timeout=2)
        end_data = json.loads(response.text)

        return end_data.get("data")

    def get_user_info_from_workbench_or_login(self):
        """首先获取工作台数据，获取不到再获取login数据"""
        try:
            end_data = self.get_user_info_from_workbench()
            if not end_data:
                raise Exception("workbench return None")
        except Exception as e:
            print("get_user_info_from_workbench_or_login_error_workbench:", e)
            default_user_icon = getattr(settings, "DEFAULT_USER_ICON",
                                        "uploads/workbench/user_icon/edfb99ee-08d6-41b8-ac5f-117fb86b0912.png")
            end_data = self.get_user_info()
            if end_data and isinstance(end_data, dict):
                end_data['icon_url'] = default_user_icon
        return end_data

    def get_language_theme_config(self, username):
        API = "/api/c/compapi/workbench/get_language_theme_config/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
            "user_token": self.token,
            "username": username,
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        dt = {}
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return dt

    def read_all_message(self):
        API = "/api/c/compapi/workbench/get_read_all_message/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token,
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        return end_data.get("data")

    def get_copyright_config(self):
        API = "/api/c/compapi/rbac/get_copyright_config/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        dt = {}
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return dt

    def get_user_group_sync(self):
        API = "/api/c/compapi/rbac/get_user_group_sync/"
        req = {
            "bk_app_code": self.app_code,
            "bk_app_secret": self.app_secret,
            "bk_username": "admin",
            "bk_token": self.token
        }
        URL = self.url + API
        response = requests.get(url=URL, params=req, headers=self.headers, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return {}

if __name__ == '__main__':
    # 业务：BUSINESS      应用：APPLICATION      服务：SERVICE

    esb_api_dev = EsbApi("dFbXGxYLiep-4TGkz7C2FUi_rqls_wXV5teKcKP9rmo")
    # esb_api_demo = EsbApi("bVKa2UyB7_5XmZACk8uGl4GvCpXmvPvh4pwZSH8oWaE")

    res1 = esb_api_dev.get_user_group_sync()
    print("res1", res1)
