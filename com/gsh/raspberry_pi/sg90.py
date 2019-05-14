import RPi.GPIO as GPIO
import time
import signal
import atexit

atexit.register(GPIO.cleanup)

servopin = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
p = GPIO.PWM(servopin, 50)  # 50HZ
p.start(0)
time.sleep(2)

# while (True):
#     for i in range(0, 181, 10):
#         p.ChangeDutyCycle(2.5 + 10 * i / 180)  # 设置转动角度
#         time.sleep(0.02)  # 等该20ms周期结束
#         p.ChangeDutyCycle(0)  # 归零信号
#         time.sleep(0.2)
#
#     for i in range(181, 0, -10):
#         p.ChangeDutyCycle(2.5 + 10 * i / 180)
#         time.sleep(0.02)
#         p.ChangeDutyCycle(0)
#         time.sleep(0.2)
p.ChangeDutyCycle(2.5 + 10 * 1 / 180)  # 设置转动角度
# time.sleep(0.02)  # 等该20ms周期结束
# p.ChangeDutyCycle(0)  # 归零信号
# time.sleep(0.2)

