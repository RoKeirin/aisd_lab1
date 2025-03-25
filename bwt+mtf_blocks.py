import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from math import log2


def calculate_entropy(data):
    if not data:
        return 0
    counter = Counter(data)
    probabilities = [count / len(data) for count in counter.values()]
    entropy = -sum(p * log2(p) for p in probabilities)
    return entropy

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

def analyze_bwt_mtf_entropy(file_path, block_sizes):
    with open(file_path, 'rb') as f:
        data = f.read()
    print(f'размер файла: {len(data)}')
    entropy_values = []
    for chunk_size in block_sizes:
        bwt_data,ind = bwt(data, chunk_size)
        print(bwt_data)
        mtf_data= mtf_encode(bwt_data)
        print(mtf_data)
        entropy = calculate_entropy(mtf_data)
        entropy_values.append(entropy)
        print(f"Block size: {chunk_size}, Entropy: {entropy}")
        mtf_decoded = mtf_decode(mtf_data)
        bwt_decoded = bwt_decode(mtf_decoded, ind, chunk_size)
        if bwt_decoded == data:
            print(f"Block size {chunk_size}: Data restored correctly.")
        else:
            print(f"Block size {chunk_size}: Data restoration failed!")

    plt.plot(block_sizes, entropy_values, marker='o',color = 'orange')
    plt.xlabel('Размер блока (в байтах)')
    plt.ylabel('Энтропия')
    plt.title('Зависимость энтропии от размера блока')
    plt.grid(True)
    plt.show()

file_path = "C:\\ЛЭТИ 2 курс\\АиСД 4 сем\\файлы\\enwik7"
block_sizes = [x for x in range(500,15000,1000)]

analyze_bwt_mtf_entropy(file_path, block_sizes)