from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app01.utils.pagination import Pagination


def admin_list(request):
    """ 管理员列表 """

    # 构造搜索条件
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html,
        "search_data": search_data,
    }

    return render(request, "admin_list.html", context)


def admin_add(request):
    """ 添加管理员 """
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})


def admin_edit(request, nid):
    """ 编辑管理员 """

    # 对象 / None
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return render(request, "error.html", {"msg": "数据不存在"})

    title = "编辑管理员"

    if request.method == "GET":
        form = AdminEditModelForm(instance=row_obj)
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")

    return render(request, "change.html", {"form": form, "title": title})


def admin_delete(request, nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    """ 重置密码 """
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect("/admin/list")

    title = f"重置密码 - {row_obj.username}"
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})