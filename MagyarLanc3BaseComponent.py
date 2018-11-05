import os


class MagyarLanc3BaseComponent():
    def __init__(self,
                 nlp,
                 label,
                 relative_path_to_magyarlanc='MagyarLanc3Wrapper/MagyarLanc3Wrapper.jar'):
        self.nlp = nlp
        self.label = label
        self.relative_path_to_magyarlanc = relative_path_to_magyarlanc

        dirname = os.path.dirname(__file__)
        jar_path = os.path.join(dirname, self.relative_path_to_magyarlanc)
        os.environ['CLASSPATH'] = jar_path
        from jnius import autoclass
        WRAPPERCLASS = autoclass('wrapper.MagyarLanc3Wrapper')

        self.wrapper = WRAPPERCLASS()
