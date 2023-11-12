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
2. Добавьте видео для перевода в директорию *videos*
3. Запустите main.py командой: python3 main.py

# Как работает
Программа обрабатывает видео из папки *videos* переводя речь на видео на указанный язык в *data_csv/dataset.csv*
1. Достает из видео аудиодорожку и переводит её в моно.
2. Определяет речь на видео и записывает, её в папку *subtitles/* в формате субтитров *.srt*
3. Переводит *.srt* на указанный язык
4. Озвучивает аудиодорожку используя речь говорящего на видео и сохраняет аудио в папке *trans_audios/*
5. Накладывает переведенную речь на оригинальную аудидорожку сохраняет её в папке *mixed_audios/*
6. Заменяет аудидорожку у видео
7. Итоговый вариант видео появится в папке *out_videos/*

## Программа завершит свою работу после того как обработает все указанные видео в *data_csv/dataset.csv*
