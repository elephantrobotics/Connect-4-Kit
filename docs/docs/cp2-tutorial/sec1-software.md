---
sidebar_position: 1
---

# 软件环境准备

## Python安装

### Windows

访问[Python3.10官方下载页面](https://www.python.org/downloads/release/python-31011/)，选择MSI版本下载并安装即可

![](attachment/2023-07-06-14-41-35.png)

注意：安装过程中记得勾选自动添加到环境变量

安装完毕后，`Win+R`打开运行，输入`CMD`，在弹出的CMD窗口中输入`python`以检查是否成功

![](attachment/2023-07-06-14-42-56.png)

### Ubuntu

```sudo apt-get install python3.10```

## Git

Git是用来下载和管理代码的工具

Git的下载安装请参考[官方教程](https://git-scm.com/book/zh/v2/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)

## 配置项目环境

按顺序执行以下命令

```bash
git clone https://github.com/elephantrobotics/Connect-4-Kit.git
cd Connect-4-Kit
pip install -r requirements.txt
```

Done.
