#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：py-client -> f5
@IDE    ：PyCharm
@Author ：sven
@Date   ：2022/2/17 13:08
@Desc   ：
"""
from icontrol.authtoken import iControlRESTTokenAuth

def make_auth(api_client):
    """

    :param api_client:
    :return:
    """
    return iControlRESTTokenAuth(api_client.username,
                                 api_client.password,
                                 verify=api_client.verify)