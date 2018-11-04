import spacy
import os
from spacy.tokens import Doc, Span, Token

import HunTag3.huntag as huntag
from HunTag3BaseComponent import HunTag3BaseComponent, TagResult


class HuNPChunker(HunTag3BaseComponent):
    def __init__(self,
                 nlp,
                 label='NPChunker',
                 config_file_path='HunTag3/models/maxNP-szeged-hfst-model/maxnp.szeged.hfst.yaml',
                 model_path='HunTag3/models/maxNP-szeged-hfst-model/maxNP-szeged-hfst',
                 HunTag3Task='tag'):
        super().__init__(nlp, label, config_file_path, model_path, HunTag3Task)
        Doc.set_extension('noun_chunks', default=[])

    def __call__(self, doc):
        result = TagResult()
        inputArray = []
        for token in doc:
            line = token.text + '\t' + token.lemma_ + '\t' + token._.pos + '\t' + token._.feature
            inputArray.append(line)
        inputArray.append(os.linesep)     # necessary blank line to show end of sentence
        self.optionsDict['inputStream'] = inputArray
        huntag.mainTag(self.featureSet, self.optionsDict, result)

        NP_tags = [i[4] for i in result.tagged_sentences[0][0]]
        for i, np_tag in enumerate(NP_tags):
            if np_tag == 'O':      # this is a capital o letter, not a zero digit
                continue
            np_tag_parts = np_tag.split('-')
            if np_tag_parts[0] == '1':
                doc._.noun_chunks = (list(doc._.noun_chunks) + [Span(doc, i, i+1)])
            elif np_tag_parts[0] == 'B':
                self.ner_begin_idx = i
            elif np_tag_parts[0] == 'E':
                if self.ner_begin_idx is None:
                    raise Exception('Found end of ner, when looking for beginning')
                else:
                    span = Span(doc, self.ner_begin_idx, i+1)
                    doc._.noun_chunks = (list(doc._.noun_chunks) + [span])
                    self.ner_begin_idx = None
        return doc

if __name__ == '__main__':
    from LocalSpacyHu import HuTokenizer
    from LocalSpacyHu import HuPOSTagger

    # debug_text = u'A kék New York elrepült a sima Berlin mellett'
    debug_text = 'A kék alma nagyon gyorsan elrepült a kicsi kutya mellett.'
    nlp = spacy.blank('en')
    nlp.tokenizer = HuTokenizer(nlp.vocab)

    POSTagger = HuPOSTagger(nlp)
    NPChunker = HuNPChunker(nlp)

    nlp.add_pipe(POSTagger)
    nlp.add_pipe(NPChunker)

    doc = nlp(debug_text)
    for span in doc._.noun_chunks:
        print(span.text)
