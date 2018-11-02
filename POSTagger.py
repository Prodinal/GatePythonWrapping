import spacy
import os
from spacy.tokens import Doc, Span, Token


class HuPOSTagger():
    def __init__(self,
                 nlp,
                 label='POS',
                 relative_path_to_magyarlanc='POSTagger/MagyarLanc3Wrapper.jar'):
        self.nlp = nlp
        self.label = label
        self.relative_path_to_magyarlanc = relative_path_to_magyarlanc
        Token.set_extension('pos', default='')
        Token.set_extension('feature', default='')

        dirname = os.path.dirname(__file__)
        jar_path = os.path.join(dirname, self.relative_path_to_magyarlanc)
        os.environ['CLASSPATH'] = jar_path
        from jnius import autoclass
        WRAPPERCLASS = autoclass('test.MagyarLanc3Wrapper')
        self.wrapper = WRAPPERCLASS()
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
    from LocalSpacyHu import HuTokenizer

    nlp = spacy.blank('hu')
    nlp.tokenizer = HuTokenizer(nlp.vocab)
    nlp.add_pipe(HuPOSTagger(nlp), last=True)
    doc = nlp('A piros almákat szeretem.')

    for token in doc:
        print('Token is: ' + token.text)
        print('tag is: ' + token.tag_)
        print('pos is: ' + token._.pos)
        print('feature is: ' + token._.feature)
        print('lemma is: ' + token.lemma_ + '\n')
