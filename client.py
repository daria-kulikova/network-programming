#!/usr/bin/env python
# coding: utf-8

import socket

def string2bits(s = ''):
    return ''.join([bin(ord(i))[2:].zfill(8) for i in s])



def get_words(data, word_length):
    while len(data) % word_length:
        data += '0'
    for i in range(len(data)):
        if not i % word_length:
            yield data[i:i + word_length]
            
            
            
def hamming_encode(data, control_bits):
    for i in control_bits:
        data = data[:i] + '0' + data[i:]
    pow2 = 1
    for control_bit in control_bits:
        mult = 0
        for i in range(len(data) - control_bit):
            if i % (pow2 * 2) >= pow2:
                continue
            if data[control_bit + i] == '1':
                mult ^= 1
        if mult == 1:
            data = data[:control_bit] + '1' + data[control_bit + 1:]
        pow2 *= 2
    return data



def message_processing(message, word_length, control_bits):
    bits = string2bits(message)
    encoded_message = ''
    for word in get_words(bits, word_length):
        encoded_message += hamming_encode(word, control_bits)
    return encoded_message



def get_control_bits(word_length):
    control_bits = []
    bit = 1
    while bit < word_length + len(control_bits):
        if not bit & (bit - 1):
            control_bits.append(bit - 1)
        bit += 1
    return control_bits



word_length = 15  
control_bits = get_control_bits(word_length)
host = "127.0.0.1"
port = 8
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.send(message_processing('sakklmkwm wdqkm отыфл 38273 ds').encode())
result = sock.recv(1024)
sock.close()
print("Получено:", result)

