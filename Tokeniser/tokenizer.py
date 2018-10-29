import sys
import os
from subprocess import Popen, PIPE, check_output, call
import xml.etree.ElementTree as ET
import spacy
from spacy.tokens import Doc


class HuTokenizer():
    def __init__(self, vocab, temp_file_name='temp.txt',
                 relative_path_to_quntoken='./quntoken'):
        self.vocab = vocab
        self.temp_file_name = temp_file_name
        self.relative_path_to_quntoken = relative_path_to_quntoken

    def __call__(self, input):
        dirname = os.path.dirname(__file__)
        quntoken_path = os.path.join(dirname, self.relative_path_to_quntoken)

        with open(self.temp_file_name, 'w+') as f:
            f.write(input)

        analysis = check_output([quntoken_path + ' ' + self.temp_file_name],
                                shell=True,
                                universal_newlines=True)
        # ET can only process if there is only one root tag
        analysis = '<root>' + analysis.strip() + '</root>'
        # Only process first sentence
        sent = ET.fromstring(analysis).find('s')
        words = [element.text for element in sent.findall('w')]

        os.remove(self.temp_file_name)
        return Doc(self.vocab, words=words)

if __name__ == '__main__':
    sentence = 'Szeretem a piros almákat mert nem savanyúak.'
    nlp = spacy.blank('hu')
    nlp.tokenizer = HuTokenizer(nlp.vocab)

    doc = nlp(sentence)
    for token in doc:
        print('Token is: ' + token.text)
