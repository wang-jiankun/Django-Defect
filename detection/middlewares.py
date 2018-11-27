"""
中间件模块
"""
from .models import User


def front_user_middleware(get_response):
    """
    获取 request 中的 cookie 信息，并从数据库中提取相应的信息
    :param get_response:
    :return:
    """
    def middleware(request):
        # request到达view之前的中间件代码
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                request.user = user
            except:
                request.user = None
        else:
            request.user = None
        response = get_response(request)
        # response到达浏览器之前的代码
        return response
    return middleware
