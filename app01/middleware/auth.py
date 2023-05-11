from django.shortcuts import redirect


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 0.排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL
        accept_url = ['/login/', '/image/code/']
        if request.path_info in accept_url:
            return self.get_response(request)

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登录过，就可以继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            return self.get_response(request)

        # 2.没有登录过，重新回到登录页面
        return redirect("/login/")
