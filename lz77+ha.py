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

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq
def build_frequency_map(data):
    freq_map = {}
    for byte in data:
        freq_map[byte] = freq_map.get(byte, 0) + 1
    return freq_map
def build_huffman_tree(freq_map):
    nodes = [HuffmanNode(char=char, freq=freq) for char, freq in freq_map.items()]
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        nodes.append(merged)
    return nodes[0]
def build_code_table(root, code="", code_table=None):
    if code_table is None:
        code_table = {}
    if root is not None:
        if root.char is not None:
            code_table[root.char] = code
        build_code_table(root.left, code + "0", code_table)
        build_code_table(root.right, code + "1", code_table)
    return code_table
def huffman_encode(data):
    if not data:
        return b"", {}, 0
    freq_map = build_frequency_map(data)
    root = build_huffman_tree(freq_map)
    code_table = build_code_table(root)
    encoded_bits = "".join(code_table[byte] for byte in data)
    padding = (8 - len(encoded_bits) % 8)
    encoded_bits += "0" * padding
    encoded_bytes = bytearray()
    for i in range(0, len(encoded_bits), 8):
        byte = encoded_bits[i:i + 8]
        encoded_bytes.append(int(byte, 2))
    return bytes(encoded_bytes), code_table, padding
def huffman_decode(encoded_data, code_table, padding):
    if not encoded_data:
        return b""
    encoded_bits = "".join(f"{byte:08b}" for byte in encoded_data)
    encoded_bits = encoded_bits[:-padding] if padding > 0 else encoded_bits
    reverse_code_table = {code: char for char, code in code_table.items()}
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
    if number == 1: return "enwik7", "lz77+HA_enwik7_encoded.txt", "lz77+HA_enwik7_decoded.txt"
    if number == 2: return "чехов.txt", "lz77+HA_чехов_encoded.txt", "lz77+HA_чехов_decoded.txt"
    if number == 3: return "SafeMain.exe", "lz77+HA_encoded.txt", "lz77+HA_exe_decoded.txt"
    if number == 4: return "фото_чб.bmp", "lz77+HA_ФОТО_ЧБ_encoded.txt", "lz77+HA_ФОТО_ЧБ_decoded.txt"
    if number == 5: return "piter.bmp", "lz77+HA_ФОТО_СЕРОЕ_encoded.txt", "lz77+HA_ФОТО_СЕРОЕ_decoded.txt"
    if number == 6: return "panda.bmp", "lz77+HA_ФОТО_ЦВЕТ_encoded.txt", "lz77+HA_ФОТО_ЦВЕТ_decoded.txt"
    if number == 7: return "english.txt", "lz77+HA_english_encoded.txt", "lz77+HA_english_decoded.txt"

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

def compress_and_decompress(input_file_path, compressed_file_path, decompressed_file_path):
    with open(input_file_path, 'rb') as file:
        original_data = file.read()

    en_data1= lz77_encode(original_data)
    en_data2, t, p = huffman_encode(en_data1)

    with open(compressed_file_path, 'wb') as file:
        file.write(en_data2)
    with open(compressed_file_path, 'rb') as file:
        read_compressed_data = file.read()

    de_data1 = huffman_decode(read_compressed_data,t,p)
    de_data2 = lz77_decode(de_data1)

    with open(decompressed_file_path, 'wb') as file:
        file.write(de_data2)

    original_size = len(original_data)
    compressed_size = len(en_data2)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 0
    is_match = original_data == de_data2

    print(f"Исходный размер: {original_size}")
    print(f"Размер после сжатия: {compressed_size}")
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")
    print(f"Декодированные данные правильные: {is_match}")
    print(f"Размер после декодирования: {len(de_data2)}")

compress_and_decompress(input_file, compressed_file, decompressed_file)