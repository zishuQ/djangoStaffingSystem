from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import UpModelForm


def city_list(request):
    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})


def city_add(request):
    """ 上传文件和数据（ModelForm）"""
    title = "新建城市"

    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_form.html', {"form": form, "title": title})
