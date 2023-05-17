from django.shortcuts import render, redirect


def upload_list(request):
    if request.method == "GET":
        return render(request, 'upload_list.html')

    # # 'username': ['img11']
    # print(request.POST)
    # # 'avatar': [<InMemoryUploadedFile: 头像.jpg (image/jpeg)>]
    # print(request.FILES)

    file_object = request.FILES.get("avatar")

    f = open( file_object.name, mode='wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return redirect('/upload/list/')
