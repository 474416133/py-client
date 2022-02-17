#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project -> File   ：py-client -> sang4
@IDE    ：PyCharm
@Author ：sven
@Date   ：2022/2/17 13:46
@Desc   ：
"""

available_paths = [
        '/api/ad/v2/slb/virtual-service/',
        '/api/ad/v2/slb/pool/',
        '/api/ad/v2/slb/snat-pool/',
        '/api/ad/v2/slb/ipro/',
    ]


if __name__ == '__main__':
    from httpx.base import ApiClient
    from httpx.auths import sang4
    api_client = ApiClient('https://192.168.1.2',
                           username='test',
                           password='test',
                           client_name='Sangfor_test',
                           make_auth=sang4.make_auth)


    for path in available_paths:
        result = api_client.get(path)
        print(result)

