#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.conf import settings
client = AcsClient(settings.ALIDAYU_ACCESSKEYID, settings.ALIDAYU_ACCESSSECRET, settings.ALIDAYU_REGIONID)


# python2:  print(response)

def send_login_code(phone, type, code):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', settings.ALIDAYU_REGIONID)
    request.add_query_param('PhoneNumbers', str(phone))
    request.add_query_param('SignName', settings.ALIDAYU_SIGNNAME)
    if type == 'login':
        request.add_query_param('TemplateCode', settings.ALIDAYU_TEMPLATECODE_LOGIN)
    request.add_query_param('TemplateParam', "{'code':"+str(code)+"}")

    response = client.do_action_with_exception(request)

    return response