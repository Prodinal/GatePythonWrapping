import hfst
import os
import re
import spacy
from spacy.tokens import Doc, Span, Token
from MagyarLanc3BaseComponent import MagyarLanc3BaseComponent


class HuLemmatiserMorphAnalyser(MagyarLanc3BaseComponent):
    def __init__(self,
                 nlp,
                 label='Morph',
                 relative_path_to_magyarlanc='MagyarLanc3Wrapper/MagyarLanc3Wrapper.jar',
                 path_to_transducer='LemmatiserMorphAnalyser/hu.hfstol'):
        super().__init__(nlp, label, relative_path_to_magyarlanc)
        self.path_to_transducer = path_to_transducer
        Token.set_extension('features', default=None)
        Token.set_extension('lemma', default=None)
        dirname = os.path.dirname(__file__)
        transducer_path = os.path.join(dirname, self.path_to_transducer)

        self.wrapper.initStemmer()

        input_stream = hfst.HfstInputStream(transducer_path)
        throwaway = input_stream.read()     # file contains 2 transducers, the first of which is useless
        self.analyser = input_stream.read()
        input_stream.close()

    def __call__(self, doc):
        for token in doc:
            anas = self.analyser.lookup(token.text)
            for ana in anas:    # each ana is a 2 long tuple, where the first item is the analysis, the second is the confidence
                cleaned = self.clean_ana(ana[0])
                analysis = self.wrapper.processStem(cleaned)

                if token._.lemma is None:
                    token._.lemma = list()
                if token._.features is None:
                    token._.features = list()

                # analysis[0] is the sent string, analysis[1] is lemma, analysis[2] is the morph analysis
                token._.lemma.append(analysis[1])
                token._.features.append(analysis[2])
        return doc

    def clean_ana(self, ana):
        return re.sub('@\S+?@', '', ana)


if __name__ == '__main__':
    from LocalSpacyHu import HuTokeniser

    debug_text = 'Elmentem játszani a kecskékkel'
    nlp = spacy.blank('hu')
    nlp.tokenizer = HuTokeniser(nlp.vocab)
    morph_analyser = HuLemmatiserMorphAnalyser(nlp)
    nlp.add_pipe(morph_analyser)

    doc = nlp(debug_text)
    for token in doc:
        print('Token is: ' + token.text)
        print('Features are: ')
        print(token._.features)
        print('Lemma is: ')
        print(token._.lemma)
