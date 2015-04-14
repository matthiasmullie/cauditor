#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

class PdependConverter:
    path = ''

    def __init__(self, path):
        self.path = path

    def convert(self):
        """ convert pdepend's --summary-xml file to json """
        import xml.etree.ElementTree as etree

        tree = etree.parse(self.path)
        node = tree.getroot()  # node <metrics>

        data = {
            'children': [self.package_data(child) for child in node.findall('package')],
            # executable lines of code
            'loc': int(node.attrib['eloc']),
            # number of classes & methods
            'noc': int(node.attrib['noc']),
            'nom': int(node.attrib['nom']),
        }

        # calculate totals for class & method metrics to get a project-wide
        # idea of how we're doing
        # these totals don't really mean much: high CCN could be either a
        # simple & big project, or a tiny & complex project
        # it gets more interesting when divided by number of classes/methods,
        # to get average metrics across the entire project

        # sum class metrics
        for metric in ['ca', 'ce', 'i', 'dit']:
            data[metric] = sum([
                class_data[metric]
                for package_data in data['children']
                for class_data in package_data['children']
            ])

        # sum method metrics
        for metric in ['ccn', 'npath', 'he', 'hi', 'mi']:
            data[metric] = sum([
                method_data[metric]
                for package_data in data['children']
                for class_data in package_data['children']
                for method_data in class_data['children']
            ])

        return data

    def save(self, path):
        import json

        data = self.convert()
        data = json.dumps(data)

        f = open(path, 'w')
        f.write(data)

    def package_data(self, node):
        return {
            'name': node.attrib['name'],
            'children': [self.class_data(child) for child in node.findall('class')],
        }

    def class_data(self, node):
        return {
            'name': node.attrib['name'],
            'children': [self.method_data(child) for child in node.findall('method')],
            # executable lines of code
            'loc': int(node.attrib['eloc']),
            # afferent coupling
            'ca': int(node.attrib['ca']),
            # efferent coupling
            'ce': int(node.attrib['ce']),
            # instability
            'i': int(node.attrib['ce']) / ((int(node.attrib['ce']) + int(node.attrib['ca'])) or 1),
            # depth of inheritance tree
            'dit': int(node.attrib['dit']),
        }

    def method_data(self, node):
        return {
            'name': node.attrib['name'],
            # executable lines of code
            'loc': int(node.attrib['eloc']),
            # extended cyclomatic complexity
            'ccn': int(node.attrib['ccn2']),
            # npath complexity
            'npath': int(node.attrib['npath']),

            # below metrics need https://github.com/pdepend/pdepend/pull/198
            # halstead effort
            'he': float(node.attrib['he']),
            # halstead intelligent content
            'hi': float(node.attrib['hi']),
            # maintainability index
            'mi': float(node.attrib['mi']),
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
