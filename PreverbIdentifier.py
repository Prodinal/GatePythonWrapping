import spacy
from spacy.tokens import Token


class HuPreverbIdentifier():
    def __init__(self,
                 nlp,
                 label='PreverbIdentifier'):
        self.nlp = nlp
        self.label = label
        Token.set_extension('preverb', default='')
        Token.set_extension('lemmaWithPreverb', default='')

    def __call__(self, doc):
        for token in doc:
            if token._.dep_type == 'PREVERB':
                token.head._.preverb = token.lemma_
                token.head._.lemmaWithPreverb = token.lemma_ + token.head.lemma_
        return doc

if __name__ == '__main__':
    from LocalSpacyHu import HuTokenizer
    from LocalSpacyHu import HuPOSTagger
    from LocalSpacyHu import HuDependencyParser

    debug_text = 'El is áztam amikor került elő a repcsi'
    nlp = spacy.blank('hu')
    nlp.tokenizer = HuTokenizer(nlp.vocab)

    POSTagger = HuPOSTagger(nlp)
    nlp.add_pipe(POSTagger)

    DepParser = HuDependencyParser(nlp)
    nlp.add_pipe(DepParser)

    preverb_identifier = HuPreverbIdentifier(nlp)
    nlp.add_pipe(preverb_identifier)

    doc = nlp(debug_text)
    for token in doc:
        print('Token is: ' + token.text)
        if token._.preverb != '':
            print('Preverb is: ' + token._.preverb)
        if token._.lemmaWithPreverb != '':
            print('lemmaWithPreverb is: ' + token._.lemmaWithPreverb)
        print()
