"""Extracts the bibcodes from the existing publication lists."""
import re

def get_bibcodes(filename):
    bibcodes = []
    for line in open(filename, 'r').readlines():
        matches = re.findall('.*/abs/([^"]+)">.*', line)
        if len(matches) > 0:
            code = matches[0]
            # Hack: hard-coded correction of known problems
            code = code.replace('%26', '&')
            code = code.replace("2014arXiv1407.1057S", "arXiv:1407.1057")
            code = code.replace("2011MNRAS.414.2860A", "2011MNRAS.414.2860O")
            bibcodes.append(code)
    return bibcodes

if __name__ == '__main__':
    k2bibcodes = ["2014PASP..126..398H",
                  "2014arXiv1404.4417B",
                  "2014arXiv1407.3780C",
                  "2014MNRAS.442.2926R",
                  "2014MNRAS.442L..61J",
                  "2014arXiv1403.5888P",
                  "2014arXiv1402.5163H"]
    for science in ['Exoplanets', 'Astrophysics']:
        bibcodes = get_bibcodes('Publications{}.shtml'.format(science))
        for code in bibcodes:
            mission = "kepler"
            if code in k2bibcodes:
                mission = "k2"
            print("{},{},{}".format(code, mission, science.lower()))
