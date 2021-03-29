
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \

# Install necessary system packages
sudo apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev

# Install gstreamer for audio, video (optional)
sudo apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good

sudo add-apt-repository ppa:kivy-team/kivy
sudo apt-get update
sudo apt-get install python3-kivy



apt update
$ apt install python3 python3-venv python3-pip python3-dev build-essential libgl1-mesa-dev
works
python3 -m PyInstaller --onefile --name SOCIAL_NETWORK_TEST --distpath packages/projectTest --workpath .cache/ app.py
export PATH="/home/nidza/.local/bin/pyinstaller:$PATH"

python3 -m venv my_kivy_project
$ cd my_kivy_project
$ source bin/activate
(my_kivy_project) $ pip install kivy

