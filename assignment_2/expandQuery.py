import xml.etree.ElementTree as ET
from thesaurus import Thesaurus

def expand(inputFileName, outputFileName, theSaurus):
    tree = ET.parse(inputFileName)
    treeRoot = tree.getroot()
    for tag in treeRoot.findall('query'):
        query = tag.find('text')
        query.text += " #wsyn( 0.5 "
        for word in query.text.split():
            for synList in theSaurus.get(word):
                query.text += ' 0.5 '.join(synList)
        query.text += ")"
    tree.write(outputFileName)
        
if __name__ == "__main__":
    ts = Thesaurus()
    expand("topics-indri-qe.trec", "testQE.trec", ts)