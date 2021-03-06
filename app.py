import random
import re
import logging
import sqlite3

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from pip._vendor import requests

app = Flask(__name__, static_url_path='')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/dna', methods=['POST'])
def dna():
    dna = Dna(request.form['dna'])
    amino = dna.get_amino_acids()
    proteins = find_proteins(amino)

    return jsonify(
        dna=dna.dna,
        mrna=dna.get_mRNA(),
        acids=amino,
        req=request.form,
        proteins=proteins,
    )

@app.route('/dna3', methods=['POST'])
def dna3():
    seq = get_page(request.form['dna']).splitlines()
    seq = ''.join(seq[1:]) + 'X'
    proteins = find_proteins(seq)

    return jsonify(
        acids=seq,
        req=request.form,
        proteins=proteins,
    )


def get_protein(url):
    if url == '':
        return 'UNKNOWN'
    return get_title(get_page(url))


def get_page(url):
    response = requests.get(url)
    return response.text


def get_title(page):
    parsed_html = BeautifulSoup(page)
    return parsed_html.find_all("h2")[0].text


class Dna:
    codes = {
        'I': ['ATT', 'ATC', 'ATA'],
        'L': ['CTT', 'CTC', 'CTA', 'CTG', 'TTA', 'TTG'],
        'V': ['GTT', 'GTC', 'GTA', 'GTG'],
        'F': ['TTT', 'TTC'],
        'M': ['ATG'],
        'C': ['TGT', 'TGC'],
        'A':
            ['GCT', 'GCC', 'GCA', 'GCG'],
        'G':
            ['GGT', 'GGC', 'GGA', 'GGG'],
        'P':
            ['CCT', 'CCC', 'CCA', 'CCG'],
        'T':
            ['ACT', 'ACC', 'ACA', 'ACG'],
        'S':
            ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'],
        'Y':
            ['TAT', 'TAC'],
        'W':
            ['TGG'],
        'Q':
            ['CAA', 'CAG'],
        'N':
            ['AAT', 'AAC'],
        'H':
            ['CAT', 'CAC'],
        'E':
            ['GAA', 'GAG'],
        'D':
            ['GAT', 'GAC'],
        'K':
            ['AAA', 'AAG'],
        'R':
            ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
        'X': ['TAA', 'TAG', 'TGA']
    }

    def __init__(self, dna):
        if dna[:4] == 'http':
            self.dna = self.download(dna)
        else:
            self.dna = self.filter(dna)

    def download(self, url):
        page = get_page(url).splitlines()
        return self.filter(''.join(page[1:]))

    def filter(self, dna):
        dna = dna.upper()
        dna = re.sub(r'W', random.choice(['A', 'T']), dna)
        dna = re.sub(r'S', random.choice(['C', 'G']), dna)
        dna = re.sub(r'M', random.choice(['A', 'C']), dna)
        dna = re.sub(r'K', random.choice(['G', 'T']), dna)
        dna = re.sub(r'R', random.choice(['A', 'G']), dna)
        dna = re.sub(r'Y', random.choice(['C', 'T']), dna)
        dna = re.sub(r'B', random.choice(['C', 'G', 'T']), dna)
        dna = re.sub(r'D', random.choice(['A', 'G', 'T']), dna)
        dna = re.sub(r'H', random.choice(['A', 'C', 'T']), dna)
        dna = re.sub(r'V', random.choice(['A', 'C', 'G']), dna)
        dna = re.sub(r'N', random.choice(['A', 'C', 'G', 'T']), dna)
        return re.sub(r'[^ATCG]', '', dna)

    def get_mRNA(self):
        return re.sub(r'T', 'U', self.dna)

    def get_dna(self, protein):
        res = ''
        for amino in protein:
            res += self.codes[amino][0]
        return res

    def get_amino_acids(self):
        seq = self.dna
        res = ''
        while len(seq) >= 3:
            tripl = seq[:3]
            seq = seq[3:]
            amino = self.find_amino(tripl)
            res += amino
        return res

    def find_amino(self, triplet):
        for amino, codes in self.codes.items():
            if triplet in codes:
                return amino
        logging.warning('Unknown codon ' + triplet)
        return '?'



def find_proteins(seq):
    proteins = []
    prot = False
    cur = ''
    for a in seq:
        if a == 'M':
            prot = True
        if a == 'X':
            print(cur)
            protein_url = select_protein(cur)
            protein_name = get_protein(protein_url)
            proteins.append((cur, protein_url, protein_name))
            prot = False
            cur = ''
        if prot:
            cur += a
    return proteins


def select_protein(protein_seq):
    conn = sqlite3.connect('proteins.sqlite')
    cur = conn.cursor()
    sql = "SELECT protein FROM proteins WHERE sequence = '%s'" % protein_seq

    cur.execute(sql)
    res = cur.fetchone()

    try:
        url = res[0]
        return re.sub('purl', 'www', url)
    except Exception as err:
        return ''
