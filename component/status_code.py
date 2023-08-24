# -*- coding: utf-8 -*-
"""
Copyright © 2012-2020 OpsAny. All Rights Reserved.
"""  # noqa

from enum import Enum
from component.return_message import *

from config import DEFAULT_LANGUAGE


class ErrorStatusCode(Enum):
    # code = 400
    INVALID_REQUEST = (400, 40000, INVALID_REQUEST_MESSAGE)

    # code = 401
    INVALID_TOKEN = (401, 40100, INVALID_TOKEN_MESSAGE)
    NOT_HAVE_USER_INFO = (401, 40102, NOT_HAVE_USER_INFO_MESSAGE)
    TOOL_AUTH_ERROR_DEPLOY = (401, 40103, TOOL_AUTH_ERROR_DEPLOY_MESSAGE)

    # code = 403

    # code = 404
    DATA_NOT_EXISTED = (404, 40400, DATA_NOT_EXISTED_MESSAGE)
    KBASE_NOT_FOUND = (404, 40409, KBASE_NOT_FOUND_MESSAGE)
    KBASE_ARTICLE_NOT_EXIST_ERROR = (404, 40410, KBASE_ARTICLE_NOT_EXIST_ERROR_MESSAGE)
    KBASE_FOLDER_NOT_EXIST_ERROR = (404, 40410, KBASE_FOLDER_NOT_EXIST_ERROR_MESSAGE)
    KBASE_COMMENT_NOT_EXIST_ERROR = (404, 40410, KBASE_COMMENT_NOT_EXIST_ERROR_MESSAGE)


    # code = 422
    MUST_INPUT_MESSAGE = (422, 42201, MUST_INPUT_MESSAGE_MESSAGE)
    OPERATION_ERROR = (422, 42202, SERVER_ERROR_MESSAGE)
    ICON_TYPE_ERROR = (422, 42203, UPLOAD_ICON_TYPE_ERROR_MESSAGE)



    REPOSITORY_ASSET_NOT_UPLOAD = (422, 42204, REPOSITORY_ASSET_NOT_UPLOAD_MESSAGE)
    PORT_MUST_UNIQUE = (422, 42205, PORT_MUST_UNIQUE_MESSAGE)
    REPO_NOT_UPDATE = (422, 42206, REPO_NOT_UPDATE_MESSAGE)
    DELETE_ICON_KBASE_USE_ERROR = (422, 42207, DELETE_ICON_KBASE_USE_ERROR_MESSAGE)

    CUSTOM_ERROR = (422, 42208, CUSTOM_ERROR_MESSAGE)
    GITLAB_CONNECTION_ERROR = (422, 42209, GITLAB_CONNECTION_ERROR_MESSAGE)
    NAME_HAS_EXISTED2_MESSAGE = (422, 42210, NAME_HAS_EXISTED2_MESSAGE)
    PERMISSION_DENIED = (422, 42211, PERMISSION_DENIED_MESSAGE)
    BUILT_IN_NOT_OPERATION = (422, 42212, BUILT_IN_NOT_OPERATION_MESSAGE)
    PARAMETER_MISSING_ERROR = (422, 42213, PARAMETER_MISSING_ERROR_MESSAGE)
    KBASE_ARTICLE_FOLDER_HAS_FOLDER_ERROR = (422, 42214, KBASE_ARTICLE_FOLDER_HAS_FOLDER_ERROR_MESSAGE)
    KBASE_ARTICLE_FOLDER_HAS_ARTICLE_ERROR = (422, 42215, KBASE_ARTICLE_FOLDER_HAS_ARTICLE_ERROR_MESSAGE)
    KBASE_TITLE_EXIST_ERROR = (422, 42216, KBASE_TITLE_EXIST_ERROR_MESSAGE)
    KBASE_MOVE_OWNER_MUST_MEMBER_ERROR = (422, 42217, KBASE_MOVE_OWNER_MUST_MEMBER_ERROR_MESSAGE)
    KBASE_FOLDER_NAME_ERROR = (422, 42218, KBASE_FOLDER_NAME_ERROR_MESSAGE)
    KBASE_CONTENT_REQUIRED_ERROR = (422, 42219, KBASE_CONTENT_REQUIRED_ERROR_MESSAGE)
    DELETE_ERROR = (422, 42220, DELETE_ERROR_MESSAGE)
    PARAMETER_ERROR = (422, 42221, PARAMETER_ERROR_MESSAGE)

    # code 500
    SERVER_ERROR = (500, 50000, OPERATION_ERROR_MESSAGE)

    # code 502
    GITLAB_SERVER_ERROR = (502, 502003, GITLAB_SERVER_ERROR_MESSAGE)


def error(error_info=ErrorStatusCode.INVALID_REQUEST, errors=None, custom_message=None, language=DEFAULT_LANGUAGE):
    http_code, error_code, error_msg = error_info.value
    params = {
        'code': http_code,
        'message': get_language_message(error_msg, language),
        'errcode': error_code,
    }
    if errors:
        params['errors'] = errors
    if custom_message:
        params['message'] = get_language_message(custom_message, language)
    return params


class SuccessStatusCode(Enum):
    # code = 200
    # 测试使用
    TEST_SUCCESS = (200, 20000, SERVER_LINK_SUCCESS_MESSAGE)

    # 模型组部分 04 - 07
    MESSAGE_CREATE_SUCCESS = (200, 20001, MESSAGE_CREATE_SUCCESS_MESSAGE)
    MESSAGE_GET_SUCCESS = (200, 20002, MESSAGE_GET_SUCCESS_MESSAGE)
    MESSAGE_DELETE_SUCCESS = (200, 20003, MESSAGE_DELETE_SUCCESS_MESSAGE)
    MESSAGE_RECYCLE_BIN_SUCCESS = (200, 20004, MESSAGE_RECYCLE_BIN_SUCCESS_MESSAGE)
    MESSAGE_RECYCLE_BIN_OUT_SUCCESS = (200, 20005, MESSAGE_RECYCLE_BIN_OUT_SUCCESS_MESSAGE)
    MESSAGE_UPDATE_SUCCESS = (200, 20006, MESSAGE_UPDATE_SUCCESS_MESSAGE)

    MENU_GET_SUCCESS = (200, 20007, MENU_GET_SUCCESS_MESSAGE)
    OPERATION_SUCCESS = (200, 20008, OPERATION_SUCCESS_MESSAGE)

    DEPLOY_TASK_RUN_SUCCESS = (200, 20009, JOB_BUILD_SUCCESS_MESSAGE)
    DEPLOY_TASK_CANCEL_SUCCESS = (200, 20010, DEPLOY_TASK_CANCEL_SUCCESS_MESSAGE)
    UPLOAD_SUCCESS = (200, 20011, UPLOAD_SUCCESS_MESSAGE)


def success(success_info=SuccessStatusCode.TEST_SUCCESS, data=None, message=None, add_fields=None, language=DEFAULT_LANGUAGE):
    http_code, success_code, success_msg = success_info.value
    params = {
        'code': http_code,
        'successcode': success_code,
        'message': get_language_message(success_msg, language=language),
    }
    if isinstance(add_fields, dict):
        params.update(add_fields)
    if message:
        params["message"] = get_language_message(message, language)
    if data is not None: params['data'] = data
    return params


def get_language_message(message, language):
    try:
        message = eval(message)
    except Exception:
        pass
    if isinstance(message, dict):
        if "chinese_simplified" not in message.keys():
            msg = str(message)
        else:
            format_str = message.pop("format_str", "")
            msg = message.get(language) or message.get(DEFAULT_LANGUAGE, "!")
            if format_str:
                msg = msg.format(format_str)
    else:
        msg = str(message)
    return msg
