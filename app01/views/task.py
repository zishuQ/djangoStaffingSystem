import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.form import TaskModelForm
from app01.utils.pagination import Pagination



def task_list(request):
    """ 任务列表 """
    # 去数据库获取所有的任务
    queryset = models.Task.objects.all()
    form = TaskModelForm()
    page_object = Pagination(request, queryset)

    context = {
        "form": form,
        "queryset": page_object.page_queryset,
        "page_string": page_object.html,
    }
    return render(request, "task_list.html", context)


@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [1, 2, 3, 4]}
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    """ 添加任务 """
    print(request.POST)
    # {'level': ['3'], 'title': ['测试'], 'detail': ['测试信息'], 'user': ['1']}

    # 1. 用户发送过来的数据进行校验（ModelForm进行校验）
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))