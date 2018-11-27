"""
装饰器模块
"""
from django.shortcuts import redirect, reverse


def login_required(func):
    """
    登入验证装饰器，验证是否已经登入，未登入的话重定向至登入页面
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if request.user:
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return wrapper
