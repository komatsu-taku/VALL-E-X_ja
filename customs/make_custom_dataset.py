import h5py
import glob
import torch
import numpy as np
import os
import torchaudio
import soundfile as sf
from tqdm.auto import tqdm
from utils.g2p.symbols import symbols
from utils.g2p import PhonemeBpeTokenizer
from utils.prompt_making import make_prompt, make_transcript
from data.collation import get_text_token_collater
from data.dataset import create_dataloader

# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}
from data.tokenizer import (
    AudioTokenizer,
    tokenize_audio,
)

tokenizer_path = "./utils/g2p/bpe_69.json"
tokenizer = PhonemeBpeTokenizer(tokenizer_path)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def make_prompts(data_dir, name, audio_prompt_path, transcript=None):
    # 读取已经存在的stems
    audio_ann_sum_backup = r"MyTTSDataset\wavs\audio_ann_sum_backup.txt"
    existing_stems = set()
    backup_data = {}
    if os.path.exists(audio_ann_sum_backup):
        with open(audio_ann_sum_backup, 'r', encoding='utf-8') as f:
            for line in f:
                stem = line.split('|')[0]
                text_pr = line.split('|')[3]
                existing_stems.add(stem)
                backup_data[stem] = {
                    'text_pr':text_pr,
                }

    text_tokenizer = PhonemeBpeTokenizer(tokenizer_path="./utils/g2p/bpe_69.json")
    text_collater = get_text_token_collater()
    codec = AudioTokenizer(device)
    wav_pr, sr = torchaudio.load(audio_prompt_path)
    # check length
    if wav_pr.size(-1) / sr > 15:
        raise ValueError(f"Prompt too long, expect length below 15 seconds, got {wav_pr / sr} seconds.")
    if wav_pr.size(0) == 2:
        wav_pr = wav_pr.mean(0, keepdim=True)

    if name in existing_stems:
        # print(f"{name} already exists in {audio_ann_sum_backup}, copying data to {name}.")
        # Read from backup and write to ann_output_path
        text_pr = backup_data[name]['text_pr']

    else:
        text_pr, lang_pr = make_transcript(name, wav_pr, sr, transcript)

    # tokenize audio
    encoded_frames = tokenize_audio(codec, (wav_pr, sr))
    audio_tokens = encoded_frames[0][0].transpose(2, 1).cpu().numpy()

    # tokenize text
    phonemes, langs = text_tokenizer.tokenize(text=f"{text_pr}".strip())
    text_tokens, enroll_x_lens = text_collater(
        [
            phonemes
        ]
    )

    return audio_tokens, text_tokens, langs, text_pr
    
def create_dataset(data_dir, dataloader_process_only):
    if dataloader_process_only:
        h5_output_path=f"{data_dir}/audio_sum.hdf5"
        ann_output_path=f"{data_dir}/audio_ann_sum.txt"
        #audio_folder = os.path.join(data_dir, 'audio')
        audio_paths = glob.glob(f"{data_dir}/*.wav")  # Change this to match your audio file extension

        # Create or open an HDF5 file
        with h5py.File(h5_output_path, 'w') as h5_file:
            # Loop through each audio and text file, assuming they have the same stem
            for audio_path in tqdm(audio_paths):
                try:
                    stem = os.path.splitext(os.path.basename(audio_path))[0]
                    audio_tokens, text_tokens, langs, text = make_prompts(data_dir=data_dir, name=stem, audio_prompt_path=audio_path)
                    
                    text_tokens = text_tokens.squeeze(0)
                    # Create a group for each stem
                    grp = h5_file.create_group(stem)
                    # Add audio and text tokens as datasets to the group
                    grp.create_dataset('audio', data=audio_tokens)
                    #grp.create_dataset('text', data=text_tokens)
                    
                    with open(ann_output_path, 'a', encoding='utf-8') as ann_file:
                        audio, sample_rate = sf.read(audio_path)
                        duration = len(audio) / sample_rate
                        ann_file.write(f'{stem}|{duration}|{langs[0]}|{text}\n')  # 改行を追加
                except Exception as e:
                    print(f"An error occurred: {e}")
    else:
        dataloader = create_dataloader(data_dir=data_dir)
        return dataloader