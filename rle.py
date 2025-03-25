def rle_encode(data):
    encoded_data = bytearray()
    n = len(data)
    i = 0
    while i < n:
        current_char = data[i]
        count = 1
        while i + count < n and data[i + count] == current_char and count < 127:
            count += 1
        if count > 1:
            encoded_data.append(count)
            encoded_data.append(current_char)
            i += count
        else:
            non_repeat_chars = bytearray()
            non_repeat_chars.append(current_char)
            i += 1
            while i < n and (i + 1 >= n or data[i] != data[i + 1]) and len(non_repeat_chars) < 127:
                non_repeat_chars.append(data[i])
                i += 1
            encoded_data.append(0x80 | len(non_repeat_chars))
            encoded_data.extend(non_repeat_chars)
    return bytes(encoded_data)
def rle_decode(encoded_data):
    decoded_data = bytearray()
    n = len(encoded_data)
    i = 0
    while i < n:
        control_byte = encoded_data[i]
        i += 1
        if control_byte & 0x80:
            length = control_byte & 0x7F
            decoded_data.extend(encoded_data[i:i + length])
            i += length
        else:
            count = control_byte
            char = encoded_data[i]
            decoded_data.extend([char] * count)
            i += 1
    return bytes(decoded_data)

def files():
    print('Выберете файл для сжатия\n1 - enwik7\n2 - текст на русском\n3 - рандомный файл\n4 - чб изображение\n5 - изображение в серых оттенках\n6 - цветное изображение\n7 - текст на английском')
    number = int(input())
    print(f'Ваш выбор: ',number)
    if number == 1: return "enwik7", "rle_enwik7_encoded.txt", "rle_enwik7_decoded.txt"
    if number == 2: return "чехов.txt", "rle_чехов_encoded.txt", "rle_чехов_decoded.txt"
    if number == 3: return "SafeMain.exe", "rle_exe_encoded.txt", "rle_exe_decoded.txt"
    if number == 4: return "фото_чб.bmp", "rle_фото_ЧБ_encoded.txt", "rle_фото_ЧБ_decoded.txt"
    if number == 5: return "piter.bmp", "rle_фото_серый_encoded.txt", "rle_фото_серый_decoded.txt"
    if number == 6: return "panda.bmp", "rle_ФОТО_ЦВЕТ_encoded.bin", "rle_ФОТО_ЦВЕТ_decoded.bin"
    if number == 7: return "english.txt", "rle_english_encoded.txt", "rle_english_decoded.txt"

file_1,file_2,file_3 = files()
def get_file_path(base_path, file_name, file_extension=""):
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

def compress_and_decompress(input_file_path, compressed_file_path, decompressed_file_path):
    with open(input_file_path, 'rb') as file:
        original_data = file.read()
    # print(original_data)
    compressed_data = rle_encode(original_data)
    # print(compressed_data)
    with open(compressed_file_path, 'wb') as file:
        file.write(compressed_data)
    with open(compressed_file_path, 'rb') as file:
        read_compressed_data = file.read()
    decompressed_data = rle_decode(read_compressed_data)
    with open(decompressed_file_path, 'wb') as file:
        file.write(decompressed_data)

    original_size = len(original_data)
    compressed_size = len(compressed_data)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 0

    is_match = original_data == decompressed_data

    print(f"Исходный размер: {original_size}")
    print(f"Размер после сжатия: {compressed_size}")
    print(f"Размер после декодирования: {len(decompressed_data)}")
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")
    print(f"Декодированные данные правильные: {is_match}")

compress_and_decompress(input_file, compressed_file, decompressed_file)