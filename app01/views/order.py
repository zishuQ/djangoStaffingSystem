import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.form import OrderModelForm
from app01.utils.pagination import Pagination


def order_list(request):
    """ 订单列表 """
    queryset = models.Order.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)
    form = OrderModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html,
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 新建订单（Ajax请求） """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 额外增加一些不是用户输入的值（自己计算出来）
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(10000, 99999))

        # 固定设置管理员ID
        form.instance.admin_id = request.session["info"]["id"]

        # 保存到数据库
        form.save()
        # return HttpResponse(json.dumps({"status": True})
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
