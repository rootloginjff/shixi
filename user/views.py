
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .common import user_is_exit,create_Token,chect_user_password,check_user_status
class phoneLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11, allow_blank=False, trim_whitespace=True)
    password = serializers.CharField(max_length=18, min_length=8,allow_blank=False, trim_whitespace=True)

    class Meta:
        # 补充说明

        fields = ('phone','password')
        extra_kwargs = {
            'phone': {
                'min_length': 11,
                'max_length': 11,
                'error_messages': {
                    'min_length': '11个字符',
                    'max_length': '11个字符',
                },
            },
            'password': {
                'help_text': '密码６－８位',
            }
        }

def message_response(code,messages,data={}):
    return Response({'code': code, 'messages': messages,'data':data})

@api_view(['GET'])
def index(request):
    Token = request.META.get('HTTP_TOKEN')
    if Token:
        user_obj = cache.get(Token,None)
        if user_obj:
            return message_response(20005, '访问成功', {"phone":user_obj.phone})
        else:
            return message_response(20006, 'token已过期/未登陆', {})
    else:
        return message_response(20005, '未携带token', {})

@api_view(['POST'])
def phonePasswordlogin(request):
    if request.method == 'POST':
        data = request.POST
        ser = phoneLoginSerializer(data=data)
        if ser.is_valid():
            pass
        else:
            return message_response(20005,'参数验证错误',{"errors":ser.errors})
        phone = request.POST['phone']
        password = request.POST['password']
        user_obj = user_is_exit(phone)
        if user_obj:
            if check_user_status(user_obj):
                if chect_user_password(user_obj,password):
                    Token = create_Token(user_obj)
                    cache.set(Token,user_obj,60)
                    return message_response(20000, '登陆成功', {"Token":Token})
                else:
                    return message_response(20004, '密码错误', {})
            else:
                return message_response(20001, '用户被禁用', {})
        else:
            return message_response(20002,'用户手机不存在',{})

