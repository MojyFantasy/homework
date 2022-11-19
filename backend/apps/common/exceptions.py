import json

from django.utils.deprecation import MiddlewareMixin
from rest_framework.views import exception_handler


class CustomExceptionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 400:
            data = {}
            if isinstance(response.data, dict):
                err_lst = []
                for key in response.data:
                    if isinstance(response.data[key], list):
                        err_lst.extend(response.data[key])
                    else:
                        err_lst.append(response.data[key])
                data['msg'] = '、'.join(err_lst)
                data['result'] = 'error'
                response.data = data
                response.content = json.dumps(data)
            elif isinstance(response.data, list):
                data['msg'] = '、'.join(response.data)
                data['result'] = 'error'
                response.data = data
                response.content = json.dumps(data)
            else:
                data['msg'] = response.data
                data['result'] = 'error'
                response.data = data
                response.content = json.dumps(data)
        return response


class NotFoundDataFileError(Exception):
    """
    classdocs : 没有找到文件
    """
    def __init__(self, err):
        Exception.__init__(self, err)


class NotDoneError(Exception):
    """
    classdocs : 有导入任务未完成
    """
    def __init__(self, err):
        Exception.__init__(self, err)


class ParameterError(Exception):
    """
    classdocs : 参数异常
    """
    def __init__(self, err):
        Exception.__init__(self, err)
