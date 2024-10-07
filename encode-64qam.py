import numpy as np
import wave

def encode_data_to_wav(data, output_file):
    # 调制参数
    sample_rate = 44100
    freq_map = {format(i, '06b'): 1000 + i * 100 for i in range(64)}  # 创建64个频率
    T = 0.01  # 每个符号的持续时间
    symbol_duration = int(sample_rate * T)
    
    wave_data = []
    bit_buffer = ''

    # 遍历原始数据的每个字节
    for byte in data:
        bits = format(byte, '08b')  # 将字节转换为8位二进制
        bit_buffer += bits  # 添加到缓冲区
        print(f"编码字节 {byte}: {bits}")  # 打印每个字节的二进制表示

        # 从缓冲区中取出每6位，编码为符号
        while len(bit_buffer) >= 6:
            symbol_bits = bit_buffer[:6]
            bit_buffer = bit_buffer[6:]  # 移除已编码的6位
            frequency = freq_map[symbol_bits]
            t = np.linspace(0, T, symbol_duration, endpoint=False)
            wave_data.append(np.sin(2 * np.pi * frequency * t))
            print(f"编码符号: {symbol_bits}, 频率: {frequency} Hz")  # 打印每个符号和对应频率
    
    # 如果还有剩余的位（少于6位），需要补0凑齐6位
    if bit_buffer:
        symbol_bits = bit_buffer.ljust(6, '0')  # 不足6位的右边补0
        frequency = freq_map[symbol_bits]
        t = np.linspace(0, T, symbol_duration, endpoint=False)
        wave_data.append(np.sin(2 * np.pi * frequency * t))
        print(f"编码符号: {symbol_bits}, 频率: {frequency} Hz (补全)")  # 打印补全的符号

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

output_file = "encoded_64qam.wav"
encode_data_to_wav(data, output_file)
