import soundfile as sf
import numpy as np

import os
import shutil


def split_channels_and_segments(input_file, segment_length=5, time_shift=2.5):
    # 读取多通道音频文件
    data, samplerate = sf.read(input_file)
    channels = data.shape[1]
    
    # 计算每个片段的样本数
    segment_samples = int(segment_length * samplerate)
    shift_samples = int(time_shift * samplerate)
    
    # 遍历每一对相邻通道
    for i in range(channels - 1):
        if i+2 == 8:
            break
        # 提取双通道数据
        stereo_data = data[:, i:i+2]
        
        # 计算并保存每个片段
        start_sample = 0
        segment_index = 0
        while start_sample + segment_samples <= stereo_data.shape[0]:
            # 提取片段
            segment_data = stereo_data[start_sample:start_sample+segment_samples, :]
            
            # 保存片段音频文件
            output_file = f'/home/zhaozhou/srp-dnn-1/data/meeting_room_data/stereo_data_1/stereo_{i}_{i+2}_{segment_index}.wav'
            sf.write(output_file, segment_data, samplerate)
            print(f'Saved {output_file}')
            
            # 更新下一个片段的起始位置和索引
            start_sample += shift_samples
            segment_index += 1

def copy_and_rename_npz(directory, npz_file='/home/zhaozhou/srp-dnn-1/data/SenSig-test/0.npz'):
    """
    遍历指定目录中的所有 .wav 文件，将 0.npz 文件复制并重命名为与 .wav 文件同名（扩展名为 .npz）
    
    :param directory: 要遍历的目录路径
    :param npz_file: 要复制和重命名的 npz 文件的名称
    """
    # 确保 npz 文件存在
    npz_path = os.path.join(directory, npz_file)
    if not os.path.exists(npz_path):
        print(f"文件 {npz_file} 不存在于目录 {directory} 中。")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            # 构建新的 npz 文件名（与 wav 文件同名）
            new_npz_filename = os.path.splitext(filename)[0] + '.npz'
            new_npz_path = os.path.join(directory, new_npz_filename)
            
            # 复制并重命名 npz 文件
            shutil.copy(npz_path, new_npz_path)
            print(f"已将 {npz_file} 复制并重命名为 {new_npz_filename}")



multi_channel_long_wav_file = "/home/zhaozhou/srp-dnn-1/data/meeting_room_data/session3.wav"
split_channels_and_segments(multi_channel_long_wav_file)

directory = "/home/zhaozhou/srp-dnn-1/data/meeting_room_data/stereo_data_1"  # 修改为你的目录路径
copy_and_rename_npz(directory)

