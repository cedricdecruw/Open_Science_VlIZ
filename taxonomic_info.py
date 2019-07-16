#!python3
#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re
import sys

ArchivesIDskeywordsnon=[]
ArchivesIDsAphianon=[]
with open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_metadata.txt") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="|")
    line_count = 1
    #make variables
    aphiaIDs=[]
    taxonomic_terms=[]
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count+=1
            #taxonomic terms
            row[11]= row[11].replace("[", "")
            row[11]= row[11].replace("]", "")
            row[11]= row[11].replace(" ", "")
            taxoinfo = row[11].split(",")
            for info in taxoinfo:
                if info == "'NA'":
                    ArchivesIDskeywordsnon.append(row[6])
                else:
                    info= info.replace("'", "")
                    info= info.replace("\t", "")
                    taxonomic_terms.append(info)
            #aphiaIDS
            row[12]= row[12].replace("[", "")
            row[12]= row[12].replace("]", "")
            row[12]= row[12].replace(" ", "")
            taxoinfo = row[12].split(",")
            for info in taxoinfo:
                if info == "'NA'":
                    ArchivesIDsAphianon.append(row[6])
                else:
                    info= info.replace("'", "")
                    info= info.replace("\t", "")
                    aphiaIDs.append(info)
            #begin exstraction
    print(f'Processed {line_count} lines.')

workbook = xlsxwriter.Workbook('Metadata_scraping_summary_taxonomic_info.xlsx')
bold = workbook.add_format({'bold': True})
worksheetcount = workbook.add_worksheet("taxonomic_summary")

worksheetcount.write('A1', 'taxonomic_term', bold)
worksheetcount.write('B1', 'Count', bold)
worksheetcount.write('E1', 'aphiaID', bold)
worksheetcount.write('F1', 'Count', bold)

#make a dictionary of the taxonomic terms and aphiaIDs

count_taxonomicterms = Counter(taxonomic_terms)
row = 1
col = 0  
for x, y in count_taxonomicterms.items():
    worksheetcount.write(row, col,     x)
    worksheetcount.write(row, col + 1, y)
    row += 1

row = 1
col = 4
countkeywords = Counter(aphiaIDs)      
for x, y in countkeywords.items():
    worksheetcount.write(row, col,     x)
    worksheetcount.write(row, col + 1, y)
    row += 1

worksheetcount.write(0, 8, "archives without taxonomic info")
worksheetcount.write(0, 9, str(len(ArchivesIDskeywordsnon)))
worksheetcount.write(1, 8, "archives without aphiaID info")
worksheetcount.write(1, 9, str(len(ArchivesIDsAphianon)))


worksheetcount.write(0, 11, "archive without taxonomic info")
row=1
col=11
for i in ArchivesIDskeywordsnon:
    worksheetcount.write(row, col, i)
    row += 1

worksheetcount.write(0, 12, "archive without AphiaID info")
row=1
col=12
for i in ArchivesIDsAphianon:
    worksheetcount.write(row, col, i)
    row += 1
workbook.close() 