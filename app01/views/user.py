from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


# Create your views here.


def user_list(request):
    """ 用户管理 """
    # 获取所有用户的列表 [obj,obj,obj]
    queryset = models.UserInfo.objects.all()
    """
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(),
              obj.depart_id, obj.depart.title)
        # obj.depart_id   # 获取数据库中存储的那个字段值
        # obj.depart.title    # 根据id自动去关联的表中获取哪一行数据depart对象
    """

    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html,
    }
    return render(request, "user_list.html", context)


def user_add(request):
    """ 添加用户（原始方式） """
    if request.method == "GET":
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    # 获取用户提交的数据
    name = request.POST.get("user")
    password = request.POST.get("pwd")
    age = request.POST.get("age")
    account = request.POST.get("ac")
    create_time = request.POST.get("ctime")
    gender = request.POST.get("gender_id")
    depart_id = request.POST.get("dp")

    # 添加到数据库中
    models.UserInfo.objects.create(name=name, password=password, age=age, account=account, create_time=create_time,
                                   gender=gender, depart_id=depart_id)
    # 返回到用户列表页面
    return redirect("/user/list/")


def user_model_form_add(request):
    """ 添加用户（ModelForm版本） """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '1', 'password': '1', 'age': 1, 'account': Decimal('1'), 'create_time': datetime.datetime(2021, 3, 5, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'depart': <Department: 新媒体>}
        # print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_model_form_add.html', {"form": form})


def user_edit(request, nid):
    """ 编辑用户 """
    row_obj = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = UserModelForm(instance=row_obj)
        return render(request, "user_edit.html", {"form": form})

    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一些值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """ 删除用户 """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
