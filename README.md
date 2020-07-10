# Caps Writer

### 简介

一款语音输入工具，后台运行脚本后，按下大写锁定键超过 0.3 秒后，开始语音识别，松开按键之后，自动输入识别结果。

### 描述

本工具（Caps Writer）是一个电脑端的语音输入工具，使用了阿里云的一句话识别 api

（有兴趣的可以改成百度、腾讯、讯飞的 api 试试）。

使用方法很简单：用 python 运行 `run.py` 后，按下 `Caps Lock`（也就是大写锁定键）超过 0.3 秒后，就会开始用阿里云的 api 进行语音识别，松开按键后，会将识别结果自动输入。

对于聊天时候进行快捷输入、写代码时快速加入中文注释非常的方便。

### 视频演示

请到 HacPai 帖子中进行查看：

### 安装使用

本工具是一个python脚本，依赖于以下模块：

- keyboard
- pyaudio
- configparser
- aliyunsdkcore
- alibabacloud-nls-python-sdk

其中：

- pyaudio 在 windows 上不是太好安装，可以先到 [这个链接](https://www.lfd.uci.edu/~gohlke/pythonlibs) 下载 pyaudio 对应版本的 whl 文件，再用 pip 安装
- alibabacloud-nls-python-sdk 不是通过 python 安装，而是通过 [阿里云官方文档的方法](https://help.aliyun.com/document_detail/120693.html) 进行安装。

另外，需要在 `run.py` 中填入阿里云拥有 **管理智能语音交互（NLS）** 权限的 **RAM访问控制** 用户的 **accessID**、**accessKey** 和智能语音交互语音识别项目的 **appkey** 。

做完以上步骤后，只要运行 `run.py` 就可以用了！

本文件夹内有一个 `安装指南` 文件夹，在里面可以找到详细的安装指南，还包括了提前下载的 alibabacloud-nls-python-sdk 和 pyaudio 的 whl 文件。

### 后话

因为作者就是本着凑合能用就可以了的心态做这个工具的，所以图形界面什么的也没做，整个工具单纯就一个脚本，功能也就一个，按住大写锁定键开始语音识别，松开后输入结果。目前作者本人已经很满意。

欢迎有想法有能力的人将这个工具加以改进，比如加入讯飞、腾讯、百度的语音识别api，长按0.3秒后开始识别时加一个提示等等等等。