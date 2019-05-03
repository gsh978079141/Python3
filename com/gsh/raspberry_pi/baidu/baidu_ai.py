# baidu_ai.py 文件内容
from aip import AipSpeech
import pygame
import pyaudio
import wave
import os

# 音频文件存储默认路径
BASE_PATH = "./audio/"
# 录音文件名
OUTPUT_WAV = "output.wav"
# 这里的三个参数,对应在百度语音创建的应用中的三个参数
APP_ID = "15823516"
API_KEY = "MpIxVxN43QTPmcrRM0bxnO5Z"
SECRET_KEY = "3McX8d975fMftR89w79pIgTHDV4B1fiS"

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 语音识别
def audio_to_text():
    voice_to_audio()
    pcm_file = wav_to_pcm()
    # 读取文件(PCM格式)
    with open(pcm_file, 'rb') as fp:
        file_context = fp.read()

    # 识别本地文件
    res = client.asr(file_context, 'pcm', 16000, {
        'dev_pid': 1536,
    })

    # 从字典里面获取"result"的value 列表中第1个元素
    try:
        res_str = res.get("result")[0]
    except TypeError:
        res_str = "请说话"
    return res_str


# 语音合成
def text_to_audio(res_str, mp3_file_name):
    synth_file = mp3_file_name
    synth_context = client.synthesis(res_str, "zh", 1, {
        "vol": 5,
        "spd": 4,
        "pit": 9,
        "per": 3
    })

    with open(BASE_PATH + synth_file, "wb") as f:
        f.write(synth_context)

    return synth_file


# 语音播报
def voice_broadcast(mp3_file_path):
    # S 其他播报
    file = r'%s%s' % (BASE_PATH, mp3_file_path)
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while True:
        # pygame.mixer.music.get_busy() 判断是否在播放音乐, 返回1为正在播放。
        if pygame.mixer.music.get_busy() == 0:
            break
        # 未来四天天气变化图
    # E 其他播报


# 音频保存wav文件
def voice_to_audio():
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    # 录音时间
    RECORD_SECONDS = 2
    # 创建PyAudio对象
    p = pyaudio.PyAudio()

    # 打开数据流
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    # 停止数据流
    stream.stop_stream()
    stream.close()

    # 关闭PyAudio
    p.terminate()

    # 写入录音文件
    wf = wave.open(BASE_PATH + OUTPUT_WAV, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# wav文件装pcm
def wav_to_pcm():
    wav_file = OUTPUT_WAV
    BASE_PRO_PATH = "~/github/Python3/com/gsh/raspberry_pi/audio/"
    # 假设 wav_file = "音频文件.wav"
    # wav_file.split(".") 得到["音频文件","wav"] 拿出第一个结果"音频文件"  与 ".pcm" 拼接 等到结果 "音频文件.pcm"
    pcm_file = "%s.pcm" % (wav_file.split(".")[0])
    # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
    os.system("ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s" % (BASE_PRO_PATH+wav_file, BASE_PRO_PATH+pcm_file))
    return BASE_PATH+pcm_file
