from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import PrettyModelForm, PrettyEditModelForm
from app01.utils.pagination import Pagination


# Create your views here.


def pretty_list(request):
    """ 靓号列表 """

    data_dict = {}
    search_data = request.GET.get('q')
    if search_data:
        data_dict["mobile__contains"] = search_data

    # select * from 表 order by level desc;
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html,  # 生成页码
    }

    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """ 新建靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    # 用户POST提交数据，数据校验
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect("/pretty/list/")

    # 校验失败（在页面上显示错误信息）
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_obj = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect(f'/pretty/list/')
