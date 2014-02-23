
使用前请确定已经安装了python和jdk1.6版本(1.7签名可能出现签不上的情况)
由于python 2和3的差异化,提供了两套方案,根据当前安装版本选择允许哪个目标文件

在本目录下放置需要批量打包的未签名apk包即可,支持多个apk同时打
具体配置看script/pythonX.py文件的配置
目录结构
	keystore 签名文件路径
	platform/X 平台相关的依赖
	script 脚本文件和渠道号配置文件
		pythonX.py 脚本文件
		apktool.jar文件，解包和打包用的
	config 目录用户配置目录
		channel.txt 批量渠道号配置文件
		config.ini 签名包的配置设置
	xx.apk 需要批量打包的未签名apk
	bin 目录 运行成功后生成的签名文件存放目录
		命名规则
		项目名+渠道名+版本号+签名状态+apk


需要注意的是项目的AndroidManifest.xml文件中必须包含<meta-data android:name="CHANNEL" android:value="xxxx" />
其中xxxx为默认渠道号，需要添加的渠道号放在channel.txt中，注意书写规范

最终输出文件为存放bin目录下

channel规则
支持单行和多行注释
#号为单行注释
/* 为多行注释 */

config.ini  支持中文注释
签名包的配置设置
#这个是签名文件,放在keystore目录下
keystore=xxxx
#这个是签名文件密码,目前不支持不同签名的,后续版本添加
storepass=xxxx
#这个是签名文件别名
alianame=xxxx


window下运行 win_start.bat即可
mac 下和linux 下执行linux_Start或mac_start相关文件
例如:bash linux_start

首次允许需要输入当前登录的账号密码


更新说明:
1.21 更改目录结构,更和谐,相关细节调整

历史更新

*1.20正式版, 添加中文支持,添加版本判断,较少使用时候的版本判断文件,只需要执行相关平台xx_start文件即可
1.12正式版 ，添加config.ini文件,让签名配置更简单,优化代码逻辑

*1.11正式版，添加多平台支持,添加python2和3版本支持,提供aapt依赖,无需配置环境变量

ps:由于基于apktool项目的,如果apktool项目本身存在的问题,哥木有办法~~~~~ by welen