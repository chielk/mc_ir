import mechanize
import json
import re
import sys

try:
    from th_cache import cache
except:
    cache = {}

key = "OMgWqQArqygX3ZGDIBOr"
host = "http://thesaurus.altervista.org/service.php"
url = host+"?word=%s&language=en_US&output=json&key="+key+"&callback=process"

class Thesaurus:
    def __init__(self):
        """Initialise browser and load cache"""
        self.br = mechanize.Browser()
        self.cache = cache

    def get(self, word):
        if word in cache:
            return cache[word]
        else:
            try:
                cache[word] = []
                r = self.br.open(url % word)
                result = []
                for line in json.loads(r.read()[8:-1])['response']:
                    l = re.split('[\s\|]', re.sub(r" \(.*", "" , line['list']['synonyms']))
                    result.extend(l)
                cache[word] = result
                return result
            except:
                pass

    def __del__(self):
        """Save cache"""
        c = open('th_cache.py', 'w')
        c.write("cache = " + str(cache))
        c.close()


def main():
    t = Thesaurus()
    r = t.get('genetic')
    for line in r:
        print line


if __name__ == '__main__':
    main()
