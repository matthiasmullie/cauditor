import subprocess
import os
from cauditor import container


def analyze(project, path):
    """ Analyse the commit
    :return: dict
    """
    # create path to store pdepend xml at
    config = container.load_config()
    pdepend_path = config['data']['pdepend_path'].format(pwd=os.getcwd(), project=project['name'])
    subprocess.check_call("mkdir -p {path}".format(path=pdepend_path), shell=True)

    # run pdepend
    xml_path = "{pdepend_path}/pdepend.xml".format(pdepend_path=pdepend_path)
    cmd = "vendor/bin/pdepend --summary-xml={xml_path} {repo_path}".format(xml_path=xml_path, repo_path=path)
    subprocess.check_call(cmd, shell=True)

    # @todo allow folders/files to be excluded?

    # convert pdepend xml to useful data
    data = convert(xml_path)

    # remove leftover files (pdepend xml) created in the process of analyzing #
    subprocess.check_call("rm -rf {path}".format(path=pdepend_path), shell=True)

    return data

def convert(path):
    """ convert pdepend's --summary-xml file to useful data
    :param path: string path of XML file generated by pdepend
    :return: dict
    """
    import xml.etree.ElementTree as etree

    tree = etree.parse(path)
    node = tree.getroot()  # root node: <metrics>

    return {
        'children': [package_data(child) for child in node.findall('package')],
        # executable lines of code
        'loc': int(node.attrib['eloc']),
        # number of classes & methods
        'noc': int(node.attrib['noc']),
        'nom': int(node.attrib['nom']),
    }

def package_data(node):
    """ Read data from <package> node
    :param node: element
    :return: dict
    """
    return {
        'name': node.attrib['name'],
        'children': [class_data(child) for child in node.findall('class')],
    }

def class_data(node):
    """ Read data from <class> node
    :param node: element
    :return: dict
    """
    return {
        'name': node.attrib['name'],
        'children': [method_data(child) for child in node.findall('method')],
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

def method_data(node):
    """ Read data from <method> node
    :param node: element
    :return: dict
    """
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