from pydub import AudioSegment
import os


def merge_audio_files(input_directory, output_directory, k):
    audio_files = os.listdir(input_directory)
    audio_files = [file for file in audio_files if file.endswith('.wav')]

    cnt = 1
    for i in range(0, len(audio_files), k):
        merged_audio = AudioSegment.empty()
        merged_content = ""

        audio_segments = []
        for j in range(k):
            if i + j < len(audio_files):
                audio_path = os.path.join(input_directory, audio_files[i + j])
                audio = AudioSegment.from_wav(audio_path)
                audio_segments.append(audio)

                file_path = audio_path[:-3] + 'txt'
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    merged_content += content + " "

        combined = sum(audio_segments)
        merged_audio += combined
        merged_audio.export(output_directory + "/merge" + str(cnt) + ".wav", format='wav')
        with open(output_directory + '/merge' + str(cnt) + '.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(merged_content)
        cnt += 1


os.makedirs('1.Training/002_merge', exist_ok=True)
input_directory = '1.Training/002'  # 합칠 음성 파일들이 있는 디렉토리 경로
output_directory = '1.Training/002_merge'  # 저장할 결과 음성 파일 경로
k = 10  # k개씩 합칠 개수

merge_audio_files(input_directory, output_directory, k)

print("음성 파일이 성공적으로 합쳐져서 저장되었습니다.")
