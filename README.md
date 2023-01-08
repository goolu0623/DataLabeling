# VibrationLabeler

From https://github.com/goolu0623/CrossHaptics you can generate and saved the vibration signals data via polling OpenVr api during the gameplay.

Use the Preprocess.py to deal with the console.txt and modified the log format into what we want to focus on, which is vibration signals, and saved to the chosen directory.
Use the main.py to start the labeler which can interact with your vibration signals.
UI design as below. 
Apply button: switch to the "start" and "end" frame and browse the data and gameplay record.
graph type: can switch the signal data type into different vibration signals.
record: can save the event that happend now with the "start" and "end" frame as the contents into the events.txt and the figures in the same time.
![image](https://user-images.githubusercontent.com/69243118/202837833-ac2eb24d-1fbd-4f6d-bd2a-691564f6aba6.png)
