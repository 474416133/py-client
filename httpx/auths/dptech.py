#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：py-client -> dptech
@IDE    ：PyCharm
@Author ：sven
@Date   ：2022/2/17 13:08
@Desc   ：
"""
import logging
import base64

from requests.auth import AuthBase


logger = logging.getLogger('client.httpx.auths')


class DpAuth(AuthBase):
    """
    迪普授权
    """
    def __init__(self, host, username, password, token_type='Basic'):
        """
        :param host:
        :param username:
        :param password:
        :param token_type:
        """
        self._host = host
        self._username = username
        self._password = password
        self._token_type = token_type
        self._token = '{} {}'.format(self._token_type, self.create_new_token())


    def create_new_token(self):
        """
        :return:
        """
        username_password = f'{self._username}:{self._password}'
        return base64.b64encode(username_password.encode('utf-8')).decode('utf-8')

    def __call__(self, request):
        """
        @override
        :param request:
        :return:
        """
        request.headers['Accept'] = 'application/json'
        request.headers['Accept-Language'] = 'zh_CN'
        request.headers['Cache-Control'] = 'no-cache'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Host'] = self._host
        # User-Agent可能需要更新
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
        request.headers['Content-Type'] = 'application/json;charset=utf-8'
        request.headers['Authorization'] = self._token

        return request


def make_auth(api_client):
    """

    :param api_client:
    :return:
    """
    return DpAuth(api_client.host[8:], api_client.username, api_client.password)
