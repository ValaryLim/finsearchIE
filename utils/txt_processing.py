import pandas as pd

def convert_list_to_txt(l, filename):
    f = open(filename, "w")
    for element in l:
        f.write(element + "\n")
    f.close()

def convert_txt_to_list(filename):
    with open(filename) as f:
        elements = f.readlines()
        elements = [x.strip() for x in elements]
    return elements

def write_html(content, filename):
    with open(filename, 'w') as html_file:
        html_file.write(content)