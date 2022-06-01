import stanfordnlp

__nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,pos')
__special_prefixes = '@#'

def truecase(text):
    global __nlp, __special_prefixes

    for prefix in __special_prefixes:
        text = text.replace(prefix, f'{prefix} ')

    nlp = __nlp(text)
    
    tokens = [w.text.capitalize() if w.upos in ["PROPN","NNS"] else w.text for sent in nlp.sentences for w in sent.words]

    sentence = ''
    for token in tokens:
        seperator = " "
        if len(sentence) == 0:
            seperator = ''
        elif token[0] in ".?!';,":
            seperator = ''
        elif len(sentence) > 0 and sentence[-1] in __special_prefixes:
            seperator = ''
        
        if len(sentence) == 0:
            token = token.capitalize()

        sentence = sentence + seperator + token

    return sentence
