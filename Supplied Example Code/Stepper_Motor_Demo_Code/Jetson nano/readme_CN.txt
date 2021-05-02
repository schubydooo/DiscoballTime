/*****************************************************************************
* | File      	:   Readme_CN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2019-06-25
* | Info        :   在这里提供一个中文版本的使用文档，以便你的快速使用
******************************************************************************/
这个文件是帮助您使用本例程。

1.基本信息：
本例程是基于jetson-nano-sd-r32.1.1-2019-05-31系统镜像而开发的。
本例程是基于Jetson Nano进行开发的，例程均在Jetson Nano上进行了验证;
本例程使用Stepper Motor HAT模块进行了验证。

2.管脚连接：
管脚连接你可以在DRV8825.py或者config.h中查看，这里也再重述一次：
OLED        =>    Jetson Nano/RPI(BCM)
VCC         ->      3.3
GND         ->      GND
M1_ENABLE   ->      12
M1_DIR      ->      13
M1_STEP     ->      19
M1_M0       ->      GND
M1_M1       ->      GND
M1_M2       ->      GND

M2_ENABLE   ->      4
M2_DIR      ->      24
M2_STEP     ->      18
M2_M0       ->      GND
M2_M1       ->      GND
M2_M2       ->      GND

3.基本使用：
由于本工程是一个综合工程，对于使用而言，你可能需要阅读以下内容：
安装对应的库GPIO
python2
    sudo apt-get install python-pip
    sudo pip install Jetson.GPIO
    sudo groupadd -f -r gpio
    sudo usermod -a -G gpio your_user_name
    vsudo udevadm control --reload-rules && sudo udevadm trigger
python3
    sudo apt-get install python-pip3
    sudo pip3 install Jetson.GPIO
    sudo groupadd -f -r gpio
    sudo usermod -a -G gpio your_user_name
    sudo udevadm control --reload-rules && sudo udevadm trigger

然后你需要执行：
C:
    编译: make
    运行: sudo ./main
python2
    运行：sudo python main.py
python3
     运行：sudo python3 main.py
