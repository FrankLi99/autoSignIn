# -*- coding: utf-8 -*-
# __author__: 臣疲软没糖
# 2/21/2023 4:52 PM

import requests
import os
import json
import logging
logging.basicConfig(level=logging.INFO)

updateAccesssTokenURL = 'https://auth.aliyundrive.com/v2/account/token'
signinURL = 'https://member.aliyundrive.com/v1/activity/sign_in_list'


class AutoSignInTool(object):
    # 通过 refresh token 更新 access_token 并获得昵称
    @staticmethod
    def updateAccessTokenByRefreshToken(queryBody):
        headers = {
            'User-Agent': 'ozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Content-Type': 'application/json'
        }

        with requests.session() as session:
            response = session.post(headers=headers, url=updateAccesssTokenURL, data=queryBody)
            try:
                ret_obj = response.json()
                ret_obj = response.json()
                access_token = ret_obj.get("access_token")
                nick_name = ret_obj.get("nick_name")
                return nick_name, access_token
            except Exception as e:
                logging.error(f'错误信息: {e}')
                logging.error("token 无效或者已过期")
                exit(1)

    # 开始签到
    @staticmethod
    def sign_in(queryBody, nick_name, access_token):
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        with requests.session() as session:
            response = session.post(headers=headers, url=signinURL, data=queryBody)
            ret = response.json()
            if ret.get("success"):
                logging.info(f"恭喜 {nick_name} ! 签到成功!")
            else:
                logging.error("签到失败，请重新检查...")

    # 获取青龙里的 环境变量配置， 多账号请以 & 分隔， 如: 变量名:refreshToken 
    #                                                          值:xxx_1&xxx_2&xxx_3
    @staticmethod
    def getRefreshTokens():
        refreshTokens = os.getenv("refreshToken").split("&")
        if refreshTokens:
            logging.info(f'配置格式正确! 提供的 token 为: {refreshTokens}')
        else:
            logging.error("请按照要求配置 refreshToken 重跑本脚本")
        return refreshTokens

    # 主方法 把上面步骤有序组合起来
    @classmethod
    def main(cls):
        for refreshToken  in cls.getRefreshTokens():
            queryBody = {'grant_type':'refresh_token',
                         'refresh_token':refreshToken
                         }
            nick_name, access_token = cls.updateAccessTokenByRefreshToken(json.dumps(queryBody))
            cls.sign_in(json.dumps(queryBody), nick_name, access_token)

if __name__ == '__main__':
    AutoSignInTool.main()




