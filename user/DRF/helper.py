from rest_framework.response import Response


def message_response(code, messages, data={}):
    return Response({'code': code, 'messages': messages,'data': data})
