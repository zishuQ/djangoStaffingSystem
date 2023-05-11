"""
自定义的分页组件

在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况筛选自己的数据
        queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html,        # 生成页码
        }

        return render(request, 'pretty_list.html', context)

在HTML页码中：

    {% for obj in queryset %}
        {{ obj.xx }}
    {% for obj in queryset %}

    <ul class="pagination">
        {{ page_string }}
    </ul>
"""

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/etty/list/?page=12
        :param plus: 显示当前页的前或后几页（页码）
        """

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        page = int(request.GET.get('page', 1))
        page_size = 10  # 每页显示10条数据
        start = (page - 1) * page_size
        end = page * page_size

        # 1.根据用户想要访问的页码，计算出起止位置
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()

        # 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    @property
    def html(self):
        # 计算出，显示当前页的前5页、后5页
        """
        if total_page_count <= 2 * plus:
            # 数据库中的数据比较少，都没有达到11页
            start_page = 1
            end_page = total_page_count
        else:
            # 数据库中的数据比较多，多于11页

            # 当前页少于5页时（小极值）
            if page <= plus:
                start_page = 1
                end_page = 2 * plus + 1
            else:
                # 当前页多于5页时
                # 当前页 + 5 > 总页码
                if page + plus > total_page_count:
                    start_page = total_page_count - 2 * plus
                    end_page = total_page_count
                else:
                    start_page = page - plus
                    end_page = page + plus
        """
        # 代码逻辑优化
        if self.total_page_count <= 2 * self.plus:
            start_page = 1
        else:
            start_page = max(1, self.page - self.plus)
            if start_page + 2 * self.plus >= self.total_page_count:
                start_page = self.total_page_count - 2 * self.plus
        end_page = min(self.total_page_count, start_page + 2 * self.plus)

        # 页码
        page_str_list = []

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">首页</a></li>')

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">上一页</a></li>'
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            else:
                ele = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nxt = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nxt = f'<li><a href="?{self.query_dict.urlencode()}">下一页</a></li>'
        page_str_list.append(nxt)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">尾页</a></li>')

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
                           type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
            """

        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string
