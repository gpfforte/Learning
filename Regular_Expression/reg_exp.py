import re


def stampa_match(result):
    if type(result) == re.Match:
        print('Result found: ', "'"+result.group()+"'",
              result.start(), result.end(), result.span())
    elif type(result) == list:
        for item in result:
            if type(item) == re.Match:
                stampa_match(item)
            elif type(item) == tuple:
                print(item)
            else:
                print("'"+item+"'")
    else:
        print('No result')


# Stringa dentro cui cercare le occorrenze
test_string = """
Viva le 120 cose migliori del mondo.
Viva le 120 cose migliori del mondo.
pinco.pallino@olio.it
pallo@olio.edu
gpf_forte@hotmail.com
https://www.google.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov
"""

# Regular Expression per cercare match
# re_pattern = re.compile(r"[a-z,A-Z,0-9]+")
# re_pattern = re.compile(r"\w+\b")
# re_pattern = re.compile(r"viva", re.I) # Matches ignoring cases
# re_pattern = re.compile(r"\d+") # Matches whole numbers
# re_pattern = re.compile(
#    r"[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+)(\.[a-zA-Z0-9-.]+)")  # Match Email
re_pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')
# match ritorna un risultato di classe match solo se la sequenza cercata è all'inizio della stringa
print("match")
result = re_pattern.match(test_string)
stampa_match(result)
print()

# search ritorna un risultato iterator in qualsiasi punto della stringa
print("search")
result = re_pattern.search(test_string)
stampa_match(result)
print()

# finditer ritorna un iterable di classe match per ogni risultato trovato nella stringa
print("finditer")
result = re_pattern.finditer(test_string)
stampa_match(list(result))
print()

# findall ritorna una lista per ogni risultato trovato nella stringa, se si usano gruppi (più di uno) ritorna
# una lista di tuple
print("findall")
result = re_pattern.findall(test_string)
stampa_match(result)
print()

# result=re_pattern.search(test_string)
# result=re_pattern.findall(test_string)
# print(re.ASCII, re.DOTALL, re_pattern)
# print(result)
