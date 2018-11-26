import spacy
from spacy.tokens import Doc, Span, Token
from MagyarLanc3BaseComponent import MagyarLanc3BaseComponent


class HuConstituencyParser(MagyarLanc3BaseComponent):
    def __init__(self,
                 nlp,
                 label='ConstituencyParser',
                 relative_path_to_magyarlanc='MagyarLanc3Wrapper/MagyarLanc3Wrapper.jar'):
        Token.set_extension('cons', default='')
        super().__init__(nlp, label, relative_path_to_magyarlanc)
        self.wrapper.initConsParser()

    def __call__(self, doc):
        words = [token.text for token in doc]
        lemmas = [token.lemma_ for token in doc]
        POSes = [token._.pos for token in doc]
        features = [token._.feature for token in doc]
        result = self.wrapper.consParseSentence(words, lemmas, POSes, features)
        for i, token in enumerate(doc):
            token._.cons = result[i][4]

        return doc

if __name__ == '__main__':
    from LocalSpacyHu import HuTokeniser
    from LocalSpacyHu import HuPOSTagger

    debug_text = 'A kék alma nagyon gyorsan elrepült a sima köcsög mellett'
    nlp = spacy.blank('hu')
    nlp.tokenizer = HuTokeniser(nlp.vocab)
    POSTagger = HuPOSTagger(nlp)
    constituency_parser = HuConstituencyParser(nlp)
    nlp.add_pipe(POSTagger)
    nlp.add_pipe(constituency_parser)

    doc = nlp(debug_text)
    result_cons_tree = []
    for token in doc:
        print('Token is: ' + token.text)
        print('Cons is: ' + token._.cons)
        result_cons_tree.append(token._.cons)
    print("".join(result_cons_tree))
