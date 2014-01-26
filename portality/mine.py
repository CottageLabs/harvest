from topia.termextract import extract
import re

# create a term extractor and keep it in memory - they have quite a start-up
# overhead so don't want to create one each time
extractor = extract.TermExtractor()

def text_extract(text, weight=1):
    """
    Extract terms from the text, and provide each one with a score equivalent to:
    
    number of incidences * number of words in term * weight
    """
    terms = extractor(text)
    result = {}
    for t, o, l in terms:
        result[t.lower()] = o * l * weight
    return result

def multi_extract(**kwargs):
    """
    Extract keywords from all passed text strings with provided weights.  Returns a dictionary
    with each field name as a key, and the term extraction results as from text_extract as the
    value.
    
    expects kwargs as follows:
    xxxx_text = text field
    xxxx_weight = weight of that text
    
    e.g.
    title_text = "This is my title"
    title_weight = 10
    abstract_text = "This very interesting paper is all about stuff..."
    abstract_weight = 5
    """
    arguments = {}
    for arg, value in kwargs.iteritems():
        name = "_".join(arg.split("_")[:-1])
        if name not in arguments:
            arguments[name] = ["", 1]
        if arg.endswith("_text"):
            arguments[name][0] = value
        if arg.endswith("_weight"):
            arguments[name][1] = value
    
    results = {}
    for name, arr in arguments.iteritems():
        results[name] = text_extract(arr[0], weight=arr[1])
        
    return results

def full_extract(combine_terms=True, group_terms=True, **kwargs):
    """
    Extract keywords from all passed text strings with provided weights.
    
    If combine is true (default) and group is true (default), then return a dictionary of terms,
    keyed by their score.
    
    If combine is true (default) and group is not true, then return a dictionary of terms, keyed
    by term, with their score as a value
    
    If combine is false, then return same result as multi_extract
    
    expects kwargs as follows:
    xxxx_text = text field
    xxxx_weight = weight of that text
    
    e.g.
    title_text = "This is my title"
    title_weight = 10
    abstract_text = "This very interesting paper is all about stuff..."
    abstract_weight = 5
    """
    results = multi_extract(**kwargs)
    if combine_terms:
        combination = combine(results.values())
        if group_terms:
            grouped = group(combination)
            return grouped
        else:
            return combination
    else:
        return results
    
def combine(result_sets=[]):
    """
    take the set of results as extracted by text_extract, and turn them into a single
    result set, with aggregate (via addition) scores
    """
    stitched = {}
    for result in result_sets:
        for k, v in result.iteritems():
            if k in stitched:
                stitched[k] += v
            else:
                stitched[k] = v
    return stitched
    
def group(result):
    """
    Take a result set and group the terms into bins of equal score
    """
    out = {}
    for k, v in result.iteritems():
        if v in out:
            out[v].append(k)
        else:
            out[v] = [k]
    return out

def html_text(html):
    # first thing is to strip the style and script tags, with all their content
    processed = re.sub("<style[ ]{0,1}.*?>.*?</style>", "", html, flags=re.DOTALL)
    processed = re.sub("<script[ ]{0,1}.*?>.*?</script>", "", processed, flags=re.DOTALL)
    
    # now get rid of all of the other html tags, leaving their content behind
    processed = re.sub("<[/]{0,1}[!a-zA-Z]+[ ]{0,1}.*?>", "", processed, flags=re.DOTALL)
    
    # finally tidy up by getting rid of all the newlines and tabs that will be all
    # over the place
    processed = processed.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    
    return processed


from StringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import LTTextItem, TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

def pdf_text(pdfstr):
    parser = PDFParser(StringIO(resp.content))












    
    
    
    
