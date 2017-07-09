# CSC-555-DNA

## Task

Implement a program that accepts as input any DNA sequence and outputs:

a) the transcribed mRNA sequence;

b) the translated amino acid sequence;

c) all possible encoded proteins.

* Tip1: Proteins are amino acid sequences starting at Methionine (AUG) and ending at a terminator codon (i.e., UAA, UAG, UGA). Ignore unfinished and/or overlapping sequences.
* Tip2: Use the 2 compressed and attached files: "proteins.csv" contain proteins and their amino acid sequences. "codons.csv" has the amino acids' transliteration codes. 
* Tip3: Not all amino acid sequences encode known proteins, so if you cannot find a match between sequences and proteins, just output "UNKNOWN".

bonus) 
(+10pts) bonus points for implementations that allow the user to enter the web link to an amino acid sequence such as in http://www.ebi.ac.uk/ena/data/... and outputs the list of protein names and links to their info such as in http://www.uniprot.org/uniprot... (1st column in proteins.csv), in addition to the info in a), b) and c).


## Installation

The application was made using Python(Flask framework)/SQLite for backend and jQuery lib for frontend.
It requires `Flask` and `BeautifulSoup` packages to be installed.

To start the app run the following commands
`FLASK_APP=app.py`
`flask run`

Then open `http://localhost:5000` in your browser.

## Authors


* **Alexey Rastaturin** - 90725

