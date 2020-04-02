from .models import User
import random
from .alidayu import send_login_code
from django.conf import settings
from django.core.cache import cache


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


def check_user_password(user_obj, password):
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



def create_random_code():
    random_number = random.randint(1000, 9999)
    return random_number


def send_code(phone):
    code = create_random_code()
    if settings.ALIDAYU_ISOPEN:
        messages = send_login_code(phone, 'login', code)
        return str(messages, encoding='utf-8'), code
    else:
        messages = '{"Message":"OK","RequestId":"207D8ABE-6666-4532-8AF0-D7EFC51382E2","BizId":"796811885785891254^0","Code":"OK","code":'+str(code)+'}'
        print("code:", code)
        return messages, code


def check_user_code(user_obj, code):
    true_code = cache.get(user_obj.phone, None)
    if str(true_code) == str(code):
        return True
    else:
        return False