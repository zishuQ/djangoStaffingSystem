from django import forms


class Bootstrap:
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


class BootstrapModelForm(Bootstrap, forms.ModelForm):
    pass


class BootstrapForm(Bootstrap, forms.Form):
    pass
