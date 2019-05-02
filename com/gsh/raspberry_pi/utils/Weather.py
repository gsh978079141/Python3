# 导入必要模块
import urllib.parse
import urllib.request
import gzip
import json
from aip import AipSpeech
import matplotlib.pyplot as plt
import re
import baidu.baidu_ai as baiduAi
# 设置参数，图片显示中文字符，否则乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
BASE_PATH = "./"
BROADCAST_MP3 = "broadcast.mp3"

# 定义获取天气数据函数
def Get_weather_data():
    # print('------天气查询------')
    # city_name = input('请输入要查询的城市名称：')
    city_name = "常州"
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + urllib.parse.quote(city_name)
    weather_data = urllib.request.urlopen(url).read()
    # 读取网页数据
    weather_data = gzip.decompress(weather_data).decode('utf-8')
    # #解压网页数据
    weather_dict = json.loads(weather_data)
    return weather_dict


# 定义当天天气输出格式
def Show_weather(weather_data):
    weather_dict = weather_data
    if weather_dict.get('desc') == 'invilad-citykey':
        print('你输入的城市有误或未收录天气，请重新输入...')
    elif weather_dict.get('desc') == 'OK':
        forecast = weather_dict.get('data').get('forecast')
        riqi = forecast[0].get('date')
        city = weather_dict.get('data').get('city')
        type = forecast[0].get('type')
        wendu = weather_dict.get('data').get('wendu') + '℃ '
        high = forecast[0].get('high')
        low = forecast[0].get('low')
        fengxiang = forecast[0].get('fengxiang')
        ganmao = weather_dict.get('data').get('ganmao')
        print('日期：', riqi)
        print('城市：', city)
        print('天气：', type)
        print('温度：', wendu)
        print('高温：', high)
        print('低温：', low)
        try:
            fengli = forecast[0].get('fengli').split('<')[2].split(']')[0]
        except:
            fengli = forecast[0].get('fengli').split('[')[2].split(']')[0]
        print('风级：', fengli)
        print('风向：', fengxiang)
        weather_forecast_txt = '您好，您所在的城市%s,' \
                               '天气%s,' \
                               '当前温度%s，' \
                               '今天最高温度%s，' \
                               '最低温度%s，' \
                               '风级%s，' \
                               '温馨提示：%s' % \
                               (
                                   city,
                                   type,
                                   wendu,
                                   high,
                                   low,
                                   fengli,
                                   ganmao
                               )
        return weather_forecast_txt, forecast


# 定义语音播报今天天气状况
def Voice_broadcast(weather_forcast_txt):
    weather_forecast_txt = weather_forcast_txt
    print('语音提醒：', weather_forecast_txt)
    # 百度语音合成
    baiduAi.text_to_audio(weather_forecast_txt,BROADCAST_MP3)
    # result = client.synthesis(weather_forecast_txt, 'zh', 1, {'vol': 5,'per': 3,'spd':4})
    # if not isinstance(result, dict):
    #     with open(BROADCAST_MP3, 'wb') as f:
    #         f.write(result)
    #         f.close()

    # ####playsound模块播放语音
    # playsound(r'/github/Python3/com/gsh/raspberry_pi/broadcast.mp3')
    # S 其他播报
    # file = r'%s%s' % (BASE_PATH, BROADCAST_MP3)
    # pygame.mixer.init()
    # track = pygame.mixer.music.load(file)
    # pygame.mixer.music.play()
    # while True:
    #     # pygame.mixer.music.get_busy() 判断是否在播放音乐, 返回1为正在播放。
    #     if (pygame.mixer.music.get_busy() == 0):
    #         start()
    #         break
    #     # 未来四天天气变化图
    # E 其他播报
    # 百度播报
    baiduAi.voice_broadcast(BROADCAST_MP3)


# 画图
def Future_weather_states(forecast):
    future_forecast = forecast
    dict = {}
    # 获取未来四天天气状况
    for i in range(5):
        data = []
        date = future_forecast[i]['date']
        date = int(re.findall('\d+', date)[0])
        data.append(int(re.findall('\d+', future_forecast[i]['high'])[0]))
        data.append(int(re.findall('\d+', future_forecast[i]['low'])[0]))
        data.append(future_forecast[i]['type'])
        dict[date] = data
    data_list = sorted(dict.items())
    date = []
    high_temperature = []
    low_temperature = []
    for each in data_list:
        date.append(each[0])
        high_temperature.append(each[1][0])
        low_temperature.append(each[1][1])
    fig = plt.plot(date, high_temperature, 'r', date, low_temperature, 'b')
    plt.xlabel('日期')
    plt.ylabel('℃')
    plt.legend(['高温', '低温'])
    plt.xticks(date)
    plt.title('最近几天温度变化趋势')
    plt.show()


# 识别开始
def start():
    weather_data = Get_weather_data()
    weather_forecast_txt, forecast = Show_weather(weather_data)
    # Future_weather_states(forecast)
    Voice_broadcast(weather_forecast_txt)



