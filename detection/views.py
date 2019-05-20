"""
视图函数模块
"""
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from .forms import RegisterForm, LoginForm, User
from .decorators import login_required
from .models import Log, State
import datetime as dt
import json

# Create your views here.


def index(request):
    """
    首页视图函数，返回所有欢迎页面的 HTML
    :param request:
    :return:
    """
    # log = Log(detect_class='划痕')
    # log.save()
    return render(request, 'index.html', context={'pos': 1})


def update(request):
    """
    更新数据
    :param request:
    :return:
    """
    data = State.objects.last()
    data_json = {'run_state': data.run_state, 'uph': data.uph, 'detection_num': data.detection_num,
                 'defect_num': data.defect_num}
    return HttpResponse(json.dumps(data_json), content_type='application/json')


# 登录
class LoginView(View):
    """
    登入类视图
    """
    def get(self, request):
        """
        GET请求响应函数，返回登入页面的 HTML
        :param request:
        :return:
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        POST 请求响应函数，登入信息验证，设置 cookie，页面重定向
        :param request:
        :return:
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(email=email, password=password).first()
            if user:
                request.session['user_id'] = user.pk
                return redirect(reverse('index'))
            else:
                print('用户名或者密码错误！')
                return redirect(reverse('login'))
        else:
            print(form.errors)
            return redirect(reverse('login'))


# 注册
class RegisterView(View):
    """
    注册类视图
    """
    def get(self, request):
        """
        GET请求响应函数，返回注册页面的 HTML
        :param request:
        :return:
        """
        return render(request, 'register.html')

    def post(self, request):
        """
        POST 请求响应函数，注册信息验证，保存注册信息到数据库，页面重定向
        :param request:
        :return:
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            User.objects.create(email=email, password=password, username=username)
            return redirect(reverse('login'))
        else:
            print(form.errors)
            return redirect(reverse('register'))


def logout(request):
    """
    注销视图函数，删除 cookie
    :param request:
    :return:
    """
    request.session.flush()
    return redirect(reverse('index'))


@login_required
def detection_view(request):
    """
    检测记录视图函数，从数据库提取所有检测记录以表格形式的返回给浏览器
    :param request:
    :return:
    """
    logs = Log.objects.all()
    return render(request, 'detection.html', context={"logs": logs, 'pos': 2})


@login_required
def log_search(request):
    """
    检索检测记录视图函数，根据选择的时间段从数据库提取相应的记录，并返回给浏览器
    :param request:
    :return:
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date == '' or end_date == '':
        logs = Log.objects.all()
    else:
        logs = Log.objects.filter(time__range=(start_date, end_date))
    return render(request, 'detection.html', context={"logs": logs, 'pos': 2})


@login_required
def defect_view(request):
    """
    查看缺陷图片视图函数，从数据库提取所有当天的缺陷图片返回给浏览器
    :param request:
    :return:
    """
    # logs = Log.objects.filter(detect_class__in=['划痕', '污渍'])
    current_date = dt.date.today()
    logs = Log.objects.filter(time__startswith=current_date)

    return render(request, 'defect.html', context={"logs": logs, 'pos': 3})


@login_required
def defect_search(request):
    """
    检索缺陷图片视图函数，根据选择的时间段和缺陷类型从数据库提取相应的图片，并返回给浏览器
    :param request:
    :return:
    """
    defect_type = request.GET.get('class')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date == '' or end_date == '':
        logs = None
    else:
        logs = Log.objects.filter(detect_class='normal', time__range=(start_date, end_date))

    paginator = Paginator(logs, 1)

    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('page')
    try:
        defects = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        defects = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        defects = paginator.page(paginator.num_pages)

    return render(request, 'defect.html', context={'logs': defects, 'pos': 3})
    # return render(request, 'defect.html', context={"logs": logs, 'pos': 3})
