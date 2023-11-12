import wave
import sys
import json
import srt
import datetime
from vosk import Model, KaldiRecognizer, SetLogLevel
import argostranslate.package
import argostranslate.translate
import csv
import moviepy.editor as mp
from pydub import AudioSegment
from subtoaudio import SubToAudio



def transcribe():
    results = []
    subs = []
    while True:
       data = wf.readframes(4000)
       if len(data) == 0:
           break
       if rec.AcceptWaveform(data):
           results.append(rec.Result())
    results.append(rec.FinalResult())

    for i, res in enumerate(results):
       jres = json.loads(res)
       if not 'result' in jres:
           continue
       words = jres['result']
       for j in range(0, len(words), WORDS_PER_LINE):
           line = words[j:j + WORDS_PER_LINE]

           if target_language == "en":
            s = srt.Subtitle(index=len(subs),
                    content=argostranslate.translate.translate(" ".join([l['word'] for l in line]), "ru", "en"),
                    start=datetime.timedelta(seconds=line[0]['start']),
                    end=datetime.timedelta(seconds=line[-1]['end']))
           else:
            eng_trans = argostranslate.translate.translate(" ".join([l['word'] for l in line]), "ru", "en")
            s = srt.Subtitle(index=len(subs),
                    content = argostranslate.translate.translate("".join(eng_trans), "en", target_language),
                    start=datetime.timedelta(seconds=line[0]['start']),
                    end=datetime.timedelta(seconds=line[-1]['end']))              

           subs.append(s)
    return subs





langugs = ['Немецкий', 'Английский', 'Французский', 'Итальянский', 'Испанский', 
           'Японский', 'Китайский', 'Португальский', 'Чешский', 'Датский', 
           'Польский', 'Турецкий'] 
lang_code = ['de','en','fr','it','es','ja','zh','pt','en', 'en', 'pl', 'tr']
filename = "data_csv/dataset.csv"

with open(filename, 'r', encoding="utf-8") as file:
    csv_data = csv.reader(file)
    next(csv_data)  
    for row in csv_data:
        target_language = row[0]


        video_name = row[1]
        target_language = lang_code[langugs.index(target_language)]

        video = mp.VideoFileClip(f"videos/{video_name}")
        audio = video.audio
        audio.write_audiofile(f"audios/{video_name}.wav")


        sound = AudioSegment.from_wav(f"audios/{video_name}.wav")
        sound = sound.set_channels(1)
        sound.export(f"audios/{video_name}.wav", format="wav")



        from_code = "ru"
        to_code = "en"
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())
        if target_language != "en":
            from_code = "en"
            to_code = target_language
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
                )
            )
            argostranslate.package.install_from_path(package_to_install.download())





        SetLogLevel(0)


        wf = wave.open(f"audios/{video_name}.wav", "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            sys.exit(1)

        model = Model("model")
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        rec.SetPartialWords(True)

        s = ""
        WORDS_PER_LINE = 7


        text = srt.compose(transcribe())
        with open(f"subtitles/{video_name}.srt", "w", encoding="utf-8") as file:
            file.write(text)

        model = SubToAudio().coqui_model()[1]

        sub = SubToAudio(fairseq_language="eng")
        subtitle = sub.subtitle(f"subtitles/{video_name}.srt")
        sub.convert_to_audio(sub_data=subtitle, voice_conversion=True, speaker_wav=f"audios/{video_name}.wav", output_path=f"transaudios/{video_name}.wav")


        sound1 = AudioSegment.from_wav(f"audios/{video_name}.wav")
        sound2 = AudioSegment.from_wav(f"transaudios/{video_name}.wav")


        output = sound2.overlay(sound1 - 20)

        # save the result
        output.export(f"mixed_audios/{video_name}.wav", format="wav")

        videoclip = mp.VideoFileClip(f"videos/{video_name}")
        audioclip = mp.AudioFileClip(f"mixed_audios/{video_name}.wav")

        new_audioclip = mp.CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile(f"out_videos/{video_name}.mp4")

