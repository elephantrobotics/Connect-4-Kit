---
sidebar_position: 1
---

# Software Environment Preparation

> Pi version's system come with necessary python environment, you only need to download the latest source code。If you are using Pi version, you can start from Setup project.

## Python Installation

Python is the main programming language used in this project and requires version 3.10 or above. Below are instructions on how to install and configure the environment on different platforms.

### Windows

Visit the [Python 3.10 official download page](https://www.python.org/downloads/release/python-31011/) and download the MSI version. Run the installer and follow the prompts to install Python.

![](attachment/2023-07-06-14-41-35.png)

Note: Remember to check the option to automatically add Python to the environment variables during the installation process.

After installation, press Win+R to open the Run dialog, type CMD, and press Enter. In the opened CMD window, type python to check if the installation was successful.

![](attachment/2023-07-06-14-42-56.png)

### Ubuntu

Python needs to be version 3.10 or above. Here is how to install a different version of Python on Ubuntu.

First, add the custom repository. Do not install directly.

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

Then, use apt to install Python 3.10 and related tools.

```bash
sudo apt-get install python3.10
sudo apt-get install python3.10-distutils
```

Verify the installation.

```bash
python3.10 --version
# python 3.10.12
```

## Git

Git is a tool used to download and manage code. In this project, it is used to clone the project repository.

Refer to the [Official Tutorial](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) for downloading and installing Git.

## Setup project

Execute the following commands in order.

```bash
git clone https://github.com/elephantrobotics/Connect-4-Kit.git
cd Connect-4-Kit
```

Based on the platform, install the corresponding requirements list.

If it's the Windows platform, please run:
```powershell
pip install -r .\requirements_windows.txt
```
If it's the Linux platform, please run:
```shell
pip install -r .\requirements_linux.txt
```

## Check robot firmware version

MyCobot 280 robot arm's firmware version of ATOM should above `6.3`.
MyArm robot arm's firmware version of ATOM should above `3.9`
If it's not, please use Mystudio to update the firmware to the latest version.
