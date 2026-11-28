"""Read values and merged-cell origins from local XLSX files without dependencies.

Does not execute formulas, macros or workbook instructions. Formula cells use their
cached value. Original workbooks are never modified.
"""
from pathlib import Path
import posixpath
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile

NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def col_number(value):
    out = 0
    for char in value:
        out = out * 26 + ord(char) - 64
    return out


def address(value):
    match = re.fullmatch(r'([A-Z]+)(\d+)', value)
    return int(match[2]), col_number(match[1])


def col_name(number):
    value = ''
    while number:
        number, rem = divmod(number - 1, 26)
        value = chr(65 + rem) + value
    return value


class Sheet:
    def __init__(self, filename, name, xml, strings):
        self.filename, self.name = filename, name
        self.values, self.origins = {}, {}
        for cell in xml.findall('s:sheetData/s:row/s:c', NS):
            key = address(cell.attrib['r'])
            raw = cell.find('s:v', NS)
            value = raw.text if raw is not None and raw.text else ''
            if cell.get('t') == 's':
                value = strings[int(value)]
            elif cell.get('t') == 'inlineStr':
                value = ''.join(t.text or '' for t in cell.findall('.//s:t', NS))
            self.values[key] = value
        for merge in xml.findall('s:mergeCells/s:mergeCell', NS):
            start, end = map(address, merge.get('ref').split(':'))
            for row in range(start[0], end[0] + 1):
                for col in range(start[1], end[1] + 1):
                    self.origins[row, col] = start
        self.max_row = max((r for r, _ in self.values), default=0)

    def cell(self, row, col, merged=True):
        key = self.origins.get((row, col), (row, col)) if merged else (row, col)
        return str(self.values.get(key, '')).strip()

    def source(self, row, col):
        r, c = self.origins.get((row, col), (row, col))
        return f'{self.filename} / {self.name}!{col_name(c)}{r}'

    def records(self):
        headers = {col: self.cell(1, col) for row, col in self.values if row == 1 and self.cell(1, col)}
        for row in range(2, self.max_row + 1):
            data = {key: self.cell(row, col) for col, key in headers.items()}
            if any(data.values()):
                yield row, data


def read_workbook(path):
    path = Path(path)
    with ZipFile(path) as archive:
        if sum(item.file_size for item in archive.infolist()) > 50_000_000:
            raise ValueError('Workbook vượt giới hạn đọc 50 MB.')
        strings = []
        if 'xl/sharedStrings.xml' in archive.namelist():
            strings = [''.join(t.text or '' for t in item.findall('.//s:t', NS))
                       for item in ET.fromstring(archive.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        rels = {item.get('Id'): item.get('Target')
                for item in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
                if item.get('TargetMode') != 'External'}
        sheets = {}
        for item in ET.fromstring(archive.read('xl/workbook.xml')).find('s:sheets', NS):
            target = rels[item.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
            sheets[item.get('name')] = Sheet(path.name, item.get('name'), ET.fromstring(archive.read(target)), strings)
        return sheets
