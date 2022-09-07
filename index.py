# -*- coding: utf8 -*-

User=[
    {
        'app_id' : 'wx0788e6432f81f28d',
        'app_secret' : '80a7b2b7257ec426a54a99edf66c7906',
        '用户列表' : [
            {
                '用户ID' : 'oQr-K6LZgkY-sJEsOMy4qxNIXNmc',
                '模块ID' : 'G64Q-nG9Y8EdLD3XQwL9Nf0GaN-GXuZf3RzYwD4Uang',
                '省份' : '贵州',#对应另一个文件查找
                '城市' : '贵阳',#对应另一个文件查找
                '生日' : {
                    '妈妈':'1978-9-11',
                    '弟弟':'2003-12-2',
                },
            },
        ]
    },
]

import requests,time,datetime,ChengShi_id,random

def 生日距离天数计算(生日):
    生日 = 生日.split('-')
    dq=datetime.date.today()
    js=datetime.date(dq.year,int(生日[1]),int(生日[2]))
    if dq>js:
        js=datetime.date(dq.year+1,int(生日[1]),int(生日[2]))
        a = (js-dq).days
    elif dq<js:
        a = (js-dq).days
    else:
        a = '今天生日诶'
    print('距离天数：%s'%a)
    return a

def 获取天气数据(城市id):
    headers = {
        'Referer': 'http://www.weather.com.cn/weather1d/%s.shtml'%城市id,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = 'http://d1.weather.com.cn/dingzhi/%s.html?_=%s'%(城市id,str(int(time.time() * 1000)))
    print(url)
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    print(r.text)
    return eval(r.text.split(';')[0].split('=')[1])['weatherinfo']

def 发送消息(app_id,app_secret,用户):
    显示内容=''
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(app_id,app_secret)
    print('url' + url)
    access_token = requests.get(url).json()['access_token']
    print('登录令牌：' + access_token)
    
    week_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六','星期日']
    时间=time.strftime('%Y年%m月%d日 %H:%M:%S（' + week_list[datetime.date.today().isoweekday()-1] + '）',time.localtime((int(time.mktime(time.gmtime()))+28800)))
    
    天气list = 获取天气数据(ChengShi_id.中国[用户['省份']][用户['城市']]['AREAID'])
    天气情况 = 天气list['weather']
    最高气温 = 天气list['temp']
    最低气温 = 天气list['tempn']

    for 生日 in list(用户['生日'].keys()):
        用户['生日'][生日]=生日距离天数计算(用户['生日'][生日])

    r = requests.get('http://open.iciba.com/dsapi/').json()
    英文文案=r['content']
    中文文案=r['note']

    r = requests.get('https://www.d5168.com/m/nongli.php',headers={'User-Agent':''},verify=False).text
    a=r.find('今日农历：')
    b=r.find('</font>',a)
    今日农历 = r[a:b]
    a=r.find('<p class="hm">')
    b=r.find('</p>',a)
    今日农历 += ' ' + r[a+14:b]
    

    print(用户['用户ID'])
    print(用户['模块ID'])
    print(用户['城市'])
    data = {
        'touser': 用户['用户ID'],
        'template_id': 用户['模块ID'],
        'url':'https://broccoli.uc.cn/apps/pneumonia/routes/index?uc_param_str=dsdnfrpfbivesscpgimibtbmnijblauputogpintnwktprchmt&uc_biz_str=S%3Acustom%7COPT%3AS_BAR_BG_COLOR%40f7f7f7%7COPT%3ATOOLBAR_STYLE%401%7COPT%3ABACK_BTN_STYLE%400&entryrtne=jiejing&tab=fromsource',
        'topcolor': '#FF0000',
        'data': {
        }
    }
    显示内容+='辛会 早呀~~\n\n'
    显示内容+='今日公历：%s\n%s\n\n'%(时间,今日农历)
    显示内容+='城市：%s\n\n'%用户['城市']
    显示内容+='天气情况：%s\n\n'%天气情况
    显示内容+='最低气温：%s\n\n'%最低气温
    显示内容+='最高气温：%s\n\n'%最高气温
    for 生日 in list(用户['生日'].keys()):
        显示内容+='距离%s的生日还有：%s天\n'%(生日,用户['生日'][生日])
    显示内容+='\n'+英文文案+'\n'+中文文案+'\n'
    显示内容list=显示内容.split('\n')
    for a in range(len(显示内容list)):
        data['data']['date%s'%a]={}
        data['data']['date%s'%a]['value']=显示内容list[a]
        data['data']['date%s'%a]['color']='#' + '%06x' % random.randint(0, 0xFFFFFF)
    print(str(data))
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token
    r = requests.post(url, headers=headers, json=data)
    print(r.text)

for 客户 in User:
    for 用户 in 客户['用户列表']:
        发送消息(客户['app_id'],客户['app_secret'],用户)
