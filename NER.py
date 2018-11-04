import spacy
import sys
import os
from spacy.tokens import Doc, Span, Token
import numpy as np
import HunTag3.huntag as huntag


class TagResult():
    def __init__(self):
        self.tagged_sentences = []


class HuNER():
    def __init__(self,
                 nlp,
                 label='NER',
                 config_file_path='HunTag3/models/NER-szeged-hfst-model/ner.szeged.hfst.yaml',
                 model_path='HunTag3/models/NER-szeged-hfst-model/NER-szeged-hfst'):
        self.nlp = nlp
        self.label = label

        dirname = os.path.dirname(__file__)
        # initializing options based on huntag parser's default values
        optionsDict = dict()
        optionsDict['cfgFile'] = os.path.join(dirname, config_file_path)
        optionsDict['modelName'] = os.path.join(dirname, model_path)
        optionsDict['modelExt'] = '.model'
        optionsDict['transModelExt'] = '.transmodel'
        optionsDict['transModelOrder'] = 3
        optionsDict['featureNumbersExt'] = '.featureNumbers.gz'
        optionsDict['labelNumbersExt'] = '.labelNumbers.gz'
        optionsDict['lmw'] = 1
        optionsDict['cutoff'] = 1
        optionsDict['tagField'] = -1
        optionsDict['toCRFsuite'] = False
        optionsDict['modelFileName'] = '{0}{1}'.format(optionsDict['modelName'], optionsDict['modelExt'])
        optionsDict['transModelFileName'] = '{0}{1}'.format(optionsDict['modelName'], optionsDict['transModelExt'])
        optionsDict['featCounterFileName'] = '{0}{1}'.format(optionsDict['modelName'], optionsDict['featureNumbersExt'])
        optionsDict['labelCounterFileName'] = '{0}{1}'.format(optionsDict['modelName'], optionsDict['labelNumbersExt'])
        optionsDict['dataSizes'] = {'rows': 'Q', 'rowsNP': np.uint64,       # Really big...
                                    'cols': 'Q', 'colsNP': np.uint64,       # ...enough for indices
                                    'data': 'B', 'dataNP': np.uint8,        # Currently data = {0, 1}
                                    'labels': 'H', 'labelsNP': np.uint16,   # Currently labels > 256...
                                    'sentEnd': 'Q', 'sentEndNP': np.uint64  # Sentence Ends in rowIndex
                                    }
        optionsDict['outputStream'] = sys.stdout
        optionsDict['inputStream'] = sys.stdin

        optionsDict['task'] = 'tag'

        optionsDict['printWeights'] = False

        self.featureSet = huntag.getFeatureSetYAML(optionsDict['cfgFile'])
        self.optionsDict = optionsDict

    def __call__(self, doc):
        result = TagResult()
        inputArray = []
        for token in doc:
            line = token.text + '\t' + token.lemma_ + '\t' + token._.pos + '\t' + token._.feature
            inputArray.append(line)
        inputArray.append(os.linesep)     # necessary blank line to show end of sentence
        self.optionsDict['inputStream'] = inputArray
        huntag.mainTag(self.featureSet, self.optionsDict, result)

        NER_tags = [i[4] for i in result.tagged_sentences[0][0]]
        for i, ner_tag in enumerate(NER_tags):
            if ner_tag == 'O':      # this is a capital o letter, not a zero digit
                continue
            ner_tag_parts = ner_tag.split('-')
            label = doc.vocab.strings[ner_tag_parts[1]]
            if ner_tag_parts[0] == '1':
                doc.ents = (list(doc.ents) + [Span(doc, i, i+1, label=label)])
            elif ner_tag_parts[0] == 'B':
                self.ner_begin_idx = i
            elif ner_tag_parts[0] == 'E':
                if self.ner_begin_idx is None:
                    raise Exception('Found end of ner, when looking for beginning')
                else:
                    span = Span(doc, self.ner_begin_idx, i+1, label=label)
                    span.merge()
                    doc.ents = (list(doc.ents) + [span])
                    self.ner_begin_idx = None

        return doc


if __name__ == '__main__':
    from LocalSpacyHu import HuTokenizer
    from LocalSpacyHu import HuPOSTagger

    # debug_text = u'A kék New York elrepült a sima Berlin mellett'
    debug_text = 'Peti Budapesten él Dorinával és nagyon szeret a jószagú Trófeában ebédelni.'
    nlp = spacy.blank('en')
    nlp.tokenizer = HuTokenizer(nlp.vocab)

    POSTagger = HuPOSTagger(nlp)
    ner = HuNER(nlp)

    nlp.add_pipe(POSTagger)
    nlp.add_pipe(ner)

    doc = nlp(debug_text)
    for span in doc.ents:
        print(span.text + " " + span.label_)
