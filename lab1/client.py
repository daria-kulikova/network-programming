import socket
import pickle
import random
# from prettytable import PrettyTable as pt
# from colorama import Fore, Back, Style



def get_control_bits(word_length):
    control_bits = []
    bit = 1
    while bit < word_length + len(control_bits):
        if not bit & (bit - 1):
            control_bits.append(bit-1)
        bit += 1
    return control_bits



def string2bits(s = ''):
    return ''.join([bin(ord(i))[2:].zfill(8) for i in s])



def get_words(data, word_length):
    while len(data) % word_length:
        data += '0'
    for i in range(len(data)):
        if not i % word_length:
            yield data[i:i+word_length]



def hamming_encode(word, control_bits):
    for i in control_bits:
        word = word[:i] + '0' + word[i:]
    pow2 = 1
    for control_bit in control_bits:
        mult = 0
        for i in range(len(word) - control_bit):
            if i % (pow2 * 2) >= pow2:
                continue
            if word[control_bit+i] == '1':
                mult ^= 1
        if mult == 1:
            word = word[:control_bit] + '1' + word[control_bit+1:]
        pow2 *= 2
    return word



def message_processing(message, word_length, control_bits):
    bits = string2bits(message)
    message_length = len(bits)
    encoded_message = ''
    for word in get_words(bits, word_length):
        encoded_message += hamming_encode(word, control_bits)
    return encoded_message, message_length



def add_mistakes(data, word_length, mistakes_number):
    mistakes = []
    no_mistakes = 0
    one_mistake = 0
    many_mistakes = 0
    message_with_mistakes = ''
    p_word = 0.8
    p_in_word = 0.02
    word_index = 0
    for word in get_words(data, word_length):
        n = 0
        if random.random() < p_word:
            for i in range(len(word)):
                if n == mistakes_number:
                    break
                if random.random() < p_in_word:
                    s = '0'
                    if word[i] == '0':
                        s = '1'
                    word = word[:i] + s + word[i+1:]
                    n += 1
                    mistakes.append((word_index+1, i+1))
        if n == 0:
            no_mistakes += 1
        elif n == 1:
            one_mistake += 1
        else:
            many_mistakes += 1
        message_with_mistakes += word
        word_index += 1    
    return message_with_mistakes, no_mistakes, one_mistake, many_mistakes



# def print_mistakes(mistakes, mistakes_from_server):
#     red = '\033[0;31;40m'
#     reset = '\033[0m'
#     tb = pt()
#     tb.field_names = ['Номер слова', 'Добавленные ошибки, биты', 'Найденные сервером ошибки, биты']
#     ind = 0
#     srv_ind = 0
#     inf = len(mistakes) + len(mistakes_from_server) + 1
#     while True:
#         word_index = inf
#         if ind < len(mistakes):
#             word_index = mistakes[ind][0]
#         if srv_ind < len(mistakes_from_server):
#             word_index = min(word_index, mistakes_from_server[srv_ind][0])
#         if word_index == inf:
#             break
#         bits = ''
#         srv_bits = ''
#         while ind < len(mistakes) and mistakes[ind][0] == word_index:
#             if len(bits) > 0:
#                 bits += ', '
#             bits += str(mistakes[ind][1])
#             ind += 1
#         while srv_ind < len(mistakes_from_server) and mistakes_from_server[srv_ind][0] == word_index:
#             if len(srv_bits) > 0:
#                 srv_bits += ', '
#             srv_bits += str(mistakes_from_server[srv_ind][1])
#             srv_ind += 1
#         if bits != srv_bits:
#             tb.add_row([word_index, Back.RED+bits+Back.RESET, Back.RED+srv_bits+Back.RESET])
#         else:
#             tb.add_row([word_index, bits, srv_bits])
#     print(tb)



word_length = 60
control_bits = get_control_bits(word_length)
host = '127.0.0.1'
port = 45102



while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    
    message = input('Введите сообщение: ')
    processed_message, message_length = message_processing(message, word_length, control_bits)
    mistakes_number = int(input('Введите количество ошибок на слово: '))
    print()
    message_with_mistakes, no_mistakes, one_mistake, many_mistakes = add_mistakes(processed_message, word_length+len(control_bits), mistakes_number)
    print('Количество слов без ошибок: ', no_mistakes)
    print('Количество слов с 1 ошибкой: ', one_mistake)
    print('Количество слов с множественными ошибками: ', many_mistakes)
    print()
    sock.send(pickle.dumps((message_with_mistakes, word_length, message_length)))
    
    fixed, correctly_delivered, uncorrectly_delivered = pickle.loads(sock.recv(1024))
    sock.close()
    
    print('Получен ответ с сервера')
    print('Количество правильно доставленных слов: ', correctly_delivered)
    print('Количество неправильно доставленных слов: ', uncorrectly_delivered)
    print('Количество исправенных ошибок: ', fixed)
    print()
#     print_mistakes(mistakes, mistakes_from_server)

