import spacy
from spacy.tokens import Doc, Span, Token
from MagyarLanc3BaseComponent import MagyarLanc3BaseComponent


class HuPOSTagger(MagyarLanc3BaseComponent):
    def __init__(self,
                 nlp,
                 label='POS',
                 relative_path_to_magyarlanc='MagyarLanc3Wrapper/MagyarLanc3Wrapper.jar'):
        Token.set_extension('pos', default='')
        Token.set_extension('feature', default='')
        super().__init__(nlp, label, relative_path_to_magyarlanc)

        self.wrapper.initPOSTagger()

    def __call__(self, doc):
        param = [token.text for token in doc]
        result = self.wrapper.tagSentence(param)
        for i, token in enumerate(doc):
            token.lemma_ = result[i][1]
            token.tag_ = result[i][2]
            token._.pos = result[i][3]
            token._.feature = result[i][4]
        return doc


if __name__ == '__main__':
    from LocalSpacyHu import HuTokeniser

    nlp = spacy.blank('hu')
    nlp.tokenizer = HuTokeniser(nlp.vocab)
    nlp.add_pipe(HuPOSTagger(nlp), last=True)
    doc = nlp('A piros almákat szeretem.')

    for token in doc:
        print('Token is: ' + token.text)
        print('tag is: ' + token.tag_)
        print('pos is: ' + token._.pos)
        print('feature is: ' + token._.feature)
        print('lemma is: ' + token.lemma_ + '\n')
