#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：py-client -> sang4
@IDE    ：PyCharm
@Author ：sven
@Date   ：2022/2/17 13:08
@Desc   ：
"""

import time
import logging
import requests
from requests.auth import AuthBase
from urllib.parse import urlsplit


logger = logging.getLogger('client.httpx.auths')


class Sang4Auth(AuthBase):
    """
    深信服授权
    """

    def __init__(self, username, password, client_name, token_path='/api/ad/v2/token', verify=False):
        """
        :param username:
        :param password:
        :param client_name:
        :param token_path:
        """
        self._username = username
        self._password = password
        self._client_name = client_name
        self._token_path = token_path
        self._token_info = {}
        self._verify = verify

    def _check_token_validity(self):
        """
        检验token是否过期
        :return:
        """
        if not self._token_info:
            return False
        elif time.time() > (self._token_info.get('expired_timestamp') or 0):
            return False
        return True

    def get_new_token(self, netloc, scheme):
        """
        获取新token
        :param netloc:
        :return:
        """
        uri = '{}://{}{}'.format(scheme, netloc, self._token_path)
        body = {
            'username': self._username,
            'password': self._password,
            'client_name': self._client_name
        }
        resp = requests.post(uri, json=body, verify=self._verify)
        if resp.status_code != 200:
            err_msg = 'status_code:{}, content:{}'.format(resp.status_code, resp.content)
            logger.error(err_msg)
            raise RuntimeError(err_msg)
        self._token_info = resp.json()

    def __call__(self, request):
        """
        @override
        :param request:
        :return:
        """
        if not self._check_token_validity():
            scheme, netloc, path, _, _ = urlsplit(request.url)
            self.get_new_token(netloc, scheme)

        request.headers['x-token-sangforad'] = self._token_info['name']
        return request


def make_auth(client):
    """
    :param client:
    :return:
    """
    return Sang4Auth(client.username, client.password, client.kwargs['client_name'])