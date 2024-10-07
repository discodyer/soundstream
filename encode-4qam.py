import numpy as np
import wave

def encode_data_to_wav(data, output_file):
    # 调制参数
    sample_rate = 44100
    freq_map = {
        '00': 1000,  # 00 对应 1000 Hz
        '01': 5000,  # 01 对应 5000 Hz
        '10': 10000, # 10 对应 10000 Hz
        '11': 15000  # 11 对应 15000 Hz
    }
    T = 0.05  # 每个符号的持续时间
    symbol_duration = int(sample_rate * T)
    
    wave_data = []

    # 遍历原始数据的每个字节
    for byte in data:
        bits = format(byte, '08b')  # 将字节转换为8位二进制
        print(f"编码字节 {byte}: {bits}")  # 打印每个字节的二进制表示
        for i in range(0, len(bits), 2):
            symbol_bits = bits[i:i + 2]
            frequency = freq_map[symbol_bits]
            t = np.linspace(0, T, symbol_duration, endpoint=False)
            wave_data.append(np.sin(2 * np.pi * frequency * t))
            print(f"编码符号: {symbol_bits}, 频率: {frequency} Hz")  # 打印每个符号和对应频率
    
    # 合并数据
    wave_data = np.concatenate(wave_data)
    wave_data = (wave_data * 32767).astype(np.int16)  # 转换为16位PCM格式
    
    # 保存为WAV文件
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(wave_data.tobytes())

# 示例使用
with open('example.txt', 'rb') as f:  # 二进制方式读取文件
    data = f.read()

output_file = "encoded.wav"
encode_data_to_wav(data, output_file)
