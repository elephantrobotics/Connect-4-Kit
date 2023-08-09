---
sidebar_position: 2
---

# Running the Program

## Windows

Open any terminal program in the project directory and enter the following command:

> You can quickly open the terminal at the current location by holding Shift and right-clicking on a blank area in the folder, then selecting "Open PowerShell here."

```bash
python app.py
```

1. First, select the serial port, and after making your selection, click "Start" and wait for the robotic arm to establish a connection.
2. Next, choose the camera; typically, it's either 0 or 1. Then, check the boxes for **Default Video Stream**, **Grayscale Stream**, and **Recognition Annotated Video Stream**. Finally, click "Start" and patiently wait for the camera to initiate. This process might take around ten seconds.
3. Click "Start Game" to begin playing.
4. If a winner emerges, the robotic arm will return to its original position. The player will be notified of the game's conclusion through the GUI.

> Note: By default, the robot plays as the second player, which means the yellow pieces should be placed in the chess bucket. The player takes the red pieces. If you choose the robot to play first, then red pieces should be placed in the chess bucket, and the player will use the yellow pieces.

![](attachment/2023-07-12-18-39-07.png)

## Linux(Pi version)

Open any terminal program in the project directory and enter the following command:

```bash
python3.11 app.py
```
