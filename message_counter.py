import fileinput
import sqlite3
import re
import operator

from os.path import expanduser

def access_database():
    conn = sqlite3.connect(expanduser("~/Library/Messages/chat.db"))
    print 'What is the other person\'s phone number? \nPlease put it in one these formats: \'(###)###-####\', or \'###-###-####\' or \'##########\'.'
    number = raw_input()
    number_string = '+1' + re.sub('[()-]\s', '', number) 
    c = conn.cursor()
    retrieve_row_id = '(select ROWID from handle where id=\'' + number_string + '\')'
    retrieve_chat_id = '(select chat_id from chat_handle_join where handle_id in' + retrieve_row_id + ')'
    retrieve_message_id = '(select message_id from chat_message_join where chat_id in' + retrieve_chat_id + ')'
    retrieve_text_is_from_me = 'select text, is_from_me from message where ROWID in' + retrieve_message_id
    c.execute(retrieve_text_is_from_me)
    parse_data(c)

def parse_data(c):
    running_dict = Counter()
    my_dict = Counter()
    their_dict = Counter()
    my_word_count = 0
    their_word_count = 0
    my_message_count = 0
    their_message_count = 0
    running_word_total = 0
    running_message_total = 0
    for line in c.fetchall():
        running_message_total += 1 
        string_token = line[0].split()
        sender = line[1]
        running_word_total += len(string_token)
        for word in string_token:
            word = re.sub('[^0-9A-Za-z]', '', word).lower()
            running_dict[word] += 1
            if sender == 0:
                their_dict[word] += 1
            else:
                my_dict[word] += 1
        if sender == 0:
            their_word_count += len(string_token)
            their_message_count += 1
        else:
            my_word_count += len(string_token)
            my_message_count += 1
    print 'In total we sent each other: ' + str(running_word_total) + ' words to each other.'
    print 'In total we sent each other: ' + str(running_message_total) + ' message to each other.'
    print 'You sent ' + str(their_word_count) + ' words'
    print 'You sent ' + str(their_message_count) + ' messages'
    print 'I sent ' + str(my_word_count) + ' words'
    print 'I sent ' + str(my_message_count) + ' messages'
    print 'On average you sent ' + str(float(their_word_count)/their_message_count) + ' words per messages'
    print 'On average I sent ' + str(float(my_word_count)/my_message_count) + ' words per messages'
    print 'Most Frequently Used words used by me: ' + str(my_dict.top_elements(0, 10, False))
    print 'Most Frequently Used words used by you: ' + str(their_dict.top_elements(0, 10, False))
    print 'Most Freqently Used words used by both you and me: ' + str(running_dict.top_elements(0, 10, False))
    print 'These might be more interesting: you 30-50 most common words: ' + str(their_dict.top_elements(30, 50, False))
    print 'Mine: 30 - 50: ' + str(my_dict.top_elements(30, 50, False))
    print 'Overall 30 - 50: ' + str(running_dict.top_elements(30, 50, False))
    

class Counter:

    def __init__(self):
        self.internal = {}

    def __getitem__(self, index):
        if not index in self.internal:
            self.internal[index] = 0
            return self.internal[index]
        else:
            return self.internal[index]

    def __setitem__(self, key, value):
        self.internal[key] = value

    def items(self):
        return self.internal.items()

    def top_elements(self, from_index, to_index, ascending=True):
#        print self.internal.items()
        sorted_x = sorted(self.internal.items(), key=operator.itemgetter(1))
        if not ascending:
            sorted_x.reverse()
        if sorted_x:
            return sorted_x[from_index:to_index]
        return []
            

def main():
    access_database()

if __name__ == '__main__':
    main()
