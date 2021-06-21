from flask import Flask, Response,render_template
import pyaudio
import wave

app = Flask(__name__)

RECORD_SECONDS = 5
CHUNK = 1024  # 定义数据流块
FORMAT = pyaudio.paInt16  # 量化位数（音量级划分）
CHANNELS = 2  # 声道数;声道数：可以是单声道或者是双声道
RATE = 44100  # 采样率;采样率：一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz


audio1 = pyaudio.PyAudio()



def genHeader(sampleRate, bitsPerSample, channels,samples):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o


@app.route('/audio')
def audio():
    # start Recording
    def sound():
        sampleRate = 44100
        bitsPerSample = 16
        wav_header = genHeader(sampleRate, bitsPerSample, CHANNELS)
        stream = audio1.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
        print("recording...")
        frames = []
        while True:
            data = wav_header+stream.read(CHUNK)

            yield(data)

    return Response(sound())


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def test():
    # 要写入的文件名
    WAVE_OUTPUT_FILENAME = "output.wav"
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
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    app.run(host='192.168.112.51', debug=True, threaded=True,port=5000)