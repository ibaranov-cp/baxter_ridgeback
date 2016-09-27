# baxter_ridgeback
Ballroom dancing demo with the Ridgeback and Baxter robots.

### Quickstart Guide:
1. Ridgeback is at 192.168.131.1, Baxter is at 192.168.131.3 (configured in Baxter boot up menu). Baxter is ethernet wired to Ridgeback. As we cannot change code on Baxter, we have to modify Ridgeback to use Baxter ROScore
2. SSH into Ridgeback (IP 192.168.0.138 for CASE), start `screen` session. In the first screen window, execute `sudo service ros stop`
3. execute `export ROS_MASTER_URI=http://011310P0010:11311` (your /etc/hosts file should contain the IP assosicated with the net name of the Baxter)
4. execute `export ROS_IP=192.168.131.1` then execute `roslaunch ridgeback_base base.launch --screen` (starts Ridgeback base modules with Baxter as the master)
5. start new screen windows (`Ctrl+a then c`), ssh ruser@011310P0010 (password `rethink`)
6. execute `rosrun baxter_tools enable_robot.py -e` then execute `rosrun baxter_examples xdisplay_image.py -f=face.png` then execute `rosrun baxter_tools tuck_arms.py -u`
7. execute `rosrun baxter_examples joint_position_file_playback.py -f pose.txt -l 0`
8. start new screen windows (`Ctrl+a then c`), do steps 3. 4., then execute `./baxter_ridgeback.py`
9. you can now drive Ridgeback normally by holding down (L1), or let ballroom work by holding down (X)
10. After demo, kill everything in every windows (`Ctrl+c`). To tuck arms after demo for packing, on the ssh session with Baxter, execute `rosrun baxter_tools tuck_arms.py -t`
