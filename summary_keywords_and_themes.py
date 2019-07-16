#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re

##########################################################################################################################
###############################        Making summary excelsheet with calculations        ################################
##########################################################################################################################


#open other workbook excel
workbook = xlsxwriter.Workbook('Metadata_scraping_summary.xlsx')
bold = workbook.add_format({'bold': True})
worksheetarh = workbook.add_worksheet("archive_summary")
worksheetcount = workbook.add_worksheet("count_summary_theme_keywords")


#make file so that raw info can be used to make changes 
with open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_metadata.txt") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="|")
    line_count = 1
    #make the variables 
    Themes = []
    Themids = []
    keywords = []
    containsfile = []
    links = []
    linksids = []
    archiveids = []
    ArchivesIDsThemenone = []
    differenttheme=[]
    ArchivesIDskeywordsnon = []
    differentkeywords=[]
    #linked to id of archive (unique for each archive)
    allkeywordnumbers = []
    alldephnumbers = []
    allnumberthemes = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            #get info here Dasthemes,dasthemeids,Keywords,dataornot,urllink,urlIDs,ids
            Themes.append(row[0])
            Themids.append(row[1])
            keywords.append(row[2])
            containsfile.append(row[3])
            links.append(row[4])
            linksids.append(row[5])
            archiveids.append(row[6])
            line_count += 1
            
            #get different themes info (can be related back to id of theme) and deph per theme measurement
            #format row into usefull info
            row[0]= row[0].replace("[", "")
            row[0]= row[0].replace("]", "")
            themeinfo = row[0].split(",")
            betweendephnumbers = []
            numberthemes= len(themeinfo)
            for info in themeinfo:
                if info == "'NA'":
                    dephnumber = 0
                    numberthemes=0
                    ArchivesIDsThemenone.append(row[6])
                else:
                    #get rid of ''
                    info= info.replace("'", "")
                    info= info.replace(" ", "")
                    info= info.replace("\t", "")
                    dephsplit = info.split(">")
                    dephnumber = len(dephsplit)
                    for dephinfo in dephsplit:
                        differenttheme.append(dephinfo)
                betweendephnumbers.append(dephnumber) 
            alldephnumbers.append(betweendephnumbers) 
            allnumberthemes.append(numberthemes)  
            #usefull info about keywords
            row[2]= row[2].replace("[", "")
            row[2]= row[2].replace("]", "")
            keywordinfo = row[2].split(",")
            numberofkeywords = len(keywordinfo)
            for info in keywordinfo:
                if info == "'NA'":
                    numberofkeywords = 0
                    ArchivesIDskeywordsnon.append(row[6])
                else:
                    info= info.replace("'", "")
                    info= info.replace("\t", "")
                    differentkeywords.append(info)
            allkeywordnumbers.append(numberofkeywords)  
                        
    #analysis of different aspects metadata     
    #themes    
    #make headers
    worksheetcount.write('A1', 'Theme', bold)
    worksheetcount.write('B1', 'Count', bold)
    worksheetcount.write('E1', 'Keyword', bold)
    worksheetcount.write('F1', 'Count', bold)
    
    worksheetarh.write('A1', 'Archive ID', bold)
    worksheetarh.write('B1', 'Number themes', bold)
    worksheetarh.write('C1', 'Theme dephs', bold)
    worksheetarh.write('D1', 'Keywords', bold)
    row = 1
    col = 0
    countdiffernetthemes = Counter(differenttheme)  
    f= open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_themes_metadata.txt","w+")
    f.write("Theme | Count \n")
    for x, y in countdiffernetthemes.items():
        worksheetcount.write(row, col,     x)
        worksheetcount.write(row, col + 1, y)
        line = '|'.join([str(x),str(y)])
        f.write(line + "\n") 
        row += 1
    f.close() 
    #keywords
    row = 1
    col = 4
    countkeywords = Counter(differentkeywords) 
    f= open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_keywords_metadata.txt","w+")
    f.write("Keyword | Count \n")     
    for x, y in countkeywords.items():
        worksheetcount.write(row, col,     x)
        worksheetcount.write(row, col + 1, y)
        line = '|'.join([str(x),str(y)])
        f.write(line + "\n") 
        row += 1
    f.close()        
    print(f'Processed {line_count} lines.')
    
    
    #individual archive analysis (archive summary)
    i=0
    row = 1
    col = 0
    while i<len(alldephnumbers):
        worksheetarh.write(row, col,     archiveids[i])
        worksheetarh.write(row, col + 1, allnumberthemes[i])
        worksheetarh.write(row, col + 2, str(alldephnumbers[i]))
        worksheetarh.write(row, col + 3, allkeywordnumbers[i])
        i+=1
        row+=1
        

workbook.close()   


#make csv file for sunburst chart in viewer
allinfo=[]
parentchild={}
for i in Themes:
    #clean up data
    i= i.replace("[", "")
    i= i.replace("]", "")
    i= i.replace("'", "")
    i= i.replace("-", "_")
    i= i.replace(" ", "")
    i= i.replace(">", "-")
    i= i.replace("\t", "")
    #split each line into individual data
    lineinfo = i.split(",")
    for info in lineinfo:
        allinfo.append(info)
        childsplit = info.split("-")
        x=0
        while x < len(childsplit):
            #child logic
            if x == 0:
                childpart = childsplit[0]
                allinfo.append(childpart)
                parentpart = ""
            if x == 1:
                parentpart = childsplit[0]
                childpart = childsplit[0]+"-"+childsplit[1]
                allinfo.append(childpart)
            if x == 2:
                parentpart = childsplit[0]+"-"+childsplit[1]
                childpart = childsplit[0]+"-"+childsplit[1]+"-"+childsplit[2]
                allinfo.append(childpart)
            if x == 3:
                parentpart = childsplit[0]+"-"+childsplit[1]+"-"+childsplit[2]
                childpart = childsplit[0]+"-"+childsplit[1]+"-"+childsplit[2]+"-"+childsplit[3]
                allinfo.append(childpart)
            if x == 4:
                parentpart = childsplit[0]+"-"+childsplit[1]+"-"+childsplit[2]+"-"+childsplit[3]
                childpart = childsplit[0]+"-"+childsplit[1]+"-"+childsplit[2]+"-"+childsplit[3]+"-"+childsplit[4]
                allinfo.append(childpart)
            x+=1
            childpart=childpart.replace(" ","")
            childpart=childpart.replace("\t","")
            parentpart=parentpart.replace(" ","")
            parentpart=parentpart.replace("\t","")
            parentchild[childpart]=parentpart
            
for x,y in parentchild.items():
    print("child:{} == parent:{}".format(x,y))
    

countallinfo = Counter(allinfo) 
for x, y in countallinfo.items():
    print("theme:{} count:{}".format(x,y))

#update dictionary
for x, y in countallinfo.items():
    countallinfo[x]=[y,parentchild[x]]

for x, y in countallinfo.items():
    print(x,y)

#transform dictionary into csv file
f= open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\sunburst_data.csv","w+")
f.write("ids,values,parents,label\n") 
for x, y in countallinfo.items():
    #make labels by breaking down x
    info = x.split("-")
    label = info[len(info)-1]
    line = ','.join([str(x),str(y[0]),str(y[1]),str(label)])
    f.write(line + "\n") 
f.close()

#create second csv file for 
    

    
   
            
            
            
            
        
    