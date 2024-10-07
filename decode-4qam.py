import numpy as np
import wave

def decode_wav_to_data(input_file):
    # 读取WAV文件
    with wave.open(input_file, 'rb') as wf:
        sample_rate = wf.getframerate()
        n_samples = wf.getnframes()
        wave_data = wf.readframes(n_samples)
        
    wave_data = np.frombuffer(wave_data, dtype=np.int16).astype(np.float32) / 32767.0

    # 4-QAM参数
    T = 0.05  # 符号持续时间
    symbol_duration = int(sample_rate * T)
    num_symbols = len(wave_data) // symbol_duration
    decoded_bits = []

    # 定义频率到符号的映射
    freq_map = {
        1000: '00',
        5000: '01',
        10000: '10',
        15000: '11'
    }
    tolerance = 200  # 频率容差
    
    hanning_window = np.hanning(symbol_duration)

    # 解调
    for i in range(num_symbols):
        segment = wave_data[i * symbol_duration:(i + 1) * symbol_duration] * hanning_window
        spectrum = np.fft.fft(segment)
        frequencies = np.fft.fftfreq(len(segment), 1/sample_rate)
        
        # 查找频率峰值
        peak_index = np.argmax(np.abs(spectrum[:len(spectrum)//2]))  # 只看正频率部分
        detected_freq = abs(frequencies[peak_index])
        
        # 打印检测到的频率
        print(f"符号 {i} 的检测频率: {detected_freq} Hz")
        
        # 判断检测到的频率是否接近我们定义的符号频率
        for freq, bits in freq_map.items():
            if abs(detected_freq - freq) < tolerance:
                decoded_bits.append(bits)
                print(f"解码符号: {bits}, 频率: {freq} Hz")  # 打印解码符号
                break
        else:
            print(f"无法识别的频率: {detected_freq} Hz")
    
    # 将比特串转换为字节
    total_bits = ''.join(decoded_bits)
    byte_array = bytearray()
    for i in range(0, len(total_bits), 8):
        byte_array.append(int(total_bits[i:i + 8], 2))
    
    # 返回解码后的原始数据
    return byte_array

# 示例使用
input_file = "encoded.wav"
decoded_data = decode_wav_to_data(input_file)
if decoded_data:
    with open('decoded_output.txt', 'wb') as f:
        f.write(decoded_data)
else:
    print("没有解码到任何数据")
