def first_error_message(form):
    error_data = form.errors.as_data()
    error_data_list = list(error_data.items())
    if not error_data_list:
        return "Form Error"
    error_message = error_data_list[0][1][0].message
    message = "{}".format(error_message)
    return message

def get_user_query_from_cookie(request):
    from base.models import UserInfo
    bk_token_username = request.COOKIES.get("bk_token_username")
    return UserInfo.fetch_one(username=bk_token_username)