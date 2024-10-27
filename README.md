# Listening the message and passing to the Unity.

This Python-template demonstrates how to develop a software module to process video data (eg., image detection, etc.) and to control Kiwi.

Prerequisites:
* [You need to install Docker for your platform](https://docs.docker.com/install/linux/docker-ce/debian/#install-docker-ce)
* [You need to install `docker-compose`](https://docs.docker.com/compose/install/#install-compose)
* You have successfully completed the _Getting started_ tutorials [here](https://github.com/chalmers-revere/opendlv-tutorial-kiwi/tree/master).
* You have a recording file (`.rec`) with some video frames.
* You need to install `libcluon` (example below is for Ubuntu 18.04 LTS):
```Bash
sudo add-apt-repository ppa:chrberger/libcluon
sudo apt-get update
sudo apt-get install libcluon
```
* You need to install Python, make, protobuf, and OpenCV (example below is for Ubuntu 18.04 LTS):
```Bash
sudo apt-get install --no-install-recommends \
    build-essential \
    python3-protobuf \
    python3-sysv-ipc \
    python3-numpy \
    python3-opencv \
    protobuf-compiler
```

---

## Developing and testing the Python application on your laptop

This template folder contains an example how to use Python to process data residing in a shared memory area using OpenCV for image processing.

* Step 1: Assuming that you have a folder `~/kiwi-recordings`, where you have at least one `.rec` file with included video.

* Step 2: Clone this repository (if it was done already in the C++ tutorial, then skip command #2):
```bash
cd $HOME
git clone git@github.com:hunli12312/Message_python.git
cd Message_python
```

* Step 3: The image should be build, just run:
```bash
docker build -t listener -f Dockerfile.base.armhf .
```
This step needs to be repeated whenever you change something in the message specifications.

* Step 4: Run the file by running:

```bash
docker run -it --rm listener
```


The application should start and wait for images to come in. Furthermore, the code also display all other sensor values from the recording file, and the code example show how these messages can be parsed.

You can stop the Python application by pressing `Ctrl-C`. When you are modifying the Python application, repeat step 4 after any change to your software.

## Listening and Sending the data to the unity

This processes contain the info how to conduct and run the function in the OpenLab.

* Step 1: Clone this repository under same the 'docker-compose.yml' (Or you can backup the docker-compose.yml for following processes)
So it should be -docker-compose.yml
                -Messsage_python  
In the Message_python folder, you can check the 'listener.py' to see if the Unity IP is the IP belongs to the laptop running Unity. Otherwise, you should change to the IP into right IP (Ethernet in most case).


* Step 2: Adding the following line to the docker-compose.yml (if you back up it, using the backup version .yml) in the end under same dirctories:
```bash
services:
  # Other services remains same.
  listener:
    container_name: opendlv-listener
    build:
      context: ./Message_python
      dockerfile: Dockerfile.base.armhf
    restart: always
    network_mode: "host"
    command: ["python3", "listener.py"]

```

* Step 3: Run the container:
```bash
docker-compose -f docker-compose.yml up -d
```
(If you don't back up, run the exmaple command. Otherwise, you need to change 'docker-compose.yml' to the your own '***.yml')

* Step 4: Run the Unity:
The unity project can get the signal from docker-compose.

quit: docker-compose -f docker-compose.yml down

---
The listener.py should be modified based on the Unity server IP address.
---


