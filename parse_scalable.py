import csv
import sys
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

def parse_financial_transactions(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = infile.readlines()
        writer = csv.writer(outfile)
        
        # Write the CSV header
        writer.writerow(['Datum', 'Transaktions-Typ', 'Produkt', 'Anzahl', 'Betrag'])

        entry = {}
        for line in reader:
            line = line.strip()
            if not line:
                continue
            
            if "Freitag," in line or "Samstag," in line or "Sonntag," in line or "Montag," in line or "Dienstag," in line or "Mittwoch," in line or "Donnerstag," in line:
                date = datetime.strptime(line, "%A, %d %B %Y").strftime("%d.%m.%Y")
            elif line in ['Einzahlung', 'Sparplan', 'Ausschüttung', 'Kauf', 'Verkauf', 'Ertrag']:
                if entry:
                    writer.writerow([entry.get('Datum'), entry.get('Transaktions-Typ'), entry.get('Produkt'), entry.get('Anzahl'), entry.get('Betrag')])
                entry = {'Datum': date}
                entry['Transaktions-Typ'] = line
            elif 'Stk.' in line:
                entry['Anzahl'] = line.replace(' Stk.', '')
            elif '€' in line:
                entry['Betrag'] = line.replace('€', '').strip()
            else:
                entry['Produkt'] = line
        
        if entry:
            writer.writerow([entry.get('Datum'), entry.get('Transaktions-Typ'), entry.get('Produkt'), entry.get('Anzahl'), entry.get('Betrag')])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        parse_financial_transactions(input_file, output_file)

