import os
import sys
import numpy as np

import HunTag3.huntag as huntag


class TagResult():
    def __init__(self):
        self.tagged_sentences = []


class HunTag3BaseComponent():
    def __init__(self,
                 nlp,
                 label='NER',
                 config_file_path='HunTag3/models/NER-szeged-hfst-model/ner.szeged.hfst.yaml',
                 model_path='HunTag3/models/NER-szeged-hfst-model/NER-szeged-hfst',
                 HunTag3Task='tag'):

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

        optionsDict['task'] = HunTag3Task

        optionsDict['printWeights'] = False

        self.featureSet = huntag.getFeatureSetYAML(optionsDict['cfgFile'])
        self.optionsDict = optionsDict
