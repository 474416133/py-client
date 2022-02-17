#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：py-client -> base
@IDE    ：PyCharm
@Author ：sven
@Date   ：2022/2/17 12:52
@Desc   ：
"""
import logging
import requests


logger = logging.getLogger('client.httpx')


class ReadonlyField(object):

    def __init__(self, field_name):
        self._field_name = field_name

    def __get__(self, instance, owner):
        return getattr(instance, self._field_name)


class ApiClient(object):
    """

    """
    host = ReadonlyField('_host')
    token = ReadonlyField('_token')
    username = ReadonlyField('_username')
    password = ReadonlyField('_password')
    verify = ReadonlyField('_verify')
    make_auth = ReadonlyField('_make_auth')
    kwargs = ReadonlyField('_kwargs')
    session = ReadonlyField('_session')


    def __init__(self, host, token=None, username=None, password=None, verify=False, make_auth=None, **kwargs):
        """
        :param host: str,
        :param username: str,
        :param password: str,
        :param client_name: str,
        :param verify: str,
        :param make_auth: Callable[[ApiClient], requests.auth.AuthBase], auth 创建器
        """
        self._host = host
        self._token = token
        self._username = username
        self._password = password
        self._make_auth = make_auth
        self._verify = verify
        self._auth = None
        self._kwargs = kwargs

        self._session = requests.Session()
        if callable(self._make_auth):
            self._auth = self._make_auth(self)
            self._session.auth = self._auth

    def execute(self, method, path, **kwargs):
        """
        :param method:
        :param path:
        :param kwargs:
            - params:
            - data:
            - headers:
            - cookies:
            - files:
            - auth:
            - timeout:
            - allow_redirects:
            - proxies:
            - hooks:
            - stream:
            - verify:
            - cert:
            - json:
        :return:
        """
        uri = f'{self._host}{path}'
        kwargs.update(verify=self._verify)
        resp = self._session.request(method, uri, **kwargs)
        return resp.json()

    def get(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :return:
        """
        return self.execute('get', path, **kwargs)

    def post(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :return:
        """
        return self.execute('post', path, **kwargs)

    def put(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :return:
        """
        return self.execute('put', path, **kwargs)

    def delete(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :return:
        """
        return self.execute('delete', path, **kwargs)

    def patch(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :return:
        """
        return self.execute('patch', path, **kwargs)

    def head(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :return:
        """
        return self.execute('head', path, **kwargs)

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()