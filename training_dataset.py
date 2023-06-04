import whisper
import csv
import os
import time
import wave

# model setting
model_base = whisper.load_model("base")
model_small = whisper.load_model("small")
model_medium = whisper.load_model("medium")
model_large = whisper.load_model("large")
models = [model_base, model_small, model_medium, model_large]

count = 1
if os.path.exists('recent_number_t.txt'):
    with open('recent_number_t.txt', 'r') as file:
        count = int(file.read()) + 1

if not os.path.exists('data_t.csv'):
    title = ['id', 'file_length', 'original', 'base_time', 'base', 'small_time', 'small', 'medium_time', 'medium', 'large_time', 'large']
    with open('data_t.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(title)


def get_audio_length(file_path):
    with wave.open(file_path, 'rb') as audio_file:
        frames = audio_file.getnframes()
        frame_rate = audio_file.getframerate()
        audio_length = frames / frame_rate
        return audio_length


for i in range(count, 1000):
    print("current:", i)
    data = [i]
    i_str = str(i)
    if i < 100:
        i_str = "0" + i_str
    if i < 10:
        i_str = "0" + i_str

    audio_length = get_audio_length("1.Training/002/broadcast_00001" + i_str + ".wav")
    data.append(audio_length)

    with open("1.Training/002/broadcast_00001" + i_str + ".txt", 'r', encoding='utf-8') as file:
        text = file.read()
        data.append(text)

    for model in models:
        start_time = time.time()

        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio("1.Training/002/broadcast_00001" + i_str + ".wav")
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # decode the audio
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)

        # print the recognized text
        end_time = time.time()
        elapsed_time = end_time - start_time
        data.append(elapsed_time)
        data.append(result.text)

    with open('data_t.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        try:
            writer.writerow(data)
        except:
            pass
    with open('recent_number_t.txt', 'w') as file:
        file.write(str(i))
