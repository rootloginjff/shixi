from rest_framework import serializers
from user.models import User


class passwordLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11,min_length=11,allow_null=False,trim_whitespace=True,allow_blank=False)
    password = serializers.CharField(max_length=20,min_length=8,allow_null=False,trim_whitespace=True,allow_blank=False)
    class Meta:
        # 补充说明
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
                'help_text': '密码8－20位',
            }
        }


class phonecodeLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11,min_length=11,allow_null=False,trim_whitespace=True,allow_blank=False)
    code = serializers.CharField(max_length=4,min_length=4,allow_null=False,trim_whitespace=True,allow_blank=False)

class phonesendcodeLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11,min_length=11,allow_null=False,trim_whitespace=True,allow_blank=False)


class phonecoderegiestSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4,min_length=4,allow_null=False,trim_whitespace=True,allow_blank=False,read_only=True)

    class Meta:
        model = User
        fields = ['phone','username','password','code']
        extra_kwargs = {
            'phone': {
                'min_length': 11,
                'max_length': 11,
                'error_messages': {
                    'min_length': '11个字符',
                    'max_length': '11个字符',
                },
                'help_text': '手机号11位',
            },
            'password': {
                'help_text': '密码8－20位',
            },
            'username':{
                'help_text': '用户昵称',
            },
            'code':{
                'help_text': '手机注册4位数字验证码',
            }
        }