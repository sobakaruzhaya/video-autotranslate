# Video Autottanslate
Озвучка видео на другие языки

# Установка
## Linux
```
git clone https://github.com/sobakaruzhaya/video-autotranslate
cd video-autotranslate
sudo apt-get install python3-venv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
## Windows
```
git clone https://github.com/sobakaruzhaya/video-autotranslate
cd video-autotranslate
python -m venv env
./env/Scripts/Activate 
pip install -r requirements.txt
```

# Как пользоваться
1. Скачайте общедоступную [модель vosk](https://alphacephei.com/vosk/models/vosk-model-ru-0.10.zip) и перенесите папку model в директорию проекта
2. Запустите main.py командой: python3 main.py

# Как работает
