import xml.etree.ElementTree as ET
import subprocess
from thesaurus import Thesaurus

def main():
    ts = Thesaurus()
    originalQueryFile = "topics-indri-qe.trec"
    trecRelFile = "document-qrels.txt"
    for x in xrange(6):
        synWeight = x/10.0
        print "synWeight: %.1f" %synWeight
        # expand queries
        print "expand queries"
        outputQueryFile = "testQE%d.trec" %x
        expand(originalQueryFile, outputQueryFile, ts, synWeight)
        # run queries
        print "run queries"
        queryOutputFile = "output_synW%d.txt" %x
        queryProcess = "IndriRunQuery %s > %s" %(outputQueryFile, queryOutputFile)
        subprocess.call(queryProcess, shell=True)
        # evaluate result
        print "evaluate result"
        resultFile = "result_synW%d.txt" %x
        trecEvalProcess = "trec_eval %s %s > %s" %(trecRelFile, queryOutputFile, resultFile)
        subprocess.call(trecEvalProcess, shell=True)

def expand(inputFileName, outputFileName, thesaurus, synWeight):
    tree = ET.parse(inputFileName)
    treeRoot = tree.getroot()
    for tag in treeRoot.findall('query'): # for each query
        qList = tag.find('text').text.split() # query list
        query = tag.find('text')
        query.text = "#weights("
        for q in qList:
            query.text += " 1.0 %s" %q
        for word in qList: # for each word in query
            for syn in thesaurus.get(word): # find synonyms
                query.text += " %.1f %s " % (synWeight, syn)
        query.text += ")" # end weighted synonyms
    tree.write(outputFileName)


if __name__ == "__main__":
    #ts = Thesaurus()
    #expand("topics-indri-qe.trec", "testWeights.txt", ts, 0.1)
    main()
