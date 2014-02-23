#!/usr/bin/python
# coding=utf-8
__author__ = 'welen'
import os
import shutil
import string
import re
import sys
import cn_module

#为兼容2和3版本print函数的差异,使用这个
def _print(*objects, **kwargs):
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')
    out = kwargs.get('file', sys.stdout)
    out.write(sep.join(objects) + end)

#读取渠道号
def readChannelfile(filename):
    flag = False
    f = open(filename)
    channelCodeList=[]
    channelNameList=[]
    while True:
        line = f.readline().strip('\n')
        if len(line) == 0:
            break
        elif flag and line.endswith('*/'):
            flag = False
        elif flag: 
            continue
        elif line.startswith('/*'):
            flag = True
        elif line.startswith('#'):
            continue
        else:
            mmap = line.split(':')
            channelCodeList.append(mmap[0])
            channelNameList.append(mmap[1])
    f.close()
    return channelCodeList,channelNameList

#备份manifest文件
def backUpManifest():
    if os.path.exists('./AndroidManifest.xml'):
        os.remove('./AndroidManifest.xml')
    manifestPath = './temp/AndroidManifest.xml'
    shutil.copyfile(manifestPath, './AndroidManifest.xml')

#修改渠道号
def modifyChannel(easyName,name,value):
    f = open('./AndroidManifest.xml')
    tempXML = ''.join(f.readlines());
    f.close()
    regex = r'(?<=android:versionCode\=\")\d+(?=\")'
    result = re.findall(regex, tempXML)
    verCode = result[0]
    
    regex = r'\<meta\-data\s+android:name\=\"CHANNEL\"\s+android:value\=\"([\w-]+)\"\s+/>'
    newValue = r'<meta-data android:name="CHANNEL" android:value="'+value+'\"/>'
    _print('原渠道号:',re.findall(regex,tempXML)[0])
    _print('目标渠道号:', value)
    tempXML = re.sub(regex, newValue, tempXML, 1)

    output = open('./temp/AndroidManifest.xml', 'w')
    output.write(tempXML)
    output.close()
    
    unsignApk = r'./bin/%s_%s_unsigned.apk'% (easyName, name)
    cmdPack = r'java -jar script/apktool.jar b temp %s'% (unsignApk)
    os.system(cmdPack)
    
    global keystore
    global storepass
    global alianame 
    signedjar = r'./bin/%s_%s_%s_signed.apk'% (easyName, name,verCode)
    unsignedjar = r'./bin/%s_%s_unsigned.apk'% (easyName, name)
    cmd_sign = r'jarsigner -verbose -keystore %s -storepass %s -signedjar %s %s %s'% (keystore, storepass, signedjar, unsignedjar, alianame)
    os.system(cmd_sign)
    os.remove(unsignedjar);

#读取用户配置文件
def readUserProperties(properfiles):
    if not os.path.exists(properfiles):
        return False
    fd = open(properfiles)
    global keystore
    global storepass
    global alianame 
    try:
        for line in fd:
            line = line.strip()
            if line.startswith('keystore'):
                keystore='./keystore/'+line.split('=')[1]
            elif line.startswith('storepass'):
                storepass=line.split('=')[1]
            elif line.startswith('alianame'):
                alianame=line.split('=')[1]
    except:
        _print( '--->>>\n请检查script文件夹下的config.ini文件配置,具体配置请查看readme ,检查修改后重新再试 \n <<<<--------')
    finally:
        fd.close()
    if not keystore.strip() or not storepass.strip() or not alianame.strip():
        return False
    _print ('keystore= %s   \nstorepass= %s    \nalianame= %s  \n' % (keystore,storepass,alianame))
    return True	

#执行签名
def startSigntrue():
    path = os.getcwd()
    fileList = os.listdir(path)
    for apkName in fileList:
        if apkName.endswith('.apk'):
            easyName = apkName.split('.apk')[0]
            channelCodeList,channelNameList = readChannelfile(channelFile)
            _print('>>>>>>>>>>>>>>> 开始对 %s 进行打包<<<<<<<<<<<<<<<' % (apkName))
            for i,channel in enumerate(channelCodeList):
                _print( '%s \n 渠道名: %s \n 渠道号: %s\n' % (apkName,channelNameList[i],channel))
            cmdExtract = r'java -jar script/apktool.jar d -s -f %s temp'% (apkName)
            #cmdExtract = r'java -jar apktool.jar d -f %s temp'% (apkName)
            os.system(cmdExtract)

            backUpManifest()
            for i,channel in enumerate(channelCodeList):
                modifyChannel(easyName,channelNameList[i],channel)

keystore=''
storepass=''
alianame=''

#用户配置文件路径
properfilespath = './config/config.ini'
#签名包输出路径
output_apk_dir="./bin"
#渠道号配置文件路径
channelFile='./config/channel.txt'
_print('-------------------------------------------------\n欢迎使用批量打包工具,此工具基于apktool项目,\n除了此项目本身的问题,如果有使用上问题和建议,\n欢迎发邮件到:welenwho@163.com\n-------------------------------------------------\n\n')
if os.path.exists(output_apk_dir):
    shutil.rmtree(output_apk_dir)
if readUserProperties(properfilespath):
    startSigntrue()  

if os.path.exists('./temp'):
    shutil.rmtree('./temp')
if os.path.exists('./AndroidManifest.xml'):
    os.remove('./AndroidManifest.xml')
_print( '-------------------- 完成 --------------------')


