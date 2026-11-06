# The-Effects-of-Robots-on-Perceived-Surveillance

A Wizard-of-Oz (WOZ) interface for a NAO robot with interactable buttons to turn left, middle, and right alongside a camera to view the real-time feed of the NAO robot's forehead camera.

## System requirements
The code is built and tested with Python 3.14.7 on Linux 6.8.0-147.

You can download Python using [the Official Python Downloads](https://www.python.org/downloads/) page.

## Installation guide 
1. pull the repository from the github page and navigate to the folder 
```
git clone https://github.com/WarrenKTan/The-Effects-of-Robots-on-Perceived-Surveillance.git
cd The-Effects-of-Robots-on-Perceived-Surveillance
```
2. Download the requirements
```
pip install qi==3.1.5
pip install pillow==13.0.0
```
3. Run the Python code

Linux
```
python3 nao_woz_gui.py
```

## Program Features
### Connecting to the NAO robot
Components will not function as intended without a connection to a NAO robot. To connect the robot to the program, input the NAO robot's IP address into the "Enter the Robot's IP:" text box.

Upon a successful connection, the NAO robot will say "Connected to Nao" and move to the sitting position. The camera will also start its real-time feed of the NAO robot.

### Buttons
- clicking the "Look Left" button will turn the NAO robot's head to a preset angle of 20 degrees left of the middle position.
- clicking the "Look Right" button will turn the NAO robot's head to a preset angle of 20 degrees right of the middle position.
- clicking the "Look Middle" button will reset the NAO robot's head to the middle position, 0 degrees.

### Camera
- After connecting to the robot, the camera will begin to display the real-time feed of where the NAO robot is facing.
- This is used in the experiment to know when to swap the robot's head position

## Video Demonstration
<https://github.com/user-attachments/assets/4e8610a8-2391-4b83-a2c7-44bf0fd99a07>