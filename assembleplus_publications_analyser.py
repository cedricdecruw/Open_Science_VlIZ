#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re

##############################################         CONFIG         ###################################################
spcolids = ["951","27","910","896"] #make array for which i put the spcolids to see if they all are the same (all the same)
namesdatabases = ["Assemblemarine","ScheldeMonitor","jerico-_next","Lifewatch"]
savefolder="C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\" #here you define your folder in which you would like to save your documents

##########################################################################################################################
###############################   Making summary excelsheets/txt-files with calculations   ###############################
##########################################################################################################################

##########################################################################################################################
#######################################    start with keywords and themes:    ############################################
for names in namesdatabases:
    workbook = xlsxwriter.Workbook('Metadata_publications_scraping_summary_thesaurusterms_'+names+'.xlsx')
    bold = workbook.add_format({'bold': True})
    worksheetarh = workbook.add_worksheet("thesaurusterms_keywords_summary")
    #make file so that raw info can be used to make changes 
    with open(savefolder+"info_metadata__publications_"+names+".txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="|")
        line_count = 1
        #make the variables 
        Thesaurusterms = []
        keywords = []
        totalkeywords=[]
        totalthesaurusterms=[]
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #get info here Dasthemes,dasthemeids,Keywords,dataornot,urllink,urlIDs,ids
                Thesaurusterms.append(row[3])
                keywords.append(row[4])
                line_count += 1
                
        #treat the data for excel implemenation
        for keywordrow in keywords:
            #replace
            keywordrow= keywordrow.replace("[", "")
            keywordrow= keywordrow.replace("]", "")
            keywordrow= keywordrow.replace("'", "")
            keywordrow= str(keywordrow.strip())
            #split keywordrow on ;
            keywordwords = keywordrow.split(",")
            for words in keywordwords:
                words= str(words.strip())
                totalkeywords.append(words)
        
        for thesaurus in Thesaurusterms:
            thesaurus= thesaurus.replace("[", "")
            thesaurus= thesaurus.replace("]", "")
            thesaurus= thesaurus.replace("'", "")
            thesaurus= thesaurus.lstrip()
            thesaurus= str(thesaurus.strip())
            thesauruswords = thesaurus.split(",")
            for words in thesauruswords:
                words= str(words.strip())
                totalthesaurusterms.append(words)
        
        #make dictionary of both with the count
        countdiffernetthesaurusterms = Counter(totalthesaurusterms) 
        countdiffernetkeywords = Counter(totalkeywords) 
        #make headers
        worksheetarh.write('A1', 'Thesaurusterm', bold)
        worksheetarh.write('B1', 'Count', bold)
        worksheetarh.write('E1', 'ThesaurustermASFA', bold)
        worksheetarh.write('F1', 'Count', bold)
        #write to file 
        row = 1
        col = 0  
        for x, y in countdiffernetthesaurusterms.items():
            worksheetarh.write(row, col,     x)
            worksheetarh.write(row, col + 1, y)
            row += 1

        row = 1
        col = 4 
        #make txt file of the asfa thesaurusterms
        f= open(savefolder+"info_asfathesaurusterms_"+names+".txt","w+")
        f.write("term,count\n")
        for x, y in countdiffernetkeywords.items():
            f.write(str(x)+","+str(y)+"\n")
            worksheetarh.write(row, col,     x)
            worksheetarh.write(row, col + 1, y)
            row += 1
    f.close()
    workbook.close()   

