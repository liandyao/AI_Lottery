# xingyunqiu/utils.py
from django.http import JsonResponse

def result_success(data,message='success', safe=False, **kwargs):
    """
    返回一个自定义的 JSON 响应。

    :param data: 要返回的数据。
    :param safe: 是否只允许字典类型的响应。默认为 False。
    :param kwargs: 其他传递给 JsonResponse 的参数。
    :return: JsonResponse 对象。
    """
    my_data = {
        'code': 200,
        'data': data,
        'message': message,
    }
    return JsonResponse(my_data, safe=safe, **kwargs)

def result_error(data, message='error', safe=False, **kwargs):
    """
    返回一个自定义的 JSON 响应。

    :param data: 要返回的数据。
    :param safe: 是否只允许字典类型的响应。默认为 False。
    :param kwargs: 其他传递给 JsonResponse 的参数。
    :return: JsonResponse 对象。
    """
    my_data = {
        'code': 500,
        'data': data,
        'message': message,
    }
    return JsonResponse(my_data, safe=safe, **kwargs)