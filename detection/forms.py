"""
表单验证模块
"""
from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    """
    注册信息表单验证类
    """
    password_repeat = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise forms.ValidationError('两次密码输入不一致！')
        return cleaned_data

    class Meta:
        """
        所继承的数据库的 model 和字段
        """
        model = User
        fields = ['username', 'password', 'email']


class LoginForm(forms.ModelForm):
    """
    登入信息表单验证类
    """
    class Meta:
        model = User
        fields = ['email', 'password']
