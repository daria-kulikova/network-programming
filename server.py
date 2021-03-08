import socket
import string
import pickle
import random



def recv_all(sock):
    data = b''
    bufsize = 1024
    while True:
        packet = sock.recv(bufsize)
        data += packet
        if len(packet) < bufsize:
            break
    return data



def get_control_bits(word_length):
    control_bits = []
    bit = 1
    while bit < word_length + len(control_bits):
        if not bit & (bit - 1):
            control_bits.append(bit - 1)
        bit += 1
    return control_bits



def get_words(data, word_length, control_bits_number):
    for i in range(len(data)):
        if not i % (word_length + control_bits_number):
            yield data[i:i + word_length  + control_bits_number]



def hamming_decode(word, control_bits):
    bad_index = 0
    pow2 = 1
    for control_bit_index in range(len(control_bits)):
        control_bit = control_bits[control_bit_index]
        ones_number = 0
        for i in range(len(word) - control_bit):
            if i % (pow2 * 2) >= pow2:
                continue
            if word[control_bit + i] == '1':
                ones_number ^= 1
        if ones_number == 1:
            bad_index |= (1 << control_bit_index)
        pow2 *= 2
    return bad_index



def message_processing(message, word_length):
    control_bits = get_control_bits(word_length)
    mistakes = []
    corrected_message = ''
    correctly_delivered = 0
    uncorrectly_delivered = 0
    fixed = 0
    word_index = 0
    for word in get_words(message, word_length, len(control_bits)):
        bad_index = hamming_decode(word, control_bits)
        if bad_index != 0:
            uncorrectly_delivered += 1
            if bad_index > len(word):
                bad_index = "Множественные ошибки"
            else:
                fixed += 1
                s = '0'
                if word[bad_index-1] == '0':
                    s = '1'
                word = word[:bad_index-1] + s + word[bad_index:]
            mistakes.append((word_index + 1, bad_index))
        else:
            correctly_delivered += 1
        corrected_message += word
        word_index += 1
    return fixed, correctly_delivered, uncorrectly_delivered



host = "127.0.0.1"
port = 45102
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((host, port))
print('Сервер запущен')



while True:
    srv.listen(True)
    sock, address = srv.accept()
    print('Жду сообщение')
    while True:
        received = recv_all(sock)
        if not received:
            break
        message, word_length, message_length = pickle.loads(received)
        print('Сообщение получено')
        answer = message_processing(message, word_length)
        sock.send(pickle.dumps(answer))
        print('Ответ отправлен')
    sock.close()

