### What is main function of the software?
Plot the CSI value in real time to analyze data changing and facilitate CSI research.
The running figures is shown as below.
![rssi](https://github.com/luxiangx/CSIPlotter/blob/master/images/rssi.png)
![csi](https://github.com/luxiangx/CSIPlotter/blob/master/images/subcarrier.png)
![csi pair](https://github.com/luxiangx/CSIPlotter/blob/master/images/antenna.png)
![all csi](https://github.com/luxiangx/CSIPlotter/blob/master/images/all.png)

### What do you need to do before using?
- OS -- Ubuntu 12.04 or 14.04
- CSI tool -- Intel 5300
- sudo command -- password free
- python3 and some libs like matplotlib, QT5

### How to use it?
The mian UI with 4 parts is shown as below.

![ui](https://github.com/luxiangx/CSIPlotter/blob/master/images/ui.png)

#### UI Introduction
- 1 figure block

Show the RSSI or CSI data in different mode. The x axis is time axis. 
**Note that time is not the accurate time but depend on your computer performance.**
The y axis is depending on your mode. Maybe the RSSI or CSI subcarriers number or CSI amplitude or phase.
**Note the phase correction algorithm is referred the paper PADS of the Tsinghua University doctor Kun Qian.**
- 2 setting block

This block decides what kind of figure you want to show. The mode combobox contains rssi, subcarrier, antenna pair and all csi mode.
In the rssi mode, the below type, TX, RX and NO combobox is invalid which only shows the RSSI value in real time.
In the subcarrier mode, the figure shows the appointed TX-RX subcarrier amplitude or phase value.
**Note that when showing the CSI, the TX setting is essential. If your TX number is 3 please select C. If your TX number is 2 please select B.
If your TX number is only one please select A.** If you choose the wrong TX, you'll see the warning message.
In the antenna pair mode, the figure will show the appointed TX-RX 30 subcarriers amplitude or phase value. The TX is also important.
In the all csi mode, all the csi value will be shown. In this mode, the TX also can not be wrong.
The type combobox contains amplitude and phase which decides the showing data type. TX and RX combobox both contain three selections which are A, B and C. 
NO combobox contains 30 value from 1 to 30 represented the 30 subcarriers number. The rate combobox is to adjust the showing rate from 1 to 10000, though there is no difference between 1 and 10. 

- 3 file selecting block

Select the data path and file name.
- 4 control and message block

To start to show or pause and quit. Message box shows the running state.

#### steps to use it
1. Set the injection and monitor mode, ping is ok but I recommend this method.
2. Run ui.py.
3. Click the save-path button to select the saving directory and edit the file name.
4. Set the showing mode as you want.
5. Click the start to show, pause to puase and quit to quit.

### Bugs
1. When you run ui.py, and click start, forget to click pause of quit button, just terminate program with pycharm or other IDE stop button.
The log procedure will still run in backend. And when you run it again, it dose not working. The solution is that delete the logging file.
2. Due to my poor coding, the program is  inefficient. Some laptops with old hardware may not use it.

-------
The software is free to use for your research. If you find some bugs or want to join this project to improve the usability of the software, welcome to contact me.
My email is <luxiangisme@gmail.com>. 
