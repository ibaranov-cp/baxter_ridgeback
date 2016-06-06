#!/usr/bin/env python

import roslib
import rospy
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from baxter_core_msgs.msg import HeadPanCommand
from std_msgs.msg import Bool
from sensor_msgs.msg import Joy

#Used to prevent robot drifting around
deadzone = 0.01
kill = 0

#Low pass moving average
avg = 3
x = [0]*avg
y = [0]*avg
z = [0]*avg
cnt = 0

def callback(data):
    global x
    global y
    global z
    global cnt
    x[cnt] = ((data.effort[3] + 6.3) + (data.effort[10] + 6.3))*0.01;
    y[cnt] = ((data.effort[6]) + (data.effort[13]))*0.01; 
    z[cnt] = (-(data.effort[3] + 6.3) + (data.effort[10] + 6.3))*0.01;
    #print x
    #print y
    #print z
    cnt = cnt + 1
    if cnt > (avg-1): cnt =0
    #We really only care about the bellow topics
    #print "left_e1:" + str(data.effort[3]) + " left_w0:" + str(data.effort[6]) + " right_e1:" + str(data.effort[10]) + " right_w0:" + str(data.effort[13])

def avg_arr(arr):
    ret = 0
    for j in range(0, avg):
        ret = ret + arr[j]
    return ret/avg

def safety(data):
    global kill
    kill = 1
    if data.axes[14] <0: kill = 1
    if data.buttons[14]==1: kill = 0
	

def limiter(val, limit):
    if val > limit: val = limit
    if val < -limit: val = -limit
    if abs(val) < deadzone: val = 0
    if kill == 1: val = 0
    return val

def accel(val,rate,up,down):
    if abs(rate) < deadzone:
        val = val - val/down
    else:
        val = val + rate/up
    return val

def ballroom():
    rospy.init_node('ballroom', anonymous=True)

    #Listen to arm joints of the Baxter
    rospy.Subscriber("/robot/joint_states", JointState, callback)
    rospy.Subscriber("/bluetooth_teleop/joy", Joy, safety)
    #Publish data to the ridgeback
    pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    cmd = Twist()
    #Publish head commands to Baxter
    pub_head_pan = rospy.Publisher('/robot/head/command_head_pan', HeadPanCommand, queue_size=1)
    pub_head_nod = rospy.Publisher('/robot/head/command_head_nod', Bool, queue_size=1)
    pan = HeadPanCommand()
    pan.speed = 100 

    rate = rospy.Rate(10) # 10hz

    #both e1 more negative = +x vel
    #both e1 more positive = -x vel
    #both w0 more negative = -y vel (robot left, baxter right)
    #both w0 more positive = +y vel (robot right, baxter left)
    #right e1 negative, left e1 positive = -z rotation
    #left e1 positive, right e1 negative = +z rotation

    while not rospy.is_shutdown():
        rate.sleep()        

        #The lower the up and down terms are, the faster it accelerates
        cmd.linear.x = accel(cmd.linear.x,avg_arr(x),4,6)
        cmd.linear.y = accel(cmd.linear.y,avg_arr(y),3,4)
        cmd.angular.z = accel(cmd.angular.z,avg_arr(z),2,2)

	#Prevent mortal injury through speed & drift, number is max speed in m/s or rad/s
        cmd.linear.x = limiter(cmd.linear.x,0.3)
        cmd.linear.y = limiter(cmd.linear.y,0.3)
        cmd.angular.z = limiter(cmd.angular.z,0.4)

        pub_vel.publish(cmd)
	print cmd

        pan.target = cmd.angular.z*2
        pub_head_pan.publish(pan)
        #pub_head_nod.publish(1)



if __name__ == '__main__':
    ballroom()

