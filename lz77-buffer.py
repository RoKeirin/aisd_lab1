def lz77_encode(data, window_size, lookahead_buffer_size):
    compressed = bytearray()
    pos = 0
    while pos < len(data):
        window_start = max(0, pos - window_size)
        lookahead_end = min(pos + lookahead_buffer_size, len(data))
        best_match = (0, 0)
        for i in range(window_start, pos):
            match_length = 0
            while (pos + match_length < lookahead_end and
                   i + match_length < pos and
                   data[i + match_length] == data[pos + match_length]):
                match_length += 1
            if match_length > best_match[1]:
                best_match = (pos - i, match_length)
        if best_match[1] >= 3:
            offset, length = best_match
            next_char = data[pos + length] if pos + length < len(data) else 0
            compressed.extend(offset.to_bytes(2, 'big'))
            compressed.extend(length.to_bytes(2, 'big'))
            compressed.append(next_char)
            pos += length + 1
        else:
            compressed.extend((0).to_bytes(2, 'big'))  # Смещение = 0
            compressed.extend((0).to_bytes(2, 'big'))  # Длина = 0
            compressed.append(data[pos])
            pos += 1
    return bytes(compressed)
def lz77_decode(compressed):
    decompressed = bytearray()
    pos = 0
    while pos < len(compressed):
        offset = int.from_bytes(compressed[pos:pos + 2], 'big')
        length = int.from_bytes(compressed[pos + 2:pos + 4], 'big')
        next_char = compressed[pos + 4]
        pos += 5
        if offset == 0 and length == 0:
            decompressed.append(next_char)
        else:
            start = len(decompressed) - offset
            for i in range(length):
                decompressed.append(decompressed[start + i])
            decompressed.append(next_char)
    return bytes(decompressed)

def to_bytes(data, encoding: str = 'utf-8') -> bytes:
    if isinstance(data, bytes):
        return data  # Если данные уже в байтах, возвращаем их как есть
    elif isinstance(data, str):
        return data.encode(encoding)  # Преобразуем строку в байты
    elif isinstance(data, (int, float)):
        return str(data).encode(encoding)  # Преобразуем числа в строку, затем в байты
    elif isinstance(data, (list, tuple, set, dict)):
        return str(data).encode(encoding)  # Преобразуем сложные структуры в строку, затем в байты
    else:
        raise TypeError(f"Неподдерживаемый тип данных: {type(data)}")


with open("C:\\ЛЭТИ 2 курс\\АиСД 4 сем\\файлы\\чехов.txt", 'r', encoding='UTF-8') as file:
    data = file.read()

prepared_data = to_bytes(data)
print(data)

def compression_ratio(original_size, compressed_size):
    return original_size/compressed_size
def test_lz77_compression(data, buffer_sizes):
    ratios = []
    for buffer_size in buffer_sizes:
        print(buffer_size)
        encoded_data = lz77_encode(data,2048,buffer_size)
        ratio = compression_ratio(len(data), len(encoded_data))
        ratios.append(ratio)
        print(f"Buffer size: {buffer_size}, Compression ratio: {ratio:.2f}")
    return ratios
k = len(data)
kk = k//10
buffer_sizes = [2**i for i in range(0,8)]

ratios = test_lz77_compression(prepared_data, buffer_sizes)
import matplotlib.pyplot as plt
plt.plot(buffer_sizes, ratios, marker='o',color = 'orange')
plt.xlabel("Размер буфера")
plt.ylabel("Коэффициент сжатия")
plt.title("Зависимость коэффициента сжатия от размера буфера")
plt.grid(True)
plt.show()