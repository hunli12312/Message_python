# Processing image data with OpenCV and controlling Kiwi using Python

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

## Developing and testing the Python application on your laptop using replay mode

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
docker-compose -f docker build -t listener -f Dockerfile.base.armhf .
```
This step needs to be repeated whenever you change something in the message specifications.

* Step 4: Run the file by running:

```bash
docker run -it --rm listener
```


The application should start and wait for images to come in. Furthermore, the code also display all other sensor values from the recording file, and the code example show how these messages can be parsed.

You can stop the Python application by pressing `Ctrl-C`. When you are modifying the Python application, repeat step 4 after any change to your software.

---

## Deploying and testing the Python application in Kiwi simulation

* Step 1: Have the previous tutorial completed.

* Step 2: Start the simulation as described in section 3.1.

* Step 3: Inside `opendlv-perception-helloworld.py` change the name of the shared memory from `/tmp/img.argb` to `/tmp/video0.argb`

* Step 4: Open another terminal. Then run the Python (note that you need version 3) module from the folder `opendlv-perception-helloworld-python`:
```bash
python3 opendlv-perception-helloworld.py
```

The application should start and wait for images to come in. Furthermore, the code also display all other sensor values from the recording file, and the code example show how these messages can be parsed. You can also send actuation signals, as exemplified in the code, to steer the simulated robot.

You can stop your software component by pressing `Ctrl-C`. When you are modifying the software component, repeat step 4 after any change to your software.

---
The listener.py should be modified based on the Unity server IP address.
---
