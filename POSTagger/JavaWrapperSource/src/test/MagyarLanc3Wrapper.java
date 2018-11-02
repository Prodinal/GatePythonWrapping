package test;

import java.util.Arrays;
import java.util.List;

import hu.ppke.itk.nlpg.docmodel.ISentence;
import hu.ppke.itk.nlpg.purepos.ITagger;
import hu.ppke.itk.nlpg.purepos.MorphTagger;
import hu.ppke.itk.nlpg.purepos.cli.configuration.Configuration;
import hu.ppke.itk.nlpg.purepos.model.internal.CompiledModel;
import hu.ppke.itk.nlpg.purepos.model.internal.RawModel;
import hu.ppke.itk.nlpg.purepos.morphology.NullAnalyzer;
//import hu.u_szeged.pos.purepos.MyPurePos;
import hu.u_szeged2.config.Config;
import hu.u_szeged2.dep.parser.MyMateParser;
import hu.u_szeged2.pos.purepos.MySerilalizer;

public class MagyarLanc3Wrapper {
	private ITagger iTagger;
	private static final double BEAM_LOG_THETA = Math.log(1000);
	private double SUFFIX_LOG_THETA = Math.log(10);
	private int MAX_GUESSED = 5;
	private boolean USE_BEAM_SEARCH = false;
	
	private MyMateParser depParser;
	
	/*public String getHelloMessage() {
		return "Hello world!";
	}*/
	
	/*public void prettyPrint2DArray(String[][] array) {
		for(int i = 0; i < array.length; i++) {
			for(int j = 0; j < array[i].length; j++) {
				System.out.println("Coords are: " + i + ", " + j + " value is: " + array[i][j]);
			}
		}
	}*/
	
	/*public String testPurePos() {
		String[] sentence = new String[1];
		sentence[0] = "alma";
		System.out.println("Creating purePos instance");
		MyPurePos purePos = MyPurePos.getInstance();
		System.out.println("Done");
		System.out.println("Calling morphParseSentence");
		String[][] result = purePos.morphParseSentence(sentence);
		System.out.println("Done");
		prettyPrint2DArray(result);
		
		System.out.println("Calling morphParseSentence a second time");
		String[] sentence2 = "Az kis körte elrepült a piros alma mellett.".split("\\s");
		result = purePos.morphParseSentence(sentence2);
		System.out.println("Done");
		prettyPrint2DArray(result);
		return "success";
	}*/
	
	/**Does POS tagging and lemmatising for tokens.
	 * 
	 * @param sentence String[] that contains the tokens of the sentence
	 * @return String[][] an array for each token, [0] is the token, [1] is the lemma, [2] is the POS and [3] is the features
	 */
	/*public String[][] morphParseSentence(String[] sentence){
		return MyPurePos.getInstance().morphParseSentence(sentence);
	}*/
	
	public void initPOSTagger() {
		if (iTagger == null) {
			
			RawModel rawmodel = null;
		    try {
		        rawmodel = MySerilalizer.readModel(Config.getInstance().getPurePosModel());
		    } catch (Exception e) {
		        e.printStackTrace();
		    }

		    CompiledModel<String, Integer> model = rawmodel.compile(new Configuration());

			iTagger = new MorphTagger(model, new NullAnalyzer(), BEAM_LOG_THETA, SUFFIX_LOG_THETA, MAX_GUESSED, USE_BEAM_SEARCH);
    	}
	}
	
	public String[][] tagSentence(String[] input) {
		if(iTagger == null) {
			initPOSTagger();
		}
		ISentence tagged = iTagger.tagSentence(Arrays.asList(input));
		String[][] result = new String[input.length][5];
		
		for (int i = 0; i < tagged.size(); ++i) {
            String stem = tagged.get(i).getStem(); // lemma
            String tag = tagged.get(i).getTag(); // hfstcode analysis tag

            String hfstlemmaana = stem + tag; 
            String form = input[i];

            String pos = DepTool.getPos( hfstlemmaana, form ); 
            String features = DepTool.getFeatures( hfstlemmaana, form ); 
            
            result[i][0] = input[i];
            result[i][1] = stem;
            result[i][2] = tag;
            result[i][3] = pos;
            result[i][4] = features;
        }
		return result;
	}
	
	public void initDepParser() {
		if(depParser == null) {
			depParser = MyMateParser.getInstance();
		}
	}
	
	public String[][] depParseSentence(String[] words, String[] lemma, String[] pos, String[] feat){        
        if(depParser == null) {
        	initDepParser();
        }
        
		String[][] result = depParser.parseSentence(words,lemma,pos,feat);
		//returned result contains one array for each word provided, result[i][0-4] contains the passed parameters
		//result[i][5] is the index of the head token (indexed from 1, not 0)
		//result[i][6] is the dep type of the token
		for(int i = 0; i < result.length; i++) {
			result[i][5] = "" + (Integer.decode(result[i][5]) - 1);	//head token id is counted from 1 instead of 0
		}
		
		return result;
	}
	
	public static void main(String[] args) {
		MagyarLanc3Wrapper main = new MagyarLanc3Wrapper();
		//System.out.println(main.testPurePos());
	}
}