<<<<<<< HEAD
# djangoStaffingSystem
=======
# Django开发

主题：员工管理系统

# 1. 新建项目

# 2. 创建app

```python
python manage.py startapp app01
```

注册app：

![Untitled](Django%E5%BC%80%E5%8F%91%208019142fa1db48cbb4763f78f598a35c/Untitled.png)

# 3. 设计表结构

| id | title |
| --- | --- |
| 1 | 开发 |
| 2 | 客服 |
| 3 | 销售 |

| id | name | passwordd | age | account | create_time | depart_id |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | zishuQ | 7777 | 20 | 1000000 | 2021/9/4 | 1 |
| 2 | aaa | 7777 | 18 | 10000 | 2021/9/3 | 1 |
| 3 | bbb | 7777 | 19 | 10000 | 2021/9/3 | 2 |
| 4 | ccc | 7777 | 20 | 10000 | 2021/9/3 | 2 |
| 5 | ddd | 7777 | 21 | 10000 | 2021/9/3 | 3 |
| 6 | eee | 7777 | 22 | 10000 | 2021/9/4 | 3 |
- 用户表存储名称？ID？
ID，数据库范式（理论知识），常见开发都是这样【节省存储开销】
名称，特别大的公司。查询的次数非常多，连表操作比较耗时【加速查找，允许数据冗余】
- 部门ID需不需要约束？
只能是部门表中已存在ID
- 部门被删除，关联的用户
- 删除用户，级联删除
- 部门ID列置空

【models.pymodels.py】

```python
from django.db import models

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)

class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 1.有约束
    #   - to，与哪张表关联
    #   - to_field，表中的那一列关联
    # 2.django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
```

# 4. 在MySQL中生成表

- 工具连接MySQL生成数据库

```sql
create database staffing_system DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

- 修改配置文件，连接MySQL【settings.py】

```sql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'staffing_system',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
```

- django命令生成数据库表

# 5. 静态文件管理

app01目录下新建

- static
    - css
    - img
    - js
    - plugins
- templates

# 6. 部门管理

> 体验，最原始方法来做
Django中提供Form和ModelForm组件（方便）
> 

## 6.1 部门列表

![Untitled](Django%E5%BC%80%E5%8F%91%208019142fa1db48cbb4763f78f598a35c/Untitled%201.png)

## 6.2  添加部门

- depart_list.html
href 跳转到 **/depart/add/**

![Untitled](Django%E5%BC%80%E5%8F%91%208019142fa1db48cbb4763f78f598a35c/Untitled%202.png)

- urls.py

```python
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
]
```

- views.py

```python
def depart_add(request):
    """ 添加部门 """
    return render(request, "depart_add.html")
```

- depart_add.html

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="{% static 'plugins/bootstrap-3.4.1-dist/css/bootstrap.min.css' %}">
    <style>
        .navbar {
            border-radius: 0;
        }
    </style>
</head>
<body>
<nav class="navbar navbar-default">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"
                    data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#"> 用户管理系统 </a>
        </div>

        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
                <li><a href="/depart/list/">部门管理</a></li>
                <li><a href="#">Link</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                <li><a href="#">登录</a></li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true"
                       aria-expanded="false">Dropdown <span class="caret"></span></a>
                    <ul class="dropdown-menu">
                        <li><a href="#">个人资料</a></li>
                        <li><a href="#">我的信息</a></li>
                        <li><a href="#">Something else here</a></li>
                        <li role="separator" class="divider"></li>
                        <li><a href="#">注销</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>

<div>
    <div class="container">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">新建部门</h3>
            </div>
            <div class="panel-body">
                <form class="form-horizontal">
                    <div class="form-group">
                        <label>标题</label>
                        <input type="text" class="form-control" placeholder="标题" name="title"/>
                    </div>

                    <button type="submit" class="btn btn-primary">提 交</button>
                </form>
            </div>
        </div>
    </div>
</div>

<script src="{% static 'js/jquery-3.6.0.min.js' %}"></script>
<script src="{% static 'plugins/bootstrap-3.4.1-dist/js/bootstrap.min.js' %}"></script>
</body>
</html>
```

## 6.3 删除部门

## 6.4 编辑部门

- depart_list.html

![Untitled](Django%E5%BC%80%E5%8F%91%208019142fa1db48cbb4763f78f598a35c/Untitled%203.png)

- urls.py

```python
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),

    # http://127.0.0.1:8000/depart/10/edit/
    # http://127.0.0.1:8000/depart/1/edit/
    # http://127.0.0.1:8000/depart/2/edit/
    path('depart/<int:nid>/edit/', views.depart_edit)   # django 3的新特性，之前是要用正则表达式的
]
```

- views.py

```python
def depart_edit(request, nid):
    """ 修改部门 """
    if request.method == "GET":
        # 根据nid，获取他的数据
        row_obj = models.Department.objects.filter(id=nid).first()

        return render(request, "depart_edit.html", {"row_obj": row_obj})

    # 获取用户提交的标题
    title = request.POST.get("title")

    # 根据ID找到数据库中的数据并进行更新
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回部门列表
    return redirect("/depart/list/")
```

# 7. 模板的继承

- 部门列表
- 添加部门
- 编辑部门

定义模板：`layout.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
		<link rel="stylesheet" href="{% static 'plugin...min.css' %}">		<link rel="stylesheet" href="{% static 'plugin...min.css' %}">
		{% block js%}{% endblock %}
</head>
<body>
		<h1>标题</h1>
		<div>
		    {% block content %}{% endblock %}
		</div>
		<h1>底部</h1>

		<script src="{% static 'js/jquery-3.6.0.min.js' %}"></script>
		{% block js%}{% endblock %}
</body>
</html>
```

继承模板：

```html
{% extends "layout.html" %}

{% block css %}
		<link rel="stylesheet" href="{% static 'plugin...min.css' %}">
		<style>
				...
		</style>
{% endblock %}

{% block content %}
    <h1>首页</h1>
{% endblock %}

{% block js %}
    <script src="{% static js/jqxxxin.js %}"></script>
{% endblock %}
```

# 8. 用户管理

```sql
insert into app01_userinfo(name,password,age,account,create_time,gender,depart_id) values("zishuQ","777",20,300000.68,"2021-09-04",1,1);

insert into app01_userinfo(name,password,age,account,create_time,gender,depart_id) values("小明","777",22,34300.68,"2020-10-26",1,4);

insert into app01_userinfo(name,password,age,account,create_time,gender,depart_id) values("小红","777",19,10.55,"2022-09-04",1,1);
```

```html
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| id          | bigint(20)    | NO   | PRI | NULL    | auto_increment |
| name        | varchar(16)   | NO   |     | NULL    |                |
| password    | varchar(64)   | NO   |     | NULL    |                |
| age         | int(11)       | NO   |     | NULL    |                |
| account     | decimal(10,2) | NO   |     | NULL    |                |
| create_time | datetime(6)   | NO   |     | NULL    |                |
| gender      | smallint(6)   | NO   |     | NULL    |                |
| depart_id   | bigint(20)    | NO   | MUL | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+----+

```

- 原始方式理思路：不会采用（本质）【麻烦】
    - 用户提交数据没有校验
    - 错误，页面上应该有错误提示
    - 页面上，每一个字段都需要我们重新写一遍
    - 关联的数据，手动去获取并展示循环显示在页面
- Django组件
    - Form组件（简便）
    - ModelForm组件（最简便）

## 8.1 初始Form

### 1. views.py

```python
class MyForm(Form):
    user = forms.CharField(widget=forms.Input)
    pwd = forms.CharField(widget=forms.Input)
    email = forms.CharField(widget=forms.Input)

def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return render(request, 'user_add.html', {"form": form})
```

### 2. user_add.html

```html
<form method="post">
    {% for field in form %}
		    {{ field }}
    {% endfor %}
    <!-- <input type="text" placeholder="姓名" name="user"/> -->
</form>
```

```html
<form method="post">
    {{ form.user }}
    {{ form.pwd }}
    {{ form.email }}
    <!-- <input type="text" placeholder="姓名" name="user"/> -->
</form>
```

## 8.2 ModelForm（推荐）

### 0. models.py

```python
class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
```

### 1. views.py

```python
class MyForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ["name", "password", "age"]

def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return render(request, 'user_add.html', {"form": form})
```

### 2. user_add.html

```html
<form method="post">
    {% for field in form %}
		    {{ field }}
    {% endfor %}
    <!-- <input type="text" placeholder="姓名" name="user"/> -->
</form>
```

```html
<form method="post">
    {{ form.user }}
    {{ form.pwd }}
    {{ form.email }}
    <!-- <input type="text" placeholder="姓名" name="user"/> -->
</form>
```

## 8.4 编辑用户

- 点击编辑，跳转到编辑页面（将编辑行的ID携带过去）
- 编辑页面（默认数据，根据ID获取并设置到页面中）
- 提交：
    - 错误提示
    - 数据校验
    - 在数据库更新
    
    ```python
    models.UserInfo.filter(id=4).update(...)
    ```
    

## 8.5 删除用户

- urls.py

```python
path('/list/<int:nid>/delete/', views.list_delete)
```

- views.py

```python
def list_delete(request, nid):
		models.UserInfo.objects.filter(id=nid).delete()
		return redirect('/user/list/')
```

# 9. 靓号管理

## 9.1 表结构

| id | mobile | price | level(choices) | status |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
- level：级别，类似于性别
- status：1未占用/2已占用

根据表结构的需求，在models.py中创建类（由类生成数据库中的表）

```python
class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    states_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    states = models.SmallIntegerField(verbose_name="状态", choices=states_choices, default=2)
```

在数据库模拟创建一些数据：

```sql
insert into app01_prettynum(mobile, price, level, status)values("1111111111", 19, 1, 1);
```

```sql
mysql> select * from app01_prettynum;
+----+------------+-------+-------+--------+
| id | mobile     | price | level | status |
+----+------------+-------+-------+--------+
|  1 | 1111111111 |    19 |     1 |      1 |
|  2 | 1111111111 |    19 |     1 |      1 |
|  3 | 1111111111 |    19 |     1 |      1 |
|  4 | 1111111111 |    19 |     1 |      1 |
+----+------------+-------+-------+--------+
4 rows in set (0.00 sec) 
```

## 9.2 靓号列表

- URL
- 函数
    - 获取所有的靓号
    - 结合html+render将靓号罗列出来
    
    ```sql
    id  号码  价格  级别（中文）  状态（中文）
    ```
    

## 9.3 新建靓号

- 列表点击跳转 `/pretty/add/`
- URL
- ModelForm类

```python
from django import forms

class PrettyModelForm(forms.ModelForm):
		...
```

- 函数
    - 实例化类的对象
    - 通过render将对象传入到HTML中
    - 模板的循环展示所有的字段
- 点击提交
    - 数据校验
    - 保存到数据库
    - 跳转回靓号列表
    
    验证：方式1 --- 字段 + 正则
    
    ```python
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误'), ],
    )
    ```
    
    验证：方式2 --- 钩子方法
    
    ```python
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
    
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
    
        # 验证通过，用户输入的值返回
        return txt_mobile
    ```
    

## 9.4 编辑靓号

- 列表页面：/pretty/数字/edit/
- URL
- 函数
    - 根据ID获取当前编辑的对象
    - ModelForm配合，默认显示数据
    - 提交数据

### 不允许手机号重复

- 添加：【正则表达式】【手机号不能存在】
    
    ```python
    # [obj, obj, obj]
    queryset = models.PrettyNum.objects.filter(mobile="18888888888")
    
    obj = models.PrettyNum.objects.filter(mobile="18888888888").first()
    
    # True/False
    exists = models.PrettyNum.objects.filter(mobile="18888888888").exists()
    ```
    
- 编辑：【正则表达式】【手机号不能存在】
    
    ```python
    排除自己以外，其他的数据是否手机号是否重复？
    
    # id!=2 and mobile='18888888888'
    models.PrettyNum.objects.filter(mobile='18888888888').exclude(id=2) 
    ```
    

## 9.5 搜索手机号

```python
models.PrettyNum.objects.filter(mobile='18888888888',id=12)

data_dict = {"mobile":"18888888888","id":12)
models.Pretty.objects.filter(**data_dict)
```

- 数字的比较

```python
models.PrettyNum.objects.filter(id=12)       # 等于12
models.PrettyNum.objects.filter(id__gt=12)   # 大于12
models.PrettyNum.objects.filter(id__gte=12)  # 大于等于12
models.PrettyNum.objects.filter(id__lt=12)   # 小于12
models.PrettyNum.objects.filter(id__lte=12)  # 小于等于12
```

- 字符串的比较

```python
models.PrettyNum.objects.filter(mobile__='1888')            # 等于
models.PrettyNum.objects.filter(mobile__startswith='1888')  # 筛选出以1888开头
models.PrettyNum.objects.filter(mobile__endswith='1888')    # 筛选出以1888结尾
models.PrettyNum.objects.filter(mobile__contains='1888')    # 筛选出包含1888
```

## 9.6 分页

```python
queryset = models.PrettyNum.objects.all()

queryset = models.PrettyNum.objects.filter)id=1)[0:10]

# 第1页
queryset = models.PrettyNum.objects.all()[0:10]

# 第2页
queryset = models.PrettyNum.objects.all()[10:20]

# 第3页
queryset = models.PrettyNum.objects.all()[20:30]
```

```python
data = models.PrettyNum.objects.all()

data = models.PrettyNum.objects.filter(id=2)
```

- 分页的逻辑和处理规则
- 封装分页类
    - 从头到尾开发
    - 写项目用【pagination.py】公共组件

- 小Bug，搜索 + 分页的情况下

```python
分页时候，保留原来的搜索条件

http://127.0.0.1:8000/pretty/list/?q=888
http://127.0.0.1:8000/pretty/list/?page=1

http://127.0.0.1:8000/pretty/list/?q=888&page=23
```

# 10. 时间插件

# 11. ModelForm和BootStrap

- ModelForm可以帮助我们生成HTML标签

```python
class UserModelForm(forms.ModelForm):
		class Meta:
				model = models.UserInfo
				fields = ["name", "password"]

form = UserModelForm()
```

```python
{{ form.name }}      # 普通的input框
{{ form.password }}  # 普通的input框
```

- 定义插件

```python
class userModelForm(forms.ModelForm):
		class Meta:
				model = models.UserInfo
				fields = ["name", "password"]
				widgets = {
						"name": forms.TextInput(attrs={"class": "form-control"}),
						"password": forms.PasswordInput(attrs={"class": "form-control"}),
						"age": forms.TextInput(attrs={"class": "form-control"}),
				}

form = UserModelForm()
```

```python
class UserModelForm(forms.ModelForm):
    name = forms.CharField(
				min_length=3,
				label="用户名",
				widget=forms.TextInput(attrs={"class": "form-control"})
		)

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age"]
```

```python
{{ form.name }}      # BootStrap的input框
{{ form.password }}  # BootStrap的input框
```

- 重新定义的init方法，批量设置

```python
class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age"]

		def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)
			
				# 循环ModelForm中的所有字段，给每个字段的插件设置
				for name, field in self.fields.items():
						field.widget.attrs = {
								"class": "form-control",
								"placeholder": field.label,
						}
```

```python
class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age"]

		def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)
			
				# 循环ModelForm中的所有字段，给每个字段的插件设置
				for name, field in self.fields.items():

						# 字段中又属性，保留原来的属性，没有属性，才增加
						if field.widget.attrs:
								field.widget.attrs["class"] = "form-control"
								field.widget.attrs["placeholder"] = field.label
						else:
								field.widget.attrs = {
										"class": "form-control",
										"placeholder": field.label,
								}
```

- 自定义类

```python
class BootstrapModelForm(forms.ModelForm):
		def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)
				# 循环ModelForm中的所有字段，给每个字段的插件设置
				for name, field in self.fields.items():
						# 字段中又属性，保留原来的属性，没有属性，才增加
						if field.widget.attrs:
								field.widget.attrs["class"] = "form-control"
								field.widget.attrs["placeholder"] = field.label
						else:
								field.widget.attrs = {
										"class": "form-control",
										"placeholder": field.label,
								}
```

```python
class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age"]
```

# 12. 管理员操作

| id | username | password |
| --- | --- | --- |
|  |  |  |
|  |  |  |

# 13. 用户登录

- 无状态 & 短连接

![Untitled](Django%E5%BC%80%E5%8F%91%208019142fa1db48cbb4763f78f598a35c/Untitled%204.png)

什么是cookie和session？

```python
http://127.0.0.1:8000/admin/list/
https://127.0.0.1:8000/admin/list/
```

- cookie：保存在浏览器上的键值对
发送请求时，自动携带
- Session：保存在（数据库、redis、文件）中的验证信息

![Untitled](Django%E5%BC%80%E5%8F%91%208019142fa1db48cbb4763f78f598a35c/Untitled%205.png)

## 13.1 登录

登录成功后：

- cookie：随机字符串
- session：用户信息

在其他需要登录才能访问的页面中，都需要加入：

```python
def index(request):
		info = request.session.get("info")
		if not info:
				return redirect('/login/')
		...
```

目标：在18个视图函数前面统一加入判断

```python
info = request.session.get("info")
if not info:
		return redirect('/login/')
```

## 13.2 中间件的体验

- 定义中间件

```python
from django.utils.deprecation import MiddlewareMixin

class M1(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # 如果方法中没有返回值（返回None），继续向后走
        # 如果有返回值 HttpResponse、render、redirect
        print("M1 is comming.")

    def process_response(self, request, response):
        print("M1 is going.")
        return response

class M2(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        print("M2 is comming.")

    def process_response(self, request, response):
        print("M2 is going.")
        return response
```

- 应用中间件 `settings.py`

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    **'app01.middleware.auth.M1'**,
    **'app01.middleware.auth.M2'**,
]
```

- 在中间件的process_request方法

```python
# 如果方法中没有返回值（返回None），继续向后走
# 如果有返回值 HttpResponse、render、redirect，则不再向后执行
```

## 13.3 中间件实现登录校验

- 编写中间件（旧写法）

```python
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL
        if request.path_info == '/login/':
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登录过，就可以继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect("/login/")
```

- 编写中间件（新写法）

```python
from django.shortcuts import redirect

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 0.排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL
        if request.path_info == '/login/':
            return self.get_response(request)

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登录过，就可以继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            return self.get_response(request)

        # 2.没有登录过，重新回到登录页面
        return redirect("/login/")
```

- 应用中间件 `settings.py`

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    **'app01.middleware.auth.AuthMiddleware'**,
]
```

## 13.4 注销

- logout

```python
def logout(request):
		request.session.clear()
		return redirect("/login/")
```

# 14. 图片验证码

## 14.1 生成图片

```python
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter

def check_code(width=120, height=30, char_length=5, font_file='Monaco.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndchar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndcolor():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndchar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text((i * width / char_length, h), char, rndcolor(), font)

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndcolor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndcolor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndcolor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndcolor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
```

生成图片后，将图片保存在缓存中，不用写入到文件，方便读取。

设置session有效时间60s，过期自动销毁。

# 15. Ajax请求

## 什么是 AJAX ？

AJAX = 异步 JavaScript 和 XML。

AJAX 是一种用于创建快速动态网页的技术。

通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。

传统的网页（不使用 AJAX）如果需要更新内容，必需重载整个网页面。

浏览器向网站发送请求时：URL 和 表单的形式提交

- GET
- POST

特点：页面刷新

除此之外，也可以基于Ajax向后台发送请求（偷偷的发送请求）

- 依赖jQuery
- 编写ajax代码

```jsx
$.ajax({
		url:"发送的地址",
		type:"post",
		data:{
				n1:123,
				n2:456,
		},
		success:function (res) {
				console.log(res);
		}
})
```

## 15.1 GET请求

```jsx
$.ajax({
    url: '/task/list/',
    type: 'get',
    data: {
        n1: 123,
        n2: 456
    },
    success: function (res) {
        alert(res);
    }
})
```

```jsx
from django.shortcuts import render

def task_list(request):
		print(request.GET)
		return render(request, 'task_list.html')
```

## 15.2 POST请求

```jsx
$.ajax({
    url: '/task/list/',
    type: 'post',
    data: {
        n1: 123,
        n2: 456
    },
    success: function (res) {
        alert(res);
    }
})
```

```jsx
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def task_list(request):
    """ 任务列表 """
    print(request.GET)
    print(request.POST)
    return render(request, "task_list.html")
```

POST请求需要 `csrf_token` 认证，可以通过添加**装饰器**的方法免除认证

## 15.3 关闭绑定事件

```html
{% extends 'layout.html' %}

{% block content %}
    <div class="container">
        <h1>任务管理</h1>
        <h3>示例一</h3>
        <input id="btn1" type="button" class="btn btn-primary" value="click"/>
    </div>
{% endblock %}

{% block js %}
    <script type="text/javascript">
        $(function () {
            //  页面框架加载完成之后代码自动执行
            bindBtn1Event();

        })

        function bindBtn1Event() {
            $("#btn1").click(function () {
                $.ajax({
                    url: '/task/list/',
                    type: 'post',
                    data: {
                        n1: 123,
                        n2: 456
                    },
                    success: function (res) {
                        alert(res);
                    }
                })
            })
        }

    </script>
{% endblock %}
```

## 15.4 ajax的返回值

一般都会返回 **JSON** 格式

- 前端

```html
{% extends 'layout.html' %}

{% block content %}
    <div class="container">
        <h1>任务管理</h1>
        <h3>示例一</h3>
        <input id="btn1" type="button" class="btn btn-primary" value="click"/>
    </div>
{% endblock %}

{% block js %}
    <script type="text/javascript">
        $(function () {
            //  页面框架加载完成之后代码自动执行
            bindBtn1Event();

        })

        function bindBtn1Event(message) {
            $("#btn1").click(function (message) {
                $.ajax({
                    url: '/task/ajax/',
                    type: 'post',
                    data: {
                        n1: 123,
                        n2: 456
                    },
                    dataType: "JSON",
                    success: function (res) {
                        console.log(res);
                        alert(res.status + " " + res.data);
                    }
                })
            })
        }

    </script>
{% endblock %}
```

- 后端

```python
import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def task_list(request):
    """ 任务列表 """
    return render(request, "task_list.html")

@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [1, 2, 3, 4]}
    return HttpResponse(json.dumps(data_dict))
```

### ajax样例

```html
{% extends 'layout.html' %}

{% block content %}
    <div class="container">
        <h1>Ajax学习</h1>

        <h3>示例1</h3>
        <input id="btn1" type="button" class="btn btn-primary" value="click 1"/>

        <h3>示例2</h3>
        <input id="txtUser" type="text" placeholder="姓名"/>
        <input id="txtAge" type="text" placeholder="年龄"/>
        <input id="btn2" type="button" class="btn btn-primary" value="click 2"/>

        <h3>示例3</h3>
        <form id="form3">
            <input type="text" name="user" placeholder="姓名"/>
            <input type="text" name="age" placeholder="年龄"/>
            <input type="text" name="email" placeholder="邮箱"/>
            <input type="text" name="more" placeholder="介绍"/>
        </form>
        <input id="btn3" type="button" class="btn btn-primary" value="click 3"/>
    </div>
{% endblock %}

{% block js %}
    <script type="text/javascript">
        $(function () {
            //  页面框架加载完成之后代码自动执行
            bindBtn1Event();

            bindBtn2Event();

            bindBtn3Event();

        })

        function bindBtn1Event() {
            $("#btn1").click(function () {
                $.ajax({
                    url: '/task/ajax/',
                    type: 'post',
                    data: {
                        n1: 123,
                        n2: 456
                    },
                    dataType: "JSON",
                    success: function (res) {
                        console.log("btn1 succeed");
                    }
                })
            })
        }

        function bindBtn2Event() {
            $("#btn2").click(function () {
                $.ajax({
                    url: '/task/ajax/',
                    type: 'post',
                    data: {
                        name: $("#txtUser").val(),
                        age: $("#txtAge").val(),
                    },
                    dataType: "JSON",
                    success: function (res) {
                        console.log("btn2 succeed");
                    }
                })
            })
        }

        function bindBtn3Event() {
            $("#btn3").click(function () {
                $.ajax({
                    url: '/task/ajax/',
                    type: 'post',
                    data: $("#form3").serialize(),
                    dataType: "JSON",
                    success: function (res) {
                        console.log("btn3 succeed");
                    }
                })
            })
        }

    </script>
{% endblock %}
```

# 16. 订单

```python
class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="状态", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)
```

# 17. 图表

- highchart，国外
- echarts，国内

更多参考文档：[Apache ECharts](https://echarts.apache.org/zh/index.html)

# 18. 关于文件上传

## 1. 基本操作

```html
<form method="post" **enctype="multipart/form-data"**>
    {% csrf_token %}
    <input type="text" name="username">
    <input type="file" name="avatar">
    <input type="submit" value="提交">
</form>
```

```python
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
```

## 案例：批量上传数据

```html
<div class="panel panel-default">
    <!-- Default panel contents -->
    <div class="panel-heading">
        <span class="glyphicon glyphicon-th-list" aria-hidden="true"></span>
        批量添加
    </div>
    <div class="panel-body">
        <form method="post" enctype="multipart/form-data" action="/depart/multi/">
            {% csrf_token %}
            <div class="form-group">
                <input type="file" name="exc">
            </div>
            <input type="submit" value="上传" class="btn btn-info btn-sm">
        </form>
    </div>
</div>
```

```python
from openpyxl import load_workbook
def depart_multi(request):
    """ 批量上传（Excel文件） """

    # 1. 获取用户上传的文件对象
    file_object = request.FILES.get("exc")

    # 2. 对象传递给openpyxl，由openpyxl读取文件的内容
    wb = load_workbook(file_object)
    sheet = wb.worksheets[0]

    # 3. 循环换取每一行数据
    for row in sheet.iter_rows(min_row=2):
        text = row[0].value
        exists = models.Department.objects.filter(title=text).exists()
        if not exists:
            models.Department.objects.create(title=text)

    return redirect('/depart/list/')
```

## 案例：混合数据（Form）

提交页面时：用户输入数据 + 文件（输入不能为空、报错）

- Form生成HTML标签：type=file
- 表单的验证
- form.cleaned_data 获取 数据 + 文件对象

```html
{% extends 'layout.html' %}

{% block content %}

    <div class="container">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">{{ title }}</h3>
            </div>
            <div class="panel-body">
                <form method="post" enctype="multipart/form-data" novalidate>
                    {% csrf_token %}

                    {% for field in form %}
                        <div class="form-group">
                            <label>{{ field.label }}</label>
                            {{ field }}
                            <span style="color: red">{{ field.errors.0 }}</span>
                        </div>
                    {% endfor %}

                    <button type="submit" class="btn btn-primary">提 交</button>
                </form>
            </div>
        </div>
    </div>

{% endblock %}
```

```python
import os

from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import UpForm

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
        db_file_path = os.path.join("static", "img", image_object.name)
        file_path = os.path.join("app01", db_file_path)
        with open(file_path, mode='wb') as f:
            for chunk in image_object.chunks():
                f.write(chunk)

        # 2.将图片文件路径写入到数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=db_file_path,
        )

        return redirect('/upload/form/')
    return render(request, 'upload_form.html', {"form": form, "title": title})
```

【注意】就目前而言，所有的静态文件都只能放在static目录

在django的开发过程中有两个特殊的的文件夹：

- static：存放静态文件的路径，包括：CSS、JS、项目图片
- media：用户上传的数据的目录

## 2. 启用media

在urls.py中进行配置：

```python
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
```

在settings.py中进行配置：

```python
import os

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

在浏览器上访问图片地址：

`127.0.0.1:8000/media/1.png`

## 案例：混合数据（Form）

```python
import os

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
```

## 案例：混合数据（ModelForm）

### models.py

```python
class City(models.Model):
    """ 老板 """
    name = models.CharField(verbose_name="名称", max_length=32)
    population = models.IntegerField(verbose_name="年龄")

    # 本质上数据也是CharField，自动保存数据
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')
```

### 定义ModelForm

```python
from app01.utils.bootstrap import BootStrapModelForm

class UpModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"
```

## 视图

```python
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
```

## 小结

- 自己手动去写

```python
file_object = request.FILES.get("exc")
```

- Form组件（表单验证）

```python
request.POST
file_obejct = request.FILES.get("exc")

# 具体文件操作还是手动自己做
```

- ModelForm组件（表单验证 + 自动保存数据库 + 自动保存文件）

```python
- media文件夹
- models.py定义类文件要
img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')
```

# 总结

关于django的开发知识点，更多的案例：

- 并发编程（进程线程协程）
- django开发知识点
- 项目开发
- 进阶项目
- 前后端分离的项目：django + drf框架 + vue.js

```python
- Django
- drf框架
```

- git 版本控制和协同开发 + 任务管理平台
- 微信小程序：Django + drf框架编写
>>>>>>> 19875e1545413da6c34259e6bc08a4c043860e5f
