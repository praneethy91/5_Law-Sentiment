

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

/** This class demonstrates building and using a Stanford CoreNLP pipeline. */
public class StanfordCoreNlpDemo {

  /** Usage: java -cp "*" StanfordCoreNlpDemo [inputFile [outputTextFile [outputXmlFile]]] */
  public static void main(String[] args) throws IOException {
    // Add in sentiment
    Properties props = new Properties();
    props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, dcoref, sentiment");

    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

    // Initialize an Annotation with some text to be annotated. The text is the argument to the constructor.
    //Annotation annotation = new Annotation(IOUtils.slurpFileNoExceptions(args[0]));
      String[] para_list = {
      "DRUMMOND, C. J. The schooner American was at Oswego in the fall of 1872, and took in a cargo of coal for Chicago, leaving Oswego on the tenth of November. A general bill of lading was given, and a high price charged for the transportation of the coal from Oswego to Chicago, being $2.75 per ton. The schooner met with adverse winds and did not arrive at Port Huron until November 29th. The weather, according to the testimony of the witnesses, was very inclement that fall, and the captain concluded that the safest course was to strip the vessel and lay up at Port Huron. The schooner accordingly remained there with her cargo during the winter, and the coal was not delivered in Chicago or received by the consignees until May 8, 1873, when the spring freight was paid by the consignees on the coal, being much less than that charged in the bill of lading. After the coal had been thus delivered by the schooner to the consignees, a libel was filed claiming the amount of freight stated in the bill of lading, the consignees having refused to pay any more than the spring price of freight. The case went to proof before the district court, where the libel was dismissed; but a cross-libel having been filed claiming that the captain of the American was negligent in wintering at Port Hur on, and that the vessel should have come on in the fall of 1872, the district court gave a decree on the cross-libel for damages against the libelants in consequence of the supposed negligence of the captain. From t hese decrees the libelants have appealed to this court, and the question is whether the decrees of the district court are right.",
              "Several cities, New York City in particular for this paper, have a 311 24-hour hot line and online service, which allows anyone, residents and tourists, to report a non-emergency problem. Reported 311 problems are passed along to government services, who address and solve the problem. The records of 311 calls are publicly open and updated daily.",
              "Analysis of 311 calls can clearly be of great use for a wide variety of purposes, ranging from a rich understanding of the status of a city to the effectiveness of the government services in addressing such calls. Ideally, the analysis can also support a prediction of future 311 calls, which would enable the assignment of service resources by the city government.",
              "We have been extensively analyzing 311 calls in NYC. In this paper, we profile the data set and highlight a few interesting facts. We provide statistics along complaint types, geolocation, and temporal patterns and show the diversity of the big 311 data along those dimensions. We then discuss the prediction problem of number of calls, where we experiment with different sets of semantic features. We show that the prediction error for different complaint types can significantly vary if some features are not considered."};

      ArrayList<Double> avgSentiment = new ArrayList<>();
      ArrayList<Integer> paraSnt = new ArrayList<>();


      long  start = System.nanoTime();
      for(String para : para_list) {
          Annotation annotation = new Annotation(para);
          pipeline.annotate(annotation);

          int para_sentiment = 0;
          int sentence_count = 0;
          List<CoreMap> sentences = annotation.get(CoreAnnotations.SentencesAnnotation.class);
          if (sentences != null && !sentences.isEmpty()) {
              for (CoreMap sentence : sentences) {
                  String sentiment = sentence.get(SentimentCoreAnnotations.SentimentClass.class);
                  sentence_count += 1;
                  int sentence_sentiment = 0;
                  if(sentiment.equals("Very Positive")){
                      sentence_sentiment = 2;
                  } else if(sentiment.equals("Positive")){
                      sentence_sentiment = 1;
                  } else if(sentiment.equals("Neutral")){
                      sentence_sentiment = 0;
                  } else if(sentiment.equals("Negative")){
                        sentence_sentiment = -1;
                  } else if(sentiment.equals("Very Negative")){
                        sentence_sentiment = -2;
                  }
                  para_sentiment += sentence_sentiment;
              }
          }
          if(sentence_count == 0){
              avgSentiment.add(0.0);
          } else {
              avgSentiment.add((double) (para_sentiment/sentence_count));
          }
          paraSnt.add(para_sentiment> 0? 1: para_sentiment<0 ? -1 : 0);
      }
      long end = System.nanoTime();
      System.out.println((end - start)/(1e9*1.0));
    }

}
