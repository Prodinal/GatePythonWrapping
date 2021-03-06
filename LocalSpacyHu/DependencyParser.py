import spacy
from spacy.tokens import Doc, Span, Token
from MagyarLanc3BaseComponent import MagyarLanc3BaseComponent


class HuDependencyParser(MagyarLanc3BaseComponent):
    def __init__(self,
                 nlp,
                 label='DependencyParser',
                 relative_path_to_magyarlanc='MagyarLanc3Wrapper/MagyarLanc3Wrapper.jar'):
        Token.set_extension('dep_type', default='')
        super().__init__(nlp, label, relative_path_to_magyarlanc)
        self.wrapper.initDepParser()

    def __call__(self, doc):
        words = [token.text for token in doc]
        lemmas = [token.lemma_ for token in doc]
        POSes = [token._.pos for token in doc]
        features = [token._.feature for token in doc]
        result = self.wrapper.depParseSentence(words, lemmas, POSes, features)
        for i, token in enumerate(doc):
            token._.dep_type = result[i][6]
            headTokenIdx = int(result[i][5])
            if headTokenIdx != -1:
                token.head = doc[headTokenIdx]

        return doc

if __name__ == '__main__':
    from LocalSpacyHu import HuTokeniser
    from LocalSpacyHu import HuPOSTagger

    debug_text = 'Autonóm autók hárítják a biztosítás terhét gyártók felé'
    nlp = spacy.blank('hu')
    nlp.tokenizer = HuTokeniser(nlp.vocab)
    POSTagger = HuPOSTagger(nlp)
    dependency_parser = HuDependencyParser(nlp)
    nlp.add_pipe(POSTagger)
    nlp.add_pipe(dependency_parser, last=True)

    doc = nlp(debug_text)
    for token in doc:
        print('Token is: ' + token.text)
        print('Head is: ' + token.head.text)
        print('DepType is: ' + token._.dep_type)
        print()
