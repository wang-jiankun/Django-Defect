"""
视图函数模块
"""
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.forms.models import model_to_dict
from .forms import RegisterForm, LoginForm, User
from .decorators import login_required
from .models import Log, State, Chart
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
    current_date = dt.date.today()
    current_time = dt.datetime.now().strftime("%H:%M:%S")
    state = model_to_dict(State.objects.last())
    step_time = model_to_dict(Chart.objects.first())
    avg_step_time = model_to_dict(Chart.objects.last())
    data_json = {'date': str(current_date), 'time': current_time,
                 'state': state, 'step_time': step_time, 'avg_time': avg_step_time}
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
    current_date = dt.date.today()
    logs = Log.objects.filter(time__contains=current_date)
    keys = {'s': '2019-01-01', 'e': str(current_date)}
    return render(request, 'detection.html', context={"logs": logs, 'pos': 2, 'ks': keys})


@login_required
def log_search(request):
    """
    检索检测记录视图函数，根据选择的时间段从数据库提取相应的记录，并返回给浏览器
    :param request:
    :return:
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    end_date_p = end_date[0:-2]+str(int(end_date[-2:])+1)
    keys = {'s': start_date, 'e': end_date}
    logs = Log.objects.filter(time__range=(start_date, end_date_p))
    return render(request, 'detection.html', context={"logs": logs, 'pos': 2, 'ks': keys})


@login_required
def defect_view(request):
    """
    查看缺陷图片视图函数，从数据库提取所有当天的缺陷图片返回给浏览器
    :param request:
    :return:
    """
    current_date = dt.date.today()
    # logs = Log.objects.filter(time__contains=current_date)
    keys = {'s': '2019-01-01', 'e': str(current_date), 'c': 'normal'}

    return render(request, 'defect.html', context={"logs": [], 'pos': 3, 'ks': keys})


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
    end_date_p = end_date[0:-2]+str(int(end_date[-2:])+1)
    keys = {'s': start_date, 'e': end_date, 'c': defect_type}
    logs = Log.objects.filter(detect_class=defect_type, time__lte=end_date_p)
    # logs = Log.objects.filter(detect_class=defect_type, time__range=(start_date, end_date))

    paginator = Paginator(logs, 3)

    # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
    page = request.GET.get('p')
    try:
        defects = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        defects = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        defects = paginator.page(paginator.num_pages)

    return render(request, 'defect.html', context={'logs': defects, 'pos': 3, 'ks': keys})
    # return render(request, 'defect.html', context={"logs": logs, 'pos': 3})
