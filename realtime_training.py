import whisper
import pyaudio
import threading
import time
import wave

# model setting
model = whisper.load_model("base")

RECORD_SECONDS = 30
OUTPUT_FILENAME = "recording.wav"


def record_audio():
    print("녹음 시작")
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("녹음 완료")

    # 새로운 스레드에서 프로시저 실행
    threading.Timer(0, train).start()


def train():
    start_time = time.time()

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(OUTPUT_FILENAME)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("걸린 시간:", elapsed_time)
    print("내용:", result.text)


def main():
    while True:
        record_audio()


if __name__ == "__main__":
    main()
