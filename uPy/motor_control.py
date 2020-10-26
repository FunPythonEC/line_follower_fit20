import uros
from std_msgs import Int16  # rosserial messages
from machine import Pin, PWM
import machine
import utime
import gc
gc.enable()

class MotorControl(
    object
):
    def __init__(self):

        # constants
        self.error_topic = "/motors_pwr"
	self.node = uros.NodeHandle(2, 115200, tx=17, rx=16)
	
	#motor1
	self.ENA = PWM(Pin(2), freq=20000, duty=620)
	self.IN1 = Pin(12,Pin.OUT)
	self.IN2 = Pin(14,Pin.OUT)

	#motor2
	self.ENB = PWM(Pin(0), freq=20000, duty=620)
	self.IN3 = Pin(27,Pin.OUT)
	self.IN4 = Pin(26,Pin.OUT)

	self.stop()

    def turn_right(self):
	self.IN1.value(0)
	self.IN2.value(0)
	self.IN3.value(0)
	self.IN4.value(1)

    def turn_left(self):
	self.IN1.value(1)
	self.IN2.value(0)
	self.IN3.value(0)
	self.IN4.value(0)

    def stop(self):
	self.IN1.value(0)
	self.IN2.value(0)
	self.IN3.value(0)
	self.IN4.value(0)

    def go_straight(self):
	self.IN1.value(1)
	self.IN2.value(0)
	self.IN3.value(0)
	self.IN4.value(1)
	
    def error_callback(self, msg):
        pos_err =  msg.data
	print(pos_err)
        if pos_err<-0:
		self.turn_left()
	if pos_err>0:
		self.turn_right()
	else:
		self.go_straight()


    def start(self):
        self.node.subscribe(self.error_topic, Int16, self.error_callback)
        while True:
            pass

def start_robot():
	robot = MotorControl()
	robot.start()
def test():
	robot = MotorControl()
	robot.go_straight()
	utime.sleep(4)
	robot.stop()

	


