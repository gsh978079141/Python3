'''
Created on 2018年4月11日

@author: gdd
'''
import urllib.parse
import urllib.error
import urllib
import requests
import http.cookiejar
from imp import reload

# 登录斗鱼,url on linux
loginurl = 'http://www.douyu.com'

class LoginDouYu(object):
    def __init__(self):
        self.cookie = 'PHPSESSID=ivfa1s4107t0alfhjam0uqe782; acf_auth=a9fcuuCP9SBb3BrrqQ9A1BhvULFXHuXErwIEBz3%2B1Z03nHEOQpTTrXbsAvOhVXLr6VVfbDiE3AidF2dhM%2BZF7kiC0Gavq7POQOD9%2F989RjcikKmMVkX1%2FTm2oM6Y; wan_auth37wan=b271a80d8a79PYq8jy%2B0tpeQfiWvzK%2FPUwRufQIbdWyMKvb3Lq9ZryTqYBmvg2skD8E75D013bEwmzvllveOl9gutaKVNLqxf%2FA6j5%2FVTnN99JxE; acf_uid=3065097; acf_username=auto_wvchV41AHL; acf_nickname=QQ1126671091; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2F003%2F06%2F50%2F97_avatar_; acf_ct=0; acf_ltkid=46846941; acf_biz=1; acf_stk=182fd8243b91e685; acf_devid=5eeb6c7e532f114b052d38806b085993; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1491506694,1492008230; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1492008306; _dys_lastPageCode=page_live,page_home; _dys_refer_action_code=click_leftnavi_rank'

    def login(self):
        '''登录网站'''
        #loginparams = {'domain': self.domain, 'email': self.name, 'password': self.pwd}
        #req = urllib.request.Request(loginurl,  urllib.parse.urlencode(loginparams).encode(),headers=headers) # urlencode未,补充encode解决
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
            'cookie': self.cookie
        }
        req = urllib.request.Request(loginurl,headers=headers)
        response = urllib.request.urlopen(req)
        thePage = response.read().decode('utf-8')
        print('....ok')
        print(thePage)


if __name__ == '__main__':
    userlogin = LoginDouYu()
    userlogin.login()