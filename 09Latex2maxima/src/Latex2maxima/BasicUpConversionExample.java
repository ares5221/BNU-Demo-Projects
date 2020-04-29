package Latex2maxima;

import uk.ac.ed.ph.snuggletex.SnuggleEngine;
import uk.ac.ed.ph.snuggletex.SnuggleInput;
import uk.ac.ed.ph.snuggletex.SnuggleSession;
import uk.ac.ed.ph.snuggletex.XMLStringOutputOptions;
import uk.ac.ed.ph.snuggletex.upconversion.UpConvertingPostProcessor;
import uk.ac.ed.ph.snuggletex.upconversion.internal.UpConversionPackageDefinitions;

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Basic example of up-converting some simple LaTeX input to Content MathML and Maxima forms.
 * 
 * <h2>Running Notes</h2>
 * 
 * You will need the following in your ClassPath:
 * 
 * <ul>
 *   <li>snuggletex-core.jar</li>
 *   <li>snuggletex-upconversion.jar</li>
 *   <li>saxon9.jar, saxon9-dom.jar</li> (These are required as the conversion process uses XSLT 2.0)
 * </ul>
 * 
 * @since 1.1.0
 *
 * @author  David McKain
 * @version $Revision: 525 $
 */
public final class BasicUpConversionExample {
    
    public static void main(String[] args) throws IOException {
        /* We will up-convert this LaTeX input */
        String input = "$$=\\sqrt{{a}^{3}+{a}^{2}}=-a\\sqrt {a+1} $$";
        BasicUpConversionExample ex = new BasicUpConversionExample();
        System.out.println(ex.l2m(input));
        System.out.println("\\s");
        System.out.println("\\\\s");

    }
   
    public static String l2m(String input) throws IOException{
    	  /* Set up SnuggleEngine, remembering to register package providing up-conversion support */
    	/*识别出从latex中识别出maxima相应的代码。
    	 * 首先处理将latex格式的东西进行处理，因为在java里面有转义字符'\\'为‘\’
    	 */
    	input.replaceAll("\\b", "\\\\b");
    	input.replaceAll("\\t", "\\\\t");
    	input.replaceAll("\\n", "\\\\n");
    	input.replaceAll("\\f", "\\\\f");
    	input.replaceAll("\\r", "\\\\r");
        SnuggleEngine engine = new SnuggleEngine();
        engine.addPackage(UpConversionPackageDefinitions.getPackage());
        
        /* Create session in usual way */
        SnuggleSession session = engine.createSession();
        
        /* Parse input. I won't bother checking it here */
        session.parseInput(new SnuggleInput(input));

        /* Create an UpConvertingPostProcesor that hooks into the DOM generation
         * process to do all of the work. We'll use its (sensible) default behaviour
         * here; options can be passed to this constructor to tweak things.
         */
        UpConvertingPostProcessor upConverter = new UpConvertingPostProcessor();
        
        /* We're going to create a simple XML String output, which we configure
         * as follow. Note how we hook the up-conversion into this options Object.
         */
        XMLStringOutputOptions xmlStringOutputOptions = new XMLStringOutputOptions();
        xmlStringOutputOptions.addDOMPostProcessors(upConverter);
        xmlStringOutputOptions.setIndenting(true);
        xmlStringOutputOptions.setUsingNamedEntities(true);
        
        /* Build up the resulting XML */
        String result = session.buildXMLString(xmlStringOutputOptions);
        //System.out.println("Up-Conversion process generated: " + result);
        /*
         * 使用正则表达式从识别出来的结果中提取出相应的maxima结果。
         * 去掉正则后可以看到mathml的识别结果。
         */
    	String regex = "\">(.*?)</annotation>";
		Pattern pattern = Pattern.compile(regex);
		Matcher matcher = pattern.matcher(result);
		while (matcher.find()) {
//			System.out.println(matcher.group(1));
			result=matcher.group(1);
		}
		return result;
    	
    }
}