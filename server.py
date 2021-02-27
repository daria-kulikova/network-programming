#!/usr/bin/env python
# coding: utf-8

import socket, string

def get_blocks(data):
    for i in range(len(data) + len(control_bits)):
        if i % (word_length + len(control_bits)) == 0:
            yield data[i:i+word_length+len(control_bits)]
            
def hamming_decode(data):
    mistake_ind = 0
    pow2 = 1
    for ind in range(len(control_bits)):
        i = control_bits[ind]
        num1 = 0
        for j in range(len(data) - i):
            if j % (pow2 * 2) >= pow2:
                continue
            if data[i + j] == '1':
                num1 ^= 1
        if num1 == 1:
            mistake_ind |= (1 << ind)
        pow2 *= 2
    return mistake_ind
            
def proccess_msg(data):
    mistakes = []
    ind = 0
    for block in get_blocks(data):
        m = hamming_decode(block)
        if m != 0:
            if m > len(block):
                m = "Множественная ошибка"
            mistakes.append((ind, m))
        ind += 1
    return mistakes


word_length = 15
control_bits = []
i = 1
while i < word_length + len(control_bits):
    if not i & (i - 1):
        control_bits.append(i - 1)
    i += 1
host = "127.0.0.1"
port = 8
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((host, port))



while True:
    print("Слушаю порт " + str(port))
    srv.listen(True)
    sock, adr = srv.accept()
    while True:
        msg = sock.recv(1024).decode() # 1024 - число байт в очередной порции
        if not msg:
            break
        print("Получено от %s:%s:" % adr, msg)
        ans = proccess_msg(msg)
        print("Отправлено %s:%s:" % adr, ans)
        sock.send(ans)
    sock.close()
