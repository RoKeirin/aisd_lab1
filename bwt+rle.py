def bwt(data, chunk_size):
    transformed_data = bytearray()
    indices = []  # Список для хранения индексов исходной строки
    for start in range(0, len(data), chunk_size):
        chunk = data[start:start + chunk_size]
        index, encoded_chunk = transform_chunk(chunk)  # Получаем индекс и закодированный блок
        transformed_data.extend(encoded_chunk)
        indices.append(index) # Сохраняем индекс
    return bytes(transformed_data), indices
def transform_chunk(chunk):
    rotations = [chunk[i:] + chunk[:i] for i in range(len(chunk))]
    rotations.sort()
    original_index = rotations.index(chunk)  # Индекс исходной строки
    encoded_chunk = bytes(rotation[-1] for rotation in rotations)  # Последние символы
    return original_index, encoded_chunk
def bwt_decode(encoded_data, indices, chunk_size):
    restored_data = bytearray()
    position = 0
    indd = 0
    while position < len(encoded_data):
        end = position + chunk_size if position + chunk_size <= len(encoded_data) else len(encoded_data)
        chunk = encoded_data[position:end]
        original_index = indices[indd] # Получаем индекс исходной строки
        restored_chunk = reverse_transform_chunk(original_index, chunk)
        restored_data.extend(restored_chunk)
        position = end
        indd+=1
    return bytes(restored_data)
def reverse_transform_chunk(original_index, encoded_chunk):
    table = [(char, idx) for idx, char in enumerate(encoded_chunk)]
    table.sort()
    result = bytearray()
    current_row = original_index
    for _ in range(len(encoded_chunk)):
        char, current_row = table[current_row]
        result.append(char)
    return bytes(result)

def rle_encode(data):
    encoded_data = bytearray()
    n = len(data)
    i = 0

    while i < n:
        # Начинаем с текущего символа
        current_char = data[i]
        count = 1

        # Считаем количество повторов
        while i + count < n and data[i + count] == current_char and count < 127:
            count += 1

        if count > 1:
            # Если символ повторяется, добавляем (количество, символ)
            encoded_data.append(count)  # Старший бит 0
            encoded_data.append(current_char)
            i += count
        else:
            # Если символ не повторяется, ищем неповторяющуюся последовательность
            non_repeat_chars = bytearray()
            non_repeat_chars.append(current_char)
            i += 1

            # Собираем неповторяющиеся символы
            while i < n and (i + 1 >= n or data[i] != data[i + 1]) and len(non_repeat_chars) < 127:
                non_repeat_chars.append(data[i])
                i += 1

            # Добавляем управляющий символ (старший бит 1) и последовательность
            encoded_data.append(0x80 | len(non_repeat_chars))  # Старший бит 1
            encoded_data.extend(non_repeat_chars)

    return bytes(encoded_data)
def rle_decode(encoded_data):
    decoded_data = bytearray()
    n = len(encoded_data)
    i = 0

    while i < n:
        control_byte = encoded_data[i]
        i += 1

        if control_byte & 0x80:  # Если старший бит равен 1
            # Неповторяющаяся последовательность
            length = control_byte & 0x7F  # Длина последовательности
            decoded_data.extend(encoded_data[i:i + length])
            i += length
        else:
            # Повторяющаяся последовательность
            count = control_byte
            char = encoded_data[i]
            decoded_data.extend([char] * count)
            i += 1

    return bytes(decoded_data)


def files():
    print('Выберете файл для сжатия\n1 - enwik7\n2 - текст на русском\n3 - exe файл\n4 - чб изображение\n5 - изображение в серых оттенках\n6 - цветное изображение\n7 - текст на английском')
    number = int(input())
    print(f'Ваш выбор: ',number)
    if number == 1: return "enwik7", "bwt+rle_enwik7_encoded.txt", "bwt+rle_enwik7_decoded.txt"
    if number == 2: return "чехов.txt", "bwt+rle_чехов_encoded.txt", "bwt+rle_чехов_decoded.txt"
    if number == 3: return "SafeMain.exe", "bwt+rle_exe_encoded.txt", "bwt+rle_exe_decoded.txt"
    if number == 4: return "фото_чб.bmp", "bwt+rle_фото_ЧБ.txt", "bwt+rle_фото_ЧБ_decoded.txt"
    if number == 5: return "piter.bmp", "bwt+rle_фото_СЕРОЕ.txt", "bwt+rle_фото_СЕРОЕ_decoded.txt"
    if number == 6: return "panda.bmp", "bwt+rle_ФОТО_ЦВЕТ_encoded.txt", "bwt+rle_ФОТО_ЦВЕТ_decoded.txt"
    if number == 7: return "english.txt", "bwt+rle_english_encoded.txt", "bwt+rle_english_decoded.txt"

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
    ch_size = 1024
    with open(input_file_path, 'rb') as file:
        original_data = file.read()
    # print(original_data)
    compressed_data1, indexes = bwt(original_data,ch_size)
    # print(compressed_data)
    compressed_data2 = rle_encode(compressed_data1)

    with open(compressed_file_path, 'wb') as file:
        file.write(compressed_data2)
    with open(compressed_file_path, 'rb') as file:
        read_compressed_data = file.read()

    decompressed_data1 = rle_decode(read_compressed_data)
    decompressed_data2 = bwt_decode(decompressed_data1,indexes,ch_size)

    with open(decompressed_file_path, 'wb') as file:
        file.write(decompressed_data2)

    original_size = len(original_data)
    compressed_size = len(compressed_data2)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 0

    is_match = original_data == decompressed_data2

    print(f"Исходный размер: {original_size}")
    print(f"Размер после сжатия: {compressed_size}")
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")
    print(f"Декодированные данные правильные: {is_match}")

compress_and_decompress(input_file, compressed_file, decompressed_file)