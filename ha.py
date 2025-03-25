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

print(huffman_encode(b'robot'))
def files():
    print('Выберете файл для сжатия\n1 - enwik7\n2 - текст на русском\n3 - exe файл\n4 - чб изображение\n5 - изображение в серых оттенках\n6 - цветное изображение\n7 - текст на английском')
    number = int(input())
    print(f'Ваш выбор: ',number)
    if number == 1: return "enwik7", "huff_enwik7_encoded.txt", "huff_enwik7_decoded.txt"
    if number == 2: return "чехов.txt", "huff_чехов_encoded.txt", "huff_чехов_decoded.txt"
    if number == 3: return "SafeMain.exe", "huff_exe_encoded.txt", "huff_exe_decoded.txt"
    if number == 4: return "фото_чб.bmp", "huff_фото_ЧБ_encoded.txt", "huff_фото_ЧБ_decoded.txt"
    if number == 5: return "piter.bmp", "huff_ФОТО_СЕРОЕ_encoded.txt", "huff_ФОТО_СЕРОЕ_decoded.txt"
    if number == 6: return "panda.bmp", "huff_ФОТО_ЦВЕТ_encoded.txt", "huff_ФОТО_ЦВЕТ_decoded.txt"
    if number == 7: return "english.txt", "huff_english_encoded.txt", "huff_english_decoded.txt"

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
    compressed_data, t, pad = huffman_encode(original_data)
    # print(compressed_data)
    with open(compressed_file_path, 'wb') as file:
        file.write(compressed_data)
    with open(compressed_file_path, 'rb') as file:
        read_compressed_data = file.read()
    decompressed_data = huffman_decode(read_compressed_data, t, pad)
    with open(decompressed_file_path, 'wb') as file:
        file.write(decompressed_data)

    original_size = len(original_data)
    compressed_size = len(compressed_data)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else 0

    is_match = original_data == decompressed_data

    print(f"Исходный размер: {original_size}")
    print(f"Размер после сжатия: {compressed_size}")
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")
    print(f"Декодированные данные правильные: {is_match}")

compress_and_decompress(input_file, compressed_file, decompressed_file)


