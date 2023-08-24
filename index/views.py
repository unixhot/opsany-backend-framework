from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from blueapps.account.decorators import login_exempt


@login_exempt
def vue(request):
    # return render(request, 'index.html')
    try:
        return render(request, 'index.html', settings.SITE_URL)
    except:
        return render(request, 'index.html')


@login_exempt
def healthz(request):
    from base.models import UserInfo
    code = 1
    status = "OK"
    message = ""
    dic = {
        "check_mysql": True,
        "check_superuser": True,
    }
    if not UserInfo.objects.filter():  # 校验用户初始化
        dic["check_superuser"] = False
        code, status = 0, "ERROR"
        message += "用户初始化失败 "
    
    if not message:
        message = "Success"
    if code == 1:
        data = {"code": code, "status": status, "message": message, "details": dic}
        return JsonResponse(data)
    else:
        data = message
        return HttpResponse(content=data, status=500)