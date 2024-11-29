""" Development from Nina Nuñez Marco
https://github.com/Nina-99/Algorithm-Huffman"""

import json
import pickle
import re
import sys
from collections import Counter
from typing import Dict

from tree import Tree


def get_dictionary(file):
    frecuency = dict(Counter(file))
    frecuency["end"] = 1  # NOTE: Assign the point end to the finaly of dictionary
    tree = Tree(frecuency)
    # NOTE: Assign codes to each character based on its position in the tree
    codes = tree.code_to_dict()
    com = tree.__str__()
    return com, codes, frecuency


def compression(codes: Dict[str, str], file) -> str:
    encoded = ""
    for letter in file:
        encoded += codes[letter]
    encoded = "1" + encoded + codes["end"]
    if len(encoded) % 8 != 0:
        size = (((len(encoded) // 8) + 1) * 8) - len(encoded)
        encoded += size * "0"
    return int(encoded, 2), encoded


def decompression(outfile):
    with open(outfile + ".dic", "r") as filedic:
        codes = json.load(filedic)
    with open(outfile + ".bin", "rb") as file:
        word = pickle.load(file)
    bin_word = bin(word)[3:]  # NOTE: We remove three characters from the beginning
    decompress_str = ""
    capture = ""
    match = []
    if not re.search("^[01]+$", bin_word):
        raise ValueError("Corrupt File!")

    for bit in bin_word:
        capture += bit
        match.clear()
        for char, code in codes.items():
            if capture == code[0 : len(capture)]:
                match.append(char)

        if len(match) == 1:
            if match[0] == "end":
                break
            decompress_str += match[0]
            capture = ""
    return decompress_str, bin_word


def store(dic, compre):
    if sys.argv[2].upper() == "C":
        with open(sys.argv[1] + ".bin", "wb") as outf:
            pickle.dump(compre, outf)

        with open(sys.argv[1] + ".dic", "w") as outf:
            json.dump(dic, outf)
    else:
        with open(sys.argv[1], "w") as str:
            str.write(compre)


if __name__ == "__main__":
    example = (
        """Example: python3 huffman.py nameFile (c or d) compression or decompression"""
    )

    if len(sys.argv) < 3:
        print(example)
        sys.exit(1)

    if sys.argv[2].upper() == "C":
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            f = file.read().strip("\n")
        com, dictionary, frec = get_dictionary(f)
        print(frec)
        print(dictionary)
        print(com)
        compress, enc = compression(dictionary, f)
        print(enc)
        store(dictionary, compress)
        print(f"{len(f)} Bytes or {len(f)*8} bits")
        print("Successful Compression")
        print(f"{len(enc)/8} Byts or {len(enc)} bits")
    elif sys.argv[2].upper() == "D":
        decompress, bi_word = decompression(sys.argv[1])
        print(bi_word)
        store(None, decompress)
        print("Successful Decompression")
    else:
        print(example)
