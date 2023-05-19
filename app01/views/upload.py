import os

from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import UpForm, UpModelForm


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')

    # print(request.POST)
    # # 'username': ['img11']
    # print(request.FILES)
    # # 'avatar': [<InMemoryUploadedFile: 头像.jpg (image/jpeg)>]
    file_object = request.FILES.get("avatar")

    with open(file_object.name, mode='wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)

    return redirect('/upload/list/')


def upload_form(request):
    """ 基于Form组件实现的文件上传 """
    title = "Form上传"
    if request.method == "GET":
        form = UpForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 1.读取图片内容，写入到文件夹中并获取文件的路径
        image_object = form.cleaned_data.get("img")

        # Linux系统和 Windows系统的分隔符不一样，因此用
        # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
        media_path = os.path.join("media", image_object.name)

        with open(media_path, mode='wb') as f:
            for chunk in image_object.chunks():
                f.write(chunk)

        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path,
        )

        return redirect('/upload/form/')
    return render(request, 'upload_form.html', {"form": form, "title": title})


def upload_modelform(request):
    """ 上传文件和数据（ModelForm）"""
    title = "ModelForm上传文件"
    if request.method == "GET":
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form": form, "title": title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对于文件：自动保存
        # 字段 + 上传路径写入到数据库
        form.save()
        return redirect('/upload/modelform/')
    return render(request, 'upload_form.html', {"form": form, "title": title})
