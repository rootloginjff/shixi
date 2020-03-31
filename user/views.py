from .models import User
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

# class phoneLoginSerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=11, min_length=11, allow_blank=False, trim_whitespace=True)
#     password = serializers.CharField(max_length=200, allow_blank=False, trim_whitespace=True)


def message_response(code,messages,data={}):
    return Response({'code': code, 'messages': messages,'data':data})

@api_view(['GET','POST'])
def index(request):
    Token = request.GET.get('Token',None)
    if Token:
        user_obj = cache.get(Token,None)
        if user_obj:
            return message_response(20005, '访问成功', {"phone":user_obj.phone})
        else:
            return message_response(20006, 'token已过期/未登陆', {})
    else:
        return message_response(20005, '未携带token', {})

@api_view(['GET','POST'])
def phonePasswordlogin(request):
    if request.method == 'POST':
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
    return message_response(20003, '没有get', {})

def user_is_exit(phone):
    '''
    判断用户是否存在，存在则返回该对象
    不存在则返回空列表
    '''
    user_obj = User.objects.filter(phone=phone)
    if user_obj:
        return user_obj[0]
    else:
        return False


def check_user_status(user_obj):
    if user_obj.status == '1':
        return True
    else:
        return False

def chect_user_password(user_obj,password):
    if user_obj.password == password:
        return True
    else:
        return False

def create_Token(user_obj):
    import hashlib,time
    ctime = str(time.time())
    md5=hashlib.md5(bytes(user_obj.phone,encoding="utf8"))
    md5.update(bytes(ctime,encoding="utf8"))
    return md5.hexdigest()