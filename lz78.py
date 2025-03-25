import os
def lz78_encode(data: bytes) -> bytes:
    dictionary = {}
    output = []
    current_string = bytearray()
    index = 1
    i = 0
    while i < len(data):
        current_string.append(data[i])
        current_bytes = bytes(current_string)
        if current_bytes in dictionary:
            i += 1
        else:
            output.append((dictionary.get(bytes(current_string[:-1]), 0), current_string[-1]))
            dictionary[current_bytes] = index
            index += 1
            current_string = bytearray()
            i += 1

    if current_string:
        output.append((dictionary.get(bytes(current_string[:-1]), 0), current_string[-1]))

    compressed_data = bytearray()
    for pair in output:
        index_bytes = pair[0].to_bytes(4, 'big')
        char_bytes = bytes([pair[1]])
        compressed_data.extend(index_bytes + char_bytes)

    return bytes(compressed_data)
def lz78_decode(compressed_data: bytes) -> bytes:
    dictionary = {}
    output = bytearray()
    index = 1
    i = 0

    while i < len(compressed_data):
        index_bytes = compressed_data[i:i + 4]
        current_index = int.from_bytes(index_bytes, 'big')
        i += 4

        char_bytes = compressed_data[i:i + 1]
        char = char_bytes[0]
        i += 1

        if current_index == 0:
            output.append(char)
            dictionary[index] = bytearray([char])
        else:
            string_from_dict = dictionary[current_index]
            output.extend(string_from_dict)
            output.append(char)
            dictionary[index] = string_from_dict + bytearray([char])
        index += 1

    return bytes(output)


def files():
    print('Выберете файл для сжатия\n1 - enwik7\n2 - текст на русском\n3 - exe файл\n4 - чб изображение\n5 - изображение в серых оттенках\n6 - цветное изображение\n7 - текст на английском')
    number = int(input())
    print(f'Ваш выбор: ',number)
    if number == 1: return "enwik7", "LZ78_enwik7_encoded.txt", "LZ78_enwik7_decoded.txt"
    if number == 2: return "чехов.txt", "LZ78_чехов_encoded.txt", "LZ78_чехов_decoded.txt"
    if number == 3: return "SafeMain.exe", "lz78_encoded.txt", "lz78_exe_decoded.txt"
    if number == 4: return "фото_чб.bmp", "lz78_ФОТО_ЧБ.txt", "lz78_ФОТО_ЧБ_decoded.txt"
    if number == 5: return "piter.bmp", "lz78_ФОТО_СЕРОЕ.txt", "lz78_ФОТО_СЕРОЕ_decoded.txt"
    if number == 6: return "panda.bmp", "LZ78_ФОТО_ЦВЕТ_encoded.txt", "LZ78_ФОТО_ЦВЕТ_decoded.txt"
    if number == 7: return "english.txt", "LZ78_english_encoded.txt", "LZ78_english_decoded.txt"

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

def compress_and_decompress(input_file, compressed_file, decompressed_file):
    with open(input_file, 'rb') as f1:
        orig_data = f1.read()

    en_data = lz78_encode(orig_data)
    with open(compressed_file, 'wb') as f2:
        f2.write(en_data)

    orig_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    ratio = orig_size / compressed_size

    with open(compressed_file, 'rb') as f3:
        compressed_data = f3.read()

    de_data = lz78_decode(compressed_data)
    with open(decompressed_file, 'wb') as output_file:
        output_file.write(de_data)

    is_match = orig_data == de_data
    print(f"Исходный размер: {orig_size}")
    print(f"Размер после сжатия: {compressed_size}")
    print(f"Коэффициент сжатия: {ratio:.3f}")
    print(f"Декодированные данные правильные: {is_match}")

compress_and_decompress(input_file, compressed_file, decompressed_file)
