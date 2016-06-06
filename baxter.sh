#Specific to Baxter Demo!!
# Kill roscore on ridgeback (sudo service ros stop), do both exports, roslaunch base.launch
export ROS_MASTER_URI=http://192.168.131.3:11311
export ROS_IP=192.168.131.1
rosrun baxter_tools enable_robot.py -e 
./xdisplay_image.py -f face.png
 rosrun baxter_examples xdisplay_image.py -f=face.png
rosrun baxter_examples joint_position_file_playback.py -f pose.txt -l 0
./baxter_ridgeback.py
