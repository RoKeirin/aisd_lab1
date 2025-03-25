def bwt(data, chunk_size):
    transformed_data = bytearray()
    ind = []
    for start in range(0, len(data), chunk_size):
        chunk = data[start:start + chunk_size]
        index, encoded_chunk = transform_chunk(chunk)
        transformed_data.extend(encoded_chunk)
        ind.append(index)
    return bytes(transformed_data), ind
def transform_chunk(chunk):
    rotations = [chunk[i:] + chunk[:i] for i in range(len(chunk))]
    rotations.sort()
    original_index = rotations.index(chunk)
    encoded_chunk = bytes(rotation[-1] for rotation in rotations)
    return original_index, encoded_chunk
def bwt_decode(encoded_data, indices, chunk_size):
    restored_data = bytearray()
    position = 0
    index = 0
    while position < len(encoded_data):
        end = position + chunk_size if position + chunk_size <= len(encoded_data) else len(encoded_data)
        chunk = encoded_data[position:end]
        original_index = indices[index]
        restored_chunk = reverse_transform_chunk(original_index, chunk)
        restored_data.extend(restored_chunk)
        position = end
        index += 1
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

def mtf_encode(data: bytes) -> bytes:
    alphabet = bytearray(range(256))
    encoded = bytearray()
    for byte in data:
        index = alphabet.index(byte)
        encoded.append(index)
        del alphabet[index]
        alphabet.insert(0, byte)
    return bytes(encoded)
def mtf_decode(encoded_data: bytes) -> bytes:
    """Декодирование данных алгоритмом Move-To-Front."""
    # Инициализация алфавита (0-255)
    alphabet = bytearray(range(256))
    decoded = bytearray()

    for index in encoded_data:
        # Получаем символ по индексу
        byte = alphabet[index]
        decoded.append(byte)

        # Перемещаем символ в начало алфавита
        del alphabet[index]
        alphabet.insert(0, byte)

    return bytes(decoded)
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
            encoded_data.append(count)  # Старший бит 0
            encoded_data.append(current_char)
            i += count
        else:
            non_repeat_chars = bytearray()
            non_repeat_chars.append(current_char)
            i += 1
            while i < n and (i + 1 >= n or data[i] != data[i + 1]) and len(non_repeat_chars) < 127:
                non_repeat_chars.append(data[i])
                i += 1
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
            length = control_byte & 0x7F
            decoded_data.extend(encoded_data[i:i + length])
            i += length
        else:
            count = control_byte
            char = encoded_data[i]
            decoded_data.extend([char] * count)
            i += 1
    return bytes(decoded_data)

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char  # Символ (байт)
        self.freq = freq  # Частота символа
        self.left = left  # Левый потомок
        self.right = right  # Правый потомок

    def __lt__(self, other):
        # Для сравнения узлов в куче
        return self.freq < other.freq
def build_frequency_map(data):
    """
    Строит частотный словарь для символов в данных.
    """
    freq_map = {}
    for byte in data:
        freq_map[byte] = freq_map.get(byte, 0) + 1
    return freq_map
def build_huffman_tree(freq_map):
    """
    Строит дерево Хаффмана на основе частотного словаря.
    """
    # Создаем список узлов
    nodes = [HuffmanNode(char=char, freq=freq) for char, freq in freq_map.items()]

    # Построение дерева Хаффмана
    while len(nodes) > 1:
        # Сортируем узлы по частоте (вручную, без heapq)
        nodes.sort(key=lambda x: x.freq)

        # Извлекаем два узла с наименьшими частотами
        left = nodes.pop(0)
        right = nodes.pop(0)

        # Создаем новый узел с суммой частот
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)

        # Добавляем новый узел в список
        nodes.append(merged)

    # Возвращаем корень дерева
    return nodes[0]
def build_code_table(root, code="", code_table=None):
    """
    Генерирует таблицу кодов Хаффмана.
    """
    if code_table is None:
        code_table = {}

    if root is not None:
        if root.char is not None:
            # Если это лист, сохраняем код
            code_table[root.char] = code
        # Рекурсивно обходим левое и правое поддерево
        build_code_table(root.left, code + "0", code_table)
        build_code_table(root.right, code + "1", code_table)

    return code_table
def huffman_encode(data):
    """
    Кодирует данные с использованием алгоритма Хаффмана.
    Возвращает закодированные данные, таблицу кодов и длину дополнения.
    """
    if not data:
        return b"", {}, 0

    # Подсчет частот символов
    freq_map = build_frequency_map(data)

    # Построение дерева Хаффмана
    root = build_huffman_tree(freq_map)

    # Генерация кодовой таблицы
    code_table = build_code_table(root)

    # Кодирование данных
    encoded_bits = "".join(code_table[byte] for byte in data)

    # Дополнение битов до длины, кратной 8
    padding = (8 - len(encoded_bits) % 8)
    encoded_bits += "0" * padding

    # Преобразование битовой строки в байты
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_bits), 8):
        byte = encoded_bits[i:i + 8]
        encoded_bytes.append(int(byte, 2))

    return bytes(encoded_bytes), code_table, padding
def huffman_decode(encoded_data, code_table, padding):
    """
    Декодирует данные, закодированные алгоритмом Хаффмана.
    """
    if not encoded_data:
        return b""

    # Преобразование байтов в битовую строку
    encoded_bits = "".join(f"{byte:08b}" for byte in encoded_data)
    encoded_bits = encoded_bits[:-padding] if padding > 0 else encoded_bits

    # Обратная кодовая таблица
    reverse_code_table = {code: char for char, code in code_table.items()}

    # Декодирование
    decoded_data = bytearray()
    current_code = ""
    for bit in encoded_bits:
        current_code += bit
        if current_code in reverse_code_table:
            decoded_data.append(reverse_code_table[current_code])
            current_code = ""

    return bytes(decoded_data)

def files():
    print('Выберете файл для сжатия\n1 - enwik7\n2 - текст на русском\n3 - exe файл\n4 - чб изображение\n5 - изображение в серых оттенках\n6 - цветное изображение\n7 - текст на английском')
    number = int(input())
    print(f'Ваш выбор: ',number)
    if number == 1: return "enwik7", "bwt+mtf+rle+ha_enwik7_encoded.txt", "bwt+mtf+rle+ha_enwik7_decoded.txt"
    if number == 2: return "чехов.txt", "bwt+mtf+rle+ha_чехов_encoded.txt", "bwt+mtf+rle+ha_чехов_decoded.txt"
    if number == 3: return "SafeMain.exe", "bwt+mtf+rle+ha_exe_encoded.txt", "bwt+mtf+rle+ha_exe_decoded.txt"
    if number == 4: return "фото_чб.bmp", "bwt+mtf+rle+ha_ФОТО_ЧБ_encoded.txt", "bwt+mtf+rle+ha_ФОТО_ЧБ_decoded.txt"
    if number == 5: return "piter.bmp", "bwt+mtf+rle+ha_ФОТО_СЕРОЕ_encoded.txt", "bwt+mtf+rle+ha_ФОТО_СЕРОЕ_decoded.txt"
    if number == 6: return "panda.bmp", "bwt+mtf+rle+ha_ФОТО_ЦВЕТ_encoded.bin", "bwt+mtf+rle+ha_ФОТО_ЦВЕТ_decoded.bin"
    if number == 7: return "english.txt", "bwt+mtf+rle+ha_english_encoded.txt", "bwt+mtf+rle+ha_english_decoded.txt"

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
    compressed_data2 = mtf_encode(compressed_data1)

    compressed_data3 = rle_encode(compressed_data2)

    compressed_data4, t, p = huffman_encode(compressed_data3)

    with open(compressed_file_path, 'wb') as file:
        file.write(compressed_data4)
    with open(compressed_file_path, 'rb') as file:
        read_compressed_data = file.read()

    decompressed_data1 = huffman_decode(read_compressed_data,t,p)

    decompressed_data2 = rle_decode(decompressed_data1)

    decompressed_data3 = mtf_decode(decompressed_data2)

    decompressed_data4 = bwt_decode(decompressed_data3,indexes, ch_size)

    with open(decompressed_file_path, 'wb') as file:
        file.write(decompressed_data4)

    original_size = len(original_data)
    compressed_size = len(compressed_data4)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 0

    is_match = original_data == decompressed_data4

    print(f"Исходный размер: {original_size}")
    print(f"Размер после сжатия: {compressed_size}")
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")
    print(f"Декодированные данные правильные: {is_match}")

compress_and_decompress(input_file, compressed_file, decompressed_file)



