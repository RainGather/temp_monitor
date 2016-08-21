# 作用
用来检测室内温度，一旦超过设置温度，就报警发送email，可以在手机端接收警报。


# 所需设备

以下设备是作者所购的型号和地址，有些相似设备或不同淘宝店购买的设备可能也可以兼容，但也有可能需要做一些修改才可以正常使用。如果你是新手，推荐购买和作者一样的设备，来保证最优兼容性。

* 1 x 树莓派3代B型 Raspberry Pi Model 3 B

    https://detail.tmall.com/item.htm?id=527595656123&spm=a1z09.2.0.0.cXUn6z&_u=l3509pv587b

* 2 x 树莓派散热片

    https://detail.tmall.com/item.htm?id=44626559422&spm=a1z09.2.0.0.cXUn6z&_u=l3509pv996a

* 2 x DHT11 温湿度传感器 (抱歉，虽然1片就可以了，但是被我代码写死了两片。。暂时懒得改。。)

    https://detail.tmall.com/item.htm?id=41248630584&ali_refid=a3_430583_1006:1109983619:N:DHT11:f42e6410295417d5b6e7b061f4b0d8ce&ali_trackid=1_f42e6410295417d5b6e7b061f4b0d8ce&spm=a230r.1.14.1.8WCr34

* 诺干杜邦线 (母头对母头)

    https://item.taobao.com/item.htm?spm=a1z10.3-c.w4002-10831283312.16.I525lp&id=27288768846

* 一张4G以上的TF卡 (Mini SD卡，淘宝随便找下)
* 一个支持HDMI输入的显示设备
* 一根HDMI双公头线
* USB鼠标和键盘
* 一根Android手机通用充电线


# 安装树莓派系统

在树莓派官网下载树莓派的系统镜像(下载Full desktop image based的)：
https://www.raspberrypi.org/downloads/raspbian/

下载镜像烧入工具win32diskimager：
https://sourceforge.net/projects/win32diskimager/

用读卡器接上格式化成FAT32的TF卡，并用win32diskimager将系统镜像烧入到该卡中。

完成后，将树莓派接上HDMI显示器、USB键盘鼠标和电源线，电源可以用Android手机充电器供电，也可以用电视机、电脑上的USB口供电。

接上电源后查看HDMI显示器，如稍后出现开机画面则说明一切已准备就绪。


# 接线

将树莓派关机并拔掉电源

这里有树莓派的针脚说明图（方向是将树莓派拿手上，针脚排靠右上方）：
https://coding.net/u/raingather/p/temp_monitor/git/blob/release/GPIO_Pi2_e14.png

图中，3.3V和5V的意思就是正极3.3V和5V，Ground的意思是负极（接地），其余类似GPIO02, GPIO15之类的针脚，是信号针脚，GPIO之后的数字意思是针脚号码。

将DHT11的温湿度传感器的正极接在随意一个3.3V针脚上，负极接在随意一个Ground针脚上。两个都接好。之后分别将两个DHT11温湿度传感器的数据线接在某个GPIO的针脚，记下两个针脚的号码。我接的是GPIO2和GPIO10。

接通电源前一定要反复确认没有接错针脚，有时候电压过高、短路、正负极接错等会导致传感器或设备烧毁甚至短路燃烧。


# 安装软件


1. 注册一个Email，推荐163的。注册好后在设置里开通POP3和SMTP服务，有些邮箱开通服务后，会有一个（或让你设置一个）独立的密码，记住这个密码，待会儿要用。如果没有独立密码那就是邮箱的登陆密码。

2. 接通树莓派电源，进入桌面后打开命令行窗口，在里面输入：

>如果你在国内：
>
> git clone https://git.coding.net/raingather/temp_monitor.git
>
>如果你在国外：
>
> git clone https://github.com/scaldstack/temp_monitor.git

3. 修改配置文件：
用文件浏览器打开home目录下temp_monitor目录，会看见里面有很多文件。将temp_monitor.cfg.sample重命名成temp_monitor.cfg，然后按照里面的格式，修改成刚刚注册的邮箱(send_email)、SMTP服务器地址(smtp)、密码（passwd, 就是1.里面说的那个密码）、温湿度传感器的针脚号码(temp1_pin, temp2_pin)、警戒温度线(safe_temp)、以及自己用于接受警报的邮箱(recv_email, 推荐和微信绑定的QQ邮箱，这样可以在微信上收到推送)。

4. 逐行输入：

> chmod +x temp_monitor/install.sh
>
> sudo temp_monitor/install.sh

此时如果有跳出要你输入密码的情况，请输入密码（之前第一次开机可能会让你设置，就是当时设置的那个密码，密码在输入时，命令行窗口会没有任何反应，这是正常的。直接输完并按回车就好）

5. 输入：

> sudo reboot

此时系统会重启，重启好后稍等一会儿，查看自己填写的recv_email邮箱是否有邮件到达。如有到达说明成功了。

6. 这里要注意把自己send_email的地址拉进白名单，否则以后发送过来的email会被识别成垃圾邮件丢弃。

7. 在手机端添加邮箱，大部分手机都有自带的邮箱客户端，如果没有，可以用QQ的邮箱客户端，如果你用的是QQ邮箱，可以在微信里设置邮件提醒，是最快捷的提醒。

8. Finish! Enjoy~!


# 说明：

为了防止被一些网站服务器识别为恶意发送导致屏蔽帐号，在email发送功能上做了限制，每隔5分钟才可以发送一份邮件，所以有时候温度上来了可能你没有立刻收到警报，是由于这个原因。

每隔1天无论是否报警都会发送一个包含当前温湿度数据的Daily Info，这个的作用是为了确认这个监控设备运作正常。


# 疑难问题：
不定时更新
