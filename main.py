# -*- coding = utf-8 -*-
# @Time : 2021/1/24 0:27
# @Auther : cmodog
# @File : main.py
# @Software: PyCharm

import os
import requests
from bs4 import BeautifulSoup

PUSH_KEY = os.environ["PUSH_KEY"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]


HEADER_GET = {
    "user-agent": "Mozilla/5.0 (Linux; Android 11; Mi 10 Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.185 Mobile Safari/537.36/lenovoofficialapp/16112154380982287_10181446134/newversion/versioncode-124/"
}

HEADER_COUNT = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
}

def login() -> (requests.session, str):       #登录过程
    url = "https://reg.lenovo.com.cn/auth/v3/dologin"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Host": "reg.lenovo.com.cn",
        "Referer": "https://www.lenovo.com.cn/",
        'Cookie': 'LA_F_T_10000001=1614393605462; LA_C_Id=_ck21022710400514675618549440548; LA_M_W_10000001=_ck21022710400514675618549440548%7C10000001%7C%7C%7C; LA_C_C_Id=_sk202102271040090.05206000.3687; _ga=GA1.3.1245350653.1614393605; leid=1.VljlpE1LZ7I; LA_F_T_10000231=1614395016398; LA_R_T_10000231=1614395016398; LA_V_T_10000231=1614395016398; LA_M_W_10000231=_ck21022710400514675618549440548%7C10000231%7C%7C%7C; LA_R_C_10000001=1; LA_R_T_10000001=1614593722192; LA_V_T_10000001=1614593722192; _gid=GA1.3.1974081891.1614593723; _gat=1; ar=1'
    }
    data = {"account": USERNAME, "password": PASSWORD, "ticket": "e40e7004-4c8a-4963-8564-31271a8337d8"}
    session = requests.Session()
    r = session.post(url,headers=header,data=data)
    if r.text.find("cerpreg-passport") == -1:       #若未找到相关cookie则返回空值
        return None
    return session

def getContinuousDays(session):
    url = "https://club.lenovo.com.cn/signlist/"
    c = session.get(url,headers=HEADER_COUNT)
    soup = BeautifulSoup(c.text,"html.parser")
    day = soup.select("body > div.signInMiddleWrapper > div > div.signInTimeInfo > div.signInTimeInfoMiddle > p.signInTimeMiddleBtn")
    day = day[0].get_text()
    url_push = "https://sc.ftqq.com/%s.send"%PUSH_KEY
    push_data = {
        "text":"联想商城签到情况：%s"%day
    }
    push = requests.post(url_push,data=push_data)
    return day,push.text


def signin(session):
    signin = session.get("https://i.lenovo.com.cn/signIn/add.jhtml?sts=e40e7004-4c8a-4963-8564-31271a8337d8",headers=HEADER_GET)
    check = str(signin.text)
    if "true" in check:
        if "乐豆" in check:
            print("签到成功")
        else:
            print("请不要重复签到")
    else:
        print("签到失败，请重试")

if __name__ == '__main__':
    s = login()
    if not s:
        print("登录失败，请检查账号密码")
    else:
        signin(s)
        print(getContinuousDays(s))
