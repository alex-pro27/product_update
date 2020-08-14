# coding: utf8
import base64
import datetime
import hashlib

import requests


class AliexpressRequest(object):

    @classmethod
    def auth(cls, email, token, password, *class_args, **class_kwargs):
        self = cls(*class_args, **class_kwargs)
        self.email = email
        self.token = token
        self.password = password
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
        }
        cls.create_basic_token(self)
        cls.create_access_token(self)

        def _request(query):
            r = requests.post(
                "https://alix.brand.company/api_top3/",
                headers=self.headers,
                params=query
            )
            ans = r.json()
            if ans.get("errorCode"):
                return ans
            return ans[query["method"].replace(".", "_") + "_response"]

        return _request

    @classmethod
    def create_basic_token(cls, obj):
        obj.headers.update({
            'X-User-Authorization': "Basic " + base64.b64encode("{}:{}".format(obj.email, obj.password))
        })

    @classmethod
    def create_access_token(cls, obj):
        token = "AccessToken {0}:{1}".format(
            obj.email,
            hashlib.md5(
                obj.email +
                datetime.datetime.utcnow().strftime("%d%m%Y%H") +
                obj.token
            ).hexdigest()
        )
        obj.headers.update({
            'Authorization': token
        })