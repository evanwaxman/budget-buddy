#!/usr/bin/env python3

import pdfplumber
import csv
import re

def parse_pdf_to_csv(pdf_file, csv_file):
    # Define a regex pattern to match purchase transactions
    # Adjust this pattern based on your specific PDF format
    purchase_pattern = re.compile(r'[\d]+ (\d{1,2}\/\d{1,2}) [\d\/]+ [\d\w]+ (.*) (\d{1,4}\.\d{1,2})')

    with pdfplumber.open(pdf_file) as pdf:
        purchases = []
        
        for page in pdf.pages[2:]:
            text = page.extract_text()
            print(text)
            if text:
                # Find all matches in the text
                matches = purchase_pattern.findall(text)
                for match in matches:
                    date, merchant, amount = match
                    purchases.append([date, merchant.strip(), amount])
    
    # Write the purchases to a CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Merchant', 'Amount'])
        writer.writerows(purchases)

if __name__ == '__main__':
    pdf_file = 'sep_statement.pdf'  # Replace with your PDF file path
    csv_file = 'purchases.csv'  # Desired output CSV file
    parse_pdf_to_csv(pdf_file, csv_file)
    print(f'Purchases extracted to {csv_file}')