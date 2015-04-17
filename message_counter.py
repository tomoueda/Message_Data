import fileinput

def main():
    tomo_word_count = 0
    logan_word_count = 0
    tomo_message_count = 0
    logan_message_count = 0
    for line in fileinput.input():
        tokenized_line = line.split()
        if tokenized_line:
            if tokenized_line[len(tokenized_line) - 1] == '0':
                logan_word_count += len(tokenized_line) - 1
                logan_message_count += 1
            else:
                tomo_word_count += len(tokenized_line) - 1
                tomo_message_count += 1
    print 'tomo_word_count messaging ', tomo_word_count
    print 'logan_word_count messaging', logan_word_count
    print 'tomo_message count', tomo_message_count
    print 'logan_message count', logan_message_count

if __name__ == '__main__':
    main()
