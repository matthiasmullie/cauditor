#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

class PdependConverter:
    path = ''

    def __init__(self, path):
        self.path = path

    def convert(self):
        ''' convert pdepend's --summary-xml file to json '''
        import xml.etree.ElementTree as etree

        tree = etree.parse(self.path)
        node = tree.getroot()  # node <metrics>

        return {
            # executable lines of code
            'loc': int(node.attrib['eloc']),
            # number of methods
            'nom': int(node.attrib['nom']),
            # cyclomatic complexity
            'ccn': int(node.attrib['ccn2']),
            'avg-ccn': int(node.attrib['ccn2']) / (int(node.attrib['nom']) or 1),
            # @todo aggregate more metrics
            'children': [self.packageData(child) for child in node.findall('package')]
        }

    def save(self, path):
        import json

        data = self.convert()
        data = json.dumps(data)

        f = open(path, 'w')
        f.write(data)

    def packageData(self, node):
        return {
            'name': node.attrib['name'],
            'children': [self.classData(child) for child in node.findall('class')],
        }

    def classData(self, node):
        return {
            'name': node.attrib['name'],
            # executable lines of code
            'loc': int(node.attrib['eloc']),
            # afferent coupling
            'ca': int(node.attrib['ca']),
            # efferent coupling
            'ce': int(node.attrib['ce']),
            # instability
            'i': int(node.attrib['ce']) / ((int(node.attrib['ce']) + int(node.attrib['ca'])) or 1),
            # code rank
            'cr': float(node.attrib['cr']),
            # weighted metric count
            'wmc': int(node.attrib['wmc']),
            # depth of inheritance tree
            'dit': int(node.attrib['dit']),
            'children': [self.methodData(child) for child in node.findall('method')],
        }

    def methodData(self, node):
        return {
            'name': node.attrib['name'],
            # executable lines of code
            'loc': int(node.attrib['eloc']),
            # extended cyclomatic complexity
            'ccn': int(node.attrib['ccn2']),
            # npath complexity
            'npath': int(node.attrib['npath']),
        }

if __name__ == "__main__":
    import sys
    import getopt

    argv = sys.argv[1:]

    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('pdepend-to-json.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    converter = PdependConverter(inputfile)
    converter.save(outputfile)
