import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ENA = 16
ENB = 18
INT1 = 11
INT2 = 12
INT3 = 13
INT4 = 15
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(INT1, GPIO.OUT)
GPIO.setup(INT2, GPIO.OUT)
GPIO.setup(INT3, GPIO.OUT)
GPIO.setup(INT4, GPIO.OUT)
####PWM初始化，并设置频率为200HZ####
# 初始化
GPIO.setup(ENA, GPIO.OUT)
# 200HZ
p1 = GPIO.PWM(ENA, 200)
p1.start(40)  # 产生占空比为0.4的PWM信号，取值范围0-100


#########定义电机正转函数##########
def gogo():
    print('正转')
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.HIGH)


#########定义电机反转函数##########
def back():
    print('反转')
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.HIGH)


#########定义电机停止函数##########
def stop():
    print('停止转动')
    GPIO.output(ENA,GPIO.LOW)
    p1.stop  # 停止PWM信号
    GPIO.output(ENB, GPIO.LOW)
    GPIO.output(INT1, GPIO.LOW)
    GPIO.output(INT2, GPIO.LOW)
    GPIO.output(INT3, GPIO.LOW)
    GPIO.output(INT4, GPIO.LOW)


'''
整个实验是
正转10.5s
反转10.5s
'''
while True:
    gogo()
    time.sleep(3)
    stop()
    time.sleep(3)
    back()
    time.sleep(3)
    action = input('是否继续？Y/N')
    if action == 'n':
        GPIO.cleanup()
        exit()
