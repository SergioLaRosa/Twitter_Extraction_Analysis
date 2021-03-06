import csv
import uuid
import sys
try:
    import fuzzywuzzy
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
except ImportError:
    print("[ERROR] Unable to import Fuzzywuzzy module: can't run!")
    sys.exit()


class PostProcessor:

    def __init__(self):
        self._status = ""
        self._map = ""
        self._fp = ""
        self._reader = ""
        self._text = ""
        self._extr = ""

    def evaluate_text(self, fname, mhash, sentiment):
        self._map = dict()
        self._fp = open(fname, 'r')
        self._reader = csv.reader(self._fp)

        for self._row in self._reader:
            try:
                if self._row[1] == sentiment:
                    self._text = self._row[0].replace("\\n", "")
                    self._text = self._text.split(" ")
                    self._extr = [
                        self._word for self._word in self._text if self._word.startswith('#')]

                    for self._part in self._extr:
                        if fuzz.partial_ratio(mhash, self._part) > 80:
                            self._extr.remove(self._part)
                        else:
                            if self._part != "#'":
                                self._map[uuid.uuid4().hex[:8]] = self._extr

            except IndexError:
                pass

        return self._map
