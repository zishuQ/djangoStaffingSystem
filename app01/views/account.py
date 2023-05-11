from io import BytesIO

from django.shortcuts import render, redirect, HttpResponse

from app01 import models
from app01.utils.form import LoginForm
from app01.utils.code import check_code


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取用户名和密码
        # 以字典形式获取 {'username': 'zishuQ', 'password': '7777'}

        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if user_input_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        # 去数据库校验用户名和密码是否正确，获取用户对象 / None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})

        # 用户名和密码正确
        # 网站生成随机字符串；写到用户浏览器的cookie中；再写入到session中
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        # session可以保存7天
        request.session.pop('image_code')
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect("/admin/list/")

    return render(request, "login.html", {"form": form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()
    return redirect("/login/")
