import argparse
import heapq
import sys
from collections import Counter
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(frequencies):
    heap = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]



def read_file(file_name):
    with open(file_name,"r",encoding="utf-8") as file:
      return file.read()


def print_huffman_tree(root, level=0, prefix="Root: "):
    if root is None:
        return
    indent = " " * (4 * level)
    if root.char:
        print(f"{indent}{prefix}'{root.char}' (Freq: {root.freq})")
    else:
        print(f"{indent}{prefix}(Freq: {root.freq})")
        print_huffman_tree(root.left, level + 1, "L: ")
        print_huffman_tree(root.right, level + 1, "R: ")


def generate_prefix_codes(root):
    def _generate_codes(node,prefix,code_table):
        if not node:
            return
        if node.char is not None:
            code_table[node.char] = prefix
            return
        _generate_codes(node.left,prefix+"0",code_table)
        _generate_codes(node.right,prefix+"1",code_table)

    code_table = {}
    _generate_codes(root, "", code_table)
    return code_table


def serialize_tree(root):
    if not root:
        return ""
    if root.char:
        return f"L{root.char}"
    return f"I{serialize_tree(root.left)}{serialize_tree(root.right)}"


def encode_text(text, code_table):
    encoded_bits = ''.join(code_table[char] for char in text)
    encoded_bytes = int(encoded_bits,2).to_bytes((len(encoded_bits) + 7) // 8, byteorder='big')
    return encoded_bits, encoded_bytes


def encode(input,output):
    # if len(args) < 2:
    #     print("Usage: compress [file]")
    #     sys.exit(1)
    # file_name = args[1]
    # if not file_name:
    #     raise ValueError("Please provide a file name in args")
    file_content = read_file(input)
    frequencies = Counter(file_content)
    root = build_huffman_tree(frequencies)
    print_huffman_tree(root)
    code_table = generate_prefix_codes(root)
    serialized_tree = serialize_tree(root)
    encoded_bits, encoded_bytes = encode_text(file_content, code_table)

    with open(output, 'wb') as out:
        out.write(len(serialized_tree).to_bytes(4, byteorder='big'))
        out.write(serialized_tree.encode('utf-8'))  # Tree
        out.write(len(encoded_bits).to_bytes(4, byteorder='big'))
        out.write(encoded_bytes)  # Compressed data

    print(f"File compressed successfully: {output}")


def deserialize_tree(serialized_tree):
    pass


def decode_text(encoded_bytes, root, bit_count):
    pass


def decompress(input_file,output_file):
    with open(input_file, "rb") as file:
        tree_length = int.from_bytes(file.read(4), byteorder='big')
        serialized_tree = file.read(tree_length).decode('utf-8')
        bit_count = int.from_bytes(file.read(4), byteorder='big')
        encoded_bytes = file.read()

    root = deserialize_tree(serialized_tree)
    decoded_text = decode_text(encoded_bytes, root, bit_count)

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(decoded_text)

    print(f"File decompressed successfully: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Huffman Encoder/Decoder Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compress_parser = subparsers.add_parser("compress", help="Compress a file")
    compress_parser.add_argument("input", help="Input file to compress")
    compress_parser.add_argument("output", help="Output compressed file")

    decompress_parser = subparsers.add_parser("decompress", help="Decompress a file")
    decompress_parser.add_argument("input", help="Input file to decompress")
    decompress_parser.add_argument("output", help="Output decompressed file")
    args = parser.parse_args()
    if args.command == "compress":
        encode(args.input, args.output)
    # elif args.command == "decompress":
    #     decompress(args.input, args.output)

