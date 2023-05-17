import random
from datetime import datetime

import requests
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


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    print(uid)
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "删除失败：数据不存在"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据ID获取订单详细 """
    uid = request.GET.get('uid')
    # 从数据库中获取到一个字典 row_dict
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "数据不存在"})

    return JsonResponse({"status": True, "data": row_dict})


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tip": "数据不存在，请刷新重试"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})