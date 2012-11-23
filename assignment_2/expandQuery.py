import xml.etree.ElementTree as ET
from thesaurus import Thesaurus

def expand(inputFileName, outputFileName, thesaurus):
    tree = ET.parse(inputFileName)
    treeRoot = tree.getroot()
    synProb = 0.5
    for tag in treeRoot.findall('query'): # for each query
        query = tag.find('text')
        query.text += " #wsyn( " # weighted synonyms
        for word in query.text.split(): # for each word in query
            for syn in thesaurus.get(word): # find synonyms
                query.text += " %.1f %s " % (synProb, syn)
            
        query.text += ")" # end weighted synonyms
    tree.write(outputFileName)

    
if __name__ == "__main__":
    ts = Thesaurus()
    expand("topics-indri-qe.trec", "testQE.trec", ts)