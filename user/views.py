
from django.core.cache import cache

from rest_framework.decorators import api_view
from .DRF.helper import message_response
from .DRF.user_serializers import passwordLoginSerializer
from .DRF.user_serializers import phonecoderegiestSerializer
from .DRF.user_serializers import phonecodeLoginSerializer
from .DRF.user_serializers import phonesendcodeLoginSerializer
from .common import user_is_exit, create_Token, check_user_password, check_user_status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import User

from django.views.generic import View
from rest_framework import exceptions
from django.conf import settings
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


class PhoneCodeRegisterCreateAPIView(CreateAPIView):
    serializer_class = phonecoderegiestSerializer
    queryset = User.objects.all()

class PhonePasswordLoginApiView(APIView):
    def post(self, request):
        data = request.POST
        ser = passwordLoginSerializer(data=data)
        if ser.is_valid():
            pass
        else:
            return message_response(20005, '参数验证错误', {"errors": ser.errors})
        phone = ser.validated_data['phone']
        password = ser.validated_data['password']
        user_obj = user_is_exit(phone)
        if user_obj:
            if check_user_status(user_obj):
                if check_user_password(user_obj, password):
                    Token = create_Token(user_obj)
                    cache.set(Token, user_obj, 60)
                    return message_response(20000, '登陆成功', {"Token": Token})
                else:
                    return message_response(20004, '密码错误', {})
            else:
                return message_response(20001, '用户被禁用', {})
        else:
            return message_response(20002, '用户手机不存在', {})


class logoutAPIView(APIView):
    def get(self,request):
        Token = request.META.get('HTTP_TOKEN')
        if Token:
            user_obj = cache.get(Token, None)
            if user_obj:
                cache.set(Token, user_obj, 0)
                return message_response(20005, '退出成功', {})
            else:
                return message_response(20006, '未登陆', {})
        else:
            return message_response(20005, '未登陆', {})


class phonecodeloginApiView(APIView):
    def post(self,request):
        data =request.data
        ser = phonecodeLoginSerializer(data=data)
        if ser.is_valid():
            pass
        else:
            return message_response(20005, '参数验证错误', {"errors": ser.errors})
        print(ser.validated_data)
        phone = ser.validated_data['phone']
        code = ser.validated_data['code']
        user_obj = user_is_exit(phone)
        if user_obj:
            if check_user_status(user_obj):
                if check_user_code(user_obj, code):
                    Token = create_Token(user_obj)
                    cache.set(Token, user_obj, 60)
                    return message_response(20000, '登陆成功', {"Token": Token})
                else:
                    return message_response(20004, '验证码错误', {})
            else:
                return message_response(20001, '用户被禁用', {})
        else:
            return message_response(20002, '用户手机不存在', {})

class phonesendcodeApiView(APIView):
    def post(self,request):
        data = request.data
        ser = phonesendcodeLoginSerializer(data=data)
        if ser.is_valid():
            pass
        else:
            return message_response(20005, '参数验证错误', {"errors": ser.errors})
        phone = ser.validated_data['phone']
        if cache.get(phone,None):
            return message_response(20009, "不要重复发送", {})
        messages,code = send_code(phone)
        messages_dict = eval(messages)
        if messages_dict.get('Message') == "OK":
            cache.set(phone,code,60)
            return message_response(20007,"短信发送成功",{"messages":messages})
        else:
            return message_response(20007, "短信发送失败", {"messages": messages})

import random
from .alidayu import send_login_code
def create_random_code():
    random_number = random.randint(1000,9999)
    return random_number

def send_code(phone):
    code = create_random_code()
    if settings.ALIDAYU_ISOPEN:
        messages = send_login_code(phone, 'login', code)
        return str(messages, encoding='utf-8'), code
    else:
        messages = '{"Message":"OK","RequestId":"207D8ABE-6666-4532-8AF0-D7EFC51382E2","BizId":"796811885785891254^0","Code":"OK"}'
        print("code:",code)
        return messages, code
def check_user_code(user_obj,code):
    true_code = cache.get(user_obj.phone,None)
    if str(true_code) == str(code):
        return True
    else:
        return False


