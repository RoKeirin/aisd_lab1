def lz77_encode(data, window_size=1024, lookahead_buffer_size=16):
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

def files():
    print('Выберете файл для сжатия\n1 - enwik7\n2 - текст на русском\n3 - exe файл\n4 - чб изображение\n5 - изображение в серых оттенках\n6 - цветное изображение\n7 - текст на английском')
    number = int(input())
    print(f'Ваш выбор: ',number)
    if number == 1: return "enwik7", "lz77_enwik7_encoded.txt", "lz77_enwik7_decoded.txt"
    if number == 2: return "чехов.txt", "lz77_чехов_encoded.txt", "lz77_чехов_decoded.txt"
    if number == 3: return "SafeMain.exe", "lz77_exe_encoded.txt", "lz77_exe_decoded.txt"
    if number == 4: return "фото_чб.bmp", "lz77_ФОТО_ЧБ_encoded.txt", "lz77_ФОТО_ЧБ_decoded.txt"
    if number == 5: return "piter.bmp", "lz77_ФОТО_СЕРОЕ_encoded.txt", "lz77_ФОТО_СЕРОЕ_decoded.txt"
    if number == 6: return "panda.bmp", "lz77_ФОТО_ЦВЕТ_encoded.txt", "lz77_ФОТО_ЦВЕТ_decoded.txt"
    if number == 7: return "english.txt", "lz77_english_encoded.txt", "lz77_english_decoded.txt"

file_1,file_2,file_3 = files()
def get_file_path(base_path, file_name):
    return f"{base_path}\\{file_name}"
base_path = r"C:\ЛЭТИ 2 курс\АиСД 4 сем\файлы"
file_name1 =  file_1
full_path1 = get_file_path(base_path, file_name1)
file_name2 =  file_2
full_path2 = get_file_path(base_path, file_name2)
file_name3 =  file_3
full_path3 = get_file_path(base_path, file_name3)

input_file = full_path1
compressed_file = full_path2
decompressed_file = full_path3

# print(lz77_encode(b'banana',1024,10))


def compress_and_decompress(input_file_path, compressed_file_path, decompressed_file_path):
    with open(input_file_path, 'rb') as file:
        original_data = file.read()
    en_data1= lz77_encode(original_data)
    with open(compressed_file_path, 'wb') as file:
        file.write(en_data1)
    with open(compressed_file_path, 'rb') as file:
        read_compressed_data = file.read()

    de_data1 = lz77_decode(read_compressed_data)
    with open(decompressed_file_path, 'wb') as file:
        file.write(de_data1)

    original_size = len(original_data)
    compressed_size = len(en_data1)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 0
    is_match = original_data == de_data1

    print(f"Исходный размер: {original_size}")
    print(f"Размер после сжатия: {compressed_size}")
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")
    print(f"Декодированные данные правильные: {is_match}")
    print(f"Размер после декодирования: {len(de_data1)}")

compress_and_decompress(input_file, compressed_file, decompressed_file)