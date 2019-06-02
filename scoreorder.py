#!/usr/bin/env python3

import os
import glob
from pprint import pprint
import re
import unittest

"""
OrchFolder = os.environ['KMVAR_OrchFold'] + "/*.pdf"
FileList = glob.glob(OrchFolder)
ScoreList = os.environ['KMVAR_ScoreOrder']
ScoreOrder = ScoreList.split(", ")
"""

SearchTerms = {
    "Score": "Score",
    "Vocals": "Vo?ca?ls.*",
    "LeadSheet": "(Lead\s?Sheet)|(\s|\_|\-)LS.*",
    "ChoirSheet": "Choir Sheet.*",
    "Rhythm Chart": "Rhy(thm)?(Chart)?",
    "Piano(and/or Vocal)": "(Vocal)?P(ia)?no\.?(Vocal)?.*",
    "Synth": "Synth(esizer)?",
    "Acoustic Guitar": "Ac(oustic)?\.?\s?G(ui)?ta?r",
    "EletricGuitar": "El(ectric)?\.?\s?G(ui)?ta?r",
    "BaseGuitar": "B(ass)?\.?\s?G(ui)?ta?r",
    "Piccolo": "(picc(olo)?)|pc",
    "Flute": "Fl(?!g)u?(?!g)t?e?.*(picc)?",
    "Oboe": "Ob(oe)?",
    "Bass": "ba?ss?(oo)?n",
    "EnglishHorn": "English H(or)?n",
    "Clarinet": "([^b]...)(\d|\s|\_|\()cl(ar)?(inet)?",
    "BaseClarinet": "b(ass)?(\d|\s|\_)?cl(ar)?(inet)?",
    "FrenchHorn": "(Fr?\.?(ench)?\s?)(Ho?r?n)|([^\w]|\d|\_)(Ho?r?n)",
    "Trumpet": "tr?u?m?pe?t",
    "Trombone": "([^b]....)T(rom)?bo?ne?",
    "BaseTrombone": "b(ass)?.?T(rom)?bo?ne?",
    "Baritone": "Baritone.?\(?BC\)?",
    "Euphonium": "Euph(onium)?",
    "Tuba": "Tu?ba",
    "Chimes": "Chimes",
    "Xylophone": "Xyl(ophone?)?.?(Bells)?",
    "Timpanie": "Timp(ani)?",
    "Mallets": "Mallets",
    "Percussion": "Perc(ussion)?.*",
    "Drums": "Drum?\s?s?(et)?",
    "Harp": "H(ar)?p",
    "Celesta": "Cel(est(e|a))?",
    "ChordChart": "Cho?rds?\s?(Cha?r?t)?",
    "Violine": "v(io)?li?n",
    "Viola": "v(io)?la",
    "Violine": "vcl?|(violin)?cello",
    "CelloBass": "CelloBass",
    "Bass": "((str?(ing)?|d(ou)?ble?)\s?)?(bass)",
    "Clarinet": "Clarinet.?(doubles|sub)",
    "Basoon": "ba?ss?(oo)?n.*(doubles|sub).*",
    "SopranoSax": "Sop(rano)?\s?Sax(ophone)?.*(sub)?",
    "AltoSax": "A(lto\s?Sa)?x(ophone)?.*(sub)?",
    "TenorSax": "T(enor\s?Sa)?x(ophone)?.*(sub)?",
    "BaritonSax": "B(ari(tone)?\s?Sa)?x(ophone)?.*(sub)?",
    "FlugelHorn": "Flu?g(el)?\s?Ho?rn",
    "Baritone": "bari(tone)?\s?t(reble)?\s?c(lef)?.*(sub)?",
    "Violin": "v(io)?li?n.*simplified.*",
    "Viola": "v(io)?la.*simplified.*",
    "Keyboard": "(((keyboard)?\s?Str(ing)?\s?Red(uction)?)|KSR)",
    "Synth Strings": "Synth\s?Str(ings)?",
}

def RankFn(ScoreOrder):
    """RankFn returns the Rank function with a specific SortOrder"""
    def Rank(FilePath):
        for idx, ScoreEntry in enumerate(ScoreOrder, start=1):
            # Look up the SearchTerm regex in the SearchTerms dictionary.
            SearchTerm = SearchTerms[ScoreEntry]
            regex = f"(\(|\s|\_|\-)?{SearchTerm}(\)|\.|$|(\sin.*)|(\ssolo)|(\s.*II?)|(\s?(\d.*\d?)))"
            if re.search(regex, FilePath, re.I):
                return idx
        return False
    return Rank

"""
FilterStage = filter(RankFn(SortOrder), FileList)
SortFirst = sorted(FilterStage, key=str.lower)
SortedStage = sorted(SortFirst, key=Rank)

for idx, FilePath in enumerate(SortedStage, start=0):
    BaseName = os.path.basename(FilePath)
    m = re.search('^(\d\d\s)(.*)', BaseName)
    if m:
        BaseName = m.group(2)
    FileDirectory = os.path.dirname(FilePath)
    NewName = "{:02d} {}".format(idx, BaseName)
    NewPath = os.path.join(FileDirectory, NewName)
    pprint (NewName)
"""

############
# Unit Tests
############

class ScoreOrderTestCase(unittest.TestCase):
    """ A collection of unit tests. unittest.main() will
    run every function that begins with 'test_' """

    def test_example(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_regex(self):
        tests = [
            ("Score", "Score", True),
            ("Score", "Scores", False),
        ]
        for x, (Term, input, expected) in enumerate(tests):
            Rank = RankFn([Term])
            actual = Rank(input)
            # The third argument is a message to help us know what went wrong.
            self.assertEqual(actual, expected, f"Rank({input})")

    def test_rank(self):
        """Test the rank function by passing it different combinations
        of sort orders, and inputs, and testing for expected outputs"""
        tests = [
            (["Score"], "Score", 1),
        ]
        for x, (SortOrder, input, expected) in enumerate(tests):
            Rank = RankFn(SortOrder)
            actual = Rank(input)
            # The third argument is a message to help us know what went wrong.
            self.assertEqual(actual, expected,
            f"{x}: Rank({input}): {actual}, want {expected}")

if __name__ == '__main__':
    unittest.main()
