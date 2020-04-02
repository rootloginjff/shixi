from .models import User
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