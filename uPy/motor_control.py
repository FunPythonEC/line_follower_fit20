import uros
from std_msgs import Int16  # rosserial messages
from machine import Pin
import utime
import gc
gc.enable()

class MotorControl(
    object
):
    def __init__(self):

        # constants
        self.error_topic = "/motors_pwr"
	self.vel = 10
	
	#motor1
	self.ENA = Pin(13,Pin.OUT)
	self.IN1 = Pin(12,Pin.OUT)
	self.IN2 = Pin(14,Pin.OUT)
	self.ena_pwm=machine.PWM(self.ENA)

    	self.ena_pwm.freq(1000)
    	self.ena_pwm.duty(self.vel)

	#motor2
	self.ENB = Pin(25,Pin.OUT)
	self.IN3 = Pin(27,Pin.OUT)
	self.IN4 = Pin(26,Pin.OUT)
	self.enb_pwm=machine.PWM(self.ENB)
	self.enb_pwm.freq(1000)
    	self.enb_pwm.duty(self.vel)

    def turn_right(self):
	self.IN1.value(1)
	self.IN2.value(0)
	self.IN3.value(0)
	self.IN4.value(0)

    def turn_left(self):
	self.IN1.value(0)
	self.IN2.value(0)
	self.IN3.value(1)
	self.IN4.value(0)

    def stop(self):
	self.IN1.value(0)
	self.IN2.value(0)
	self.IN3.value(0)
	self.IN4.value(0)

    def go_straight(self):
	self.IN1.value(1)
	self.IN2.value(0)
	self.IN3.value(1)
	self.IN4.value(0)
	
    def error_callback(self, msg):
        pos_err =  msg.data
        if pos_err<-5:
		self.turn_left()
	if pos_err>5:
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


