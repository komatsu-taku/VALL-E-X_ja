# import argparse
# import os
# import soundfile as sf


# def parse_args():
#     parser = argparse.ArgumentParser()

#     parser.add_argument('--input', '-i', type=str, required=True, help="Path to the input directory (basic5000/)")
#     parser.add_argument('--output', '-o', type=str, required=True, help="Path to the output directory")
#     parser.add_argument('--transcript', '-t', type=str, required=True, help="Path to the transcript file (transcript_utf8.txt)")

#     return parser.parse_args()


# def main(args: argparse.Namespace):
#     # 入力ディレクトリと出力ディレクトリの設定
#     input_dir = args.input
#     output_dir = args.output
#     transcript_path = args.transcript

#     # 出力ディレクトリを作成
#     os.makedirs(output_dir, exist_ok=True)

#     # 音声ファイルリストを取得
#     wav_files = sorted([f for f in os.listdir(os.path.join(input_dir, "wav")) if f.endswith(".wav")])

#     # トランスクリプトの読み込み
#     with open(transcript_path, 'r', encoding='utf-8') as transcript_file:
#         transcript_lines = transcript_file.readlines()

#     # トランスクリプトを辞書形式に変換 (キー: ファイル名, 値: トランスクリプト)
#     transcript_dict = {}
#     for line in transcript_lines:
#         if ":" in line:
#             key, text = line.strip().split(":", 1)
#             transcript_dict[key] = text

#     # アノテーションファイル (audio_ann_sum.txt) の準備
#     ann_output_path = os.path.join(output_dir, "audio_ann_sum.txt")
#     with open(ann_output_path, 'w', encoding='utf-8') as ann_file:
#         # 音声ファイルを出力ディレクトリ直下に配置
#         for wav_file in wav_files:
#             # 音声ファイルを移動
#             src_wav_path = os.path.join(input_dir, "wav", wav_file)
#             dst_wav_path = os.path.join(output_dir, wav_file)
#             os.rename(src_wav_path, dst_wav_path)

#             # 対応するトランスクリプトを取得
#             wav_stem = os.path.splitext(wav_file)[0]  # BASIC5000_0001 形式
#             if wav_stem in transcript_dict:
#                 transcript_text = transcript_dict[wav_stem]
#                 # 音声データの長さを取得してアノテーションに追加
#                 try:
#                     audio, sample_rate = sf.read(dst_wav_path)
#                     duration = len(audio) / sample_rate
#                     ann_file.write(f"{wav_stem}|{duration:.2f}|ja|{transcript_text}\n")
#                 except Exception as e:
#                     print(f"Error processing {wav_file}: {e}")
#             else:
#                 print(f"Warning: No transcript found for {wav_file}")

#     print("Files and transcripts have been organized successfully.")
#     print(f"Annotation file saved to {ann_output_path}")


# if __name__ == "__main__":
#     main(parse_args())


import argparse
import os
import soundfile as sf


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', type=str, required=True, help="Path to the input directory (basic5000/)")
    parser.add_argument('--output', '-o', type=str, required=True, help="Path to the output directory")
    parser.add_argument('--transcript', '-t', type=str, required=True, help="Path to the transcript file (transcript_utf8.txt)")

    return parser.parse_args()


def main(args: argparse.Namespace):
    # 入力ディレクトリと出力ディレクトリの設定
    input_dir = args.input
    output_dir = args.output
    transcript_path = args.transcript

    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    # 音声ファイルリストを取得
    wav_files = sorted([f for f in os.listdir(os.path.join(input_dir, "wav")) if f.endswith(".wav")])

    # トランスクリプトの読み込み
    with open(transcript_path, 'r', encoding='utf-8') as transcript_file:
        transcript_lines = transcript_file.readlines()

    # トランスクリプトを辞書形式に変換 (キー: ファイル名, 値: トランスクリプト)
    transcript_dict = {}
    for line in transcript_lines:
        if ":" in line:
            key, text = line.strip().split(":", 1)
            transcript_dict[key] = text

    # アノテーションファイル (audio_ann_sum.txt) の準備
    ann_output_path = os.path.join(output_dir, "audio_ann_sum.txt")
    with open(ann_output_path, 'w', encoding='utf-8') as ann_file:
        # 音声ファイルを出力ディレクトリ直下に配置
        for wav_file in wav_files:
            # 音声ファイルを移動
            src_wav_path = os.path.join(input_dir, "wav", wav_file)
            dst_wav_path = os.path.join(output_dir, wav_file)
            os.rename(src_wav_path, dst_wav_path)

            # 対応するトランスクリプトを取得
            wav_stem = os.path.splitext(wav_file)[0]  # BASIC5000_0001 形式
            if wav_stem in transcript_dict:
                transcript_text = transcript_dict[wav_stem]
                # 音声データの長さを取得してアノテーションに追加
                try:
                    audio, sample_rate = sf.read(dst_wav_path)
                    duration = len(audio) / sample_rate
                    ann_file.write(f"{wav_stem}|{duration:.2f}|ja|{transcript_text}\n")
                except Exception as e:
                    print(f"Error processing {wav_file}: {e}")
            else:
                print(f"Warning: No transcript found for {wav_file}")

    print("Files and transcripts have been organized successfully.")
    print(f"Annotation file saved to {ann_output_path}")


if __name__ == "__main__":
    main(parse_args())
