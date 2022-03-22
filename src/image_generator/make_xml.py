import openpyxl
from xml.etree.ElementTree import Element, SubElement, ElementTree

data = openpyxl.load_workbook("C:/Users/hyejiHan/Downloads/svg_database+pattern_code_ver3.xlsx", data_only=True)

base = data['base']
sticker = data['sticker']

if __name__ == '__main__':
    root = Element('mappingdata')

    pattern = SubElement(root, 'pattern')

    '''SubElement(pattern, 'svgPath').text = svgPath
    SubElement(pattern, 'dxfPath').text = dxfPath'''

    base = SubElement(pattern, 'base')

    '''SubElement(base, 'category').text = category
    SubElement(base, 'feature').text = feature
    SubElement(base, 'block').text = block'''

    #SubElement()







