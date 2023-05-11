from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01.utils.bootstrap import BootstrapModelForm, BootstrapForm
from app01.utils.encrypt import md5


# class UserModelForm(forms.ModelForm):
#     name = forms.CharField(min_length=3, label="用户名")
#
#     class Meta:
#         model = models.UserInfo
#         fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
#         # widgets = {
#         #     "name": forms.TextInput(attrs={"class": "form-control"}),
#         #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
#         #     "age": forms.TextInput(attrs={"class": "form-control"}),
#         # }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # 循环找到所有的插件，添加了class="form-control"
#         for name, field in self.fields.items():
#             field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class UserModelForm(BootstrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ["name", 'password', "age", "account", "create_time", "gender", "depart"]


class PrettyModelForm(BootstrapModelForm):
    # 验证：方式1 --- 字段 + 正则
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"    获取所有字段
        fields = ["mobile", "price", "level", "status"]
        # exclude = ["level"]   获取除"level"外的所有字段

    # 验证：方式2 --- 钩子方法
    def clean_mobile(self):
        # 当前编辑的那一行的ID
        # self.instance.pk

        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile)
        if exists:
            raise ValidationError("手机号已存在")

        return txt_mobile


class PrettyEditModelForm(PrettyModelForm):
    """ 继承重写，禁止手机号被更改 """
    mobile = forms.CharField(disabled=True, label="手机号")

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        return txt_mobile


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("密码不一致")

        # 返回什么，此字段以后保存到数据库就是什么
        return confirm


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(AdminModelForm):
    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        md5_pwd = super().clean_password()
        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")

        return md5_pwd


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput,
        }


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]
