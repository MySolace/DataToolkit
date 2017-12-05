#!/usr/bin/python
# -*- coding: utf-8 -*-

from outputs.csvOutput import csvOutput
from inputs.Messages import Messages
from collections import Counter
import string
from sys import stdout

stopwords_file = open('lib/stopwords.txt', 'r')
stopwords = stopwords_file.read().splitlines()

stopphrases_file = open('lib/stopphrases.txt', 'r')
stopphrases = stopphrases_file.read().splitlines()

translator = string.maketrans(string.punctuation + '\n', ' '
                              * (len(string.punctuation) + 1))
wordCounts = []


def getWords(text, id):
    text = text.translate(translator).lower()
    c = Counter(word for word in text.split(' ') if word
                not in stopwords)
    wordCounts.append([id, list(c.most_common())])


# First get all messages

messages = Messages()
total = len(messages)

# Then, we're going to put all of the messages into their proper
# conversations.

print ('Organizing metadata...')
conversations = {}
for row in messages:

    # if row['message'] not in stopphrases and row['address'] != 'internal': # only texter messages

    if row['message'] not in stopphrases:  # all messages
        conversations.setdefault(int(row['conversation_id']),
                                 []).append(row['message'])

print ('Parsing...')

# Then we're going to put all the messages in a conversation into
# a single string.

i = 0
for cid in conversations:
    i += 1
    stdout.write('\r%d%%' % (i * 100 / len(conversations)))
    stdout.flush()
    conversations[cid] = ' '.join(conversations[cid])
    getWords(conversations[cid], cid)
stdout.write('\n')
stdout.flush()

# Generate the output file

print ('Writing CSV...')
output = csvOutput('frequency')
output.output(wordCounts)
