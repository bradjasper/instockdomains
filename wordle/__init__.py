import re
import logging
import pprint

log = logging.getLogger('inst.wordle')

def clean(phrase):
    """Clean a string by removing all non-alpha or space characters"""
    phrase = strip_tags(phrase)
    return re.sub('[^a-zA-Z ,&\-]', '', phrase).strip()

def strip_tags(data):
    """Remove HTML tags"""
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    

class TitleFolder(object):
    """The TitleFolder takes a list of datas and generates a list of synonyms
    based on context. Try to keep this as magic free as possible."""

    def fold_data(self, parts, query):
        """Take parts of data and deduce synonym relationships from them using a
        query. We call this folding."""

        def _inc(bank, key):
            value = bank.get(key, 0)
            value += 1
            return value
            

        query_parts = query.split()

        max = len(query_parts)

        bank = {}
        for i, query in enumerate(query_parts):
            for title in parts:
                for part in title:
                    words = part.split()
                    for x, word in enumerate(words):

                        # ex. mac == mac
                        try:
                            if word == query:
                                bank[query_parts[i+1]] = _inc(bank, words[x+1])
                        except IndexError:
                            pass

        pprint.pprint(bank)
                            
                       
    def check_data(self, data):
        """Check if data is valid. Used for filter functions"""

        data = re.sub('(\-|\|)', '', data)
        data = data.strip()
        return len(data)

    def fix_data(self, data):
        """Convert everything to lowercase and normalize commas. Also split on
        dashes and | signs"""

        data = data.lower()
        data = re.sub('(and|\&amp\;|\/)', ',', data)
        parts = re.split('\s(\-|\|)\s', data)
        parts = [clean(part) for part in parts]
        data = filter(self.check_data, parts)

        return data


    def get_synonyms(self, data, query):
        """Extract the synonyms from a piece of data, referencing a query"""

        log.debug("Getting informatino from synonyms (%s) - %s", query, data)

        parts = [self.fix_data(part) for part in data]

        log.debug("Got parts for synonyms (%s) - %s", query, parts)

        synonyms = self.fold_data(parts, query)

        log.debug("Got synonyms back for (%s) - %s", query, synonyms)
        for syn in synonyms:
            print syn

