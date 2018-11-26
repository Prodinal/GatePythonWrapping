import os
import sys


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
        if 'jnius' not in sys.modules:  # importing jnius starts the java vm, config cannot be changed afterwards
            import jnius_config
            jnius_config.add_options('-Xmx4G')  # constituency parsing model needs a lot of memory
        from jnius import autoclass
        WRAPPERCLASS = autoclass('wrapper.MagyarLanc3Wrapper')

        self.wrapper = WRAPPERCLASS()
