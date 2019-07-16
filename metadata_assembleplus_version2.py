#!/usr/bin/env python
#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re

##########################################################################################################################
#############                       MAKING OF EXCELSHEET WITH RAW EXTRACTED INFO IN IT                       #############   
##########################################################################################################################
#make excel workbook
workbook = xlsxwriter.Workbook('C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\Metadata_scraping.xlsx')
worksheet = workbook.add_worksheet("full_data")

#formatting for excel
bold = workbook.add_format({'bold': True})

#make headers
worksheet.write('A1', 'Archive ID', bold)
worksheet.write('B1', 'URLIDs', bold)
worksheet.write('C1', 'Link-URLs', bold)
worksheet.write('D1', 'file or not', bold)
worksheet.write('E1', 'Keywords Archive', bold)
worksheet.write('F1', 'Themes Archive', bold)
worksheet.write('G1', 'Themes IDs', bold)
worksheet.write('H1', 'Access_constraints', bold)
worksheet.write('I1', 'Surname_projectworker(s)', bold)
worksheet.write('J1', 'Firstname_projectworker(s)', bold)
worksheet.write('K1', 'Role_projectworker(s)', bold)
worksheet.write('L1', 'Taxterm', bold)
worksheet.write('M1', 'AphiaID', bold)
worksheet.write('N1', 'Temp_startD', bold)
worksheet.write('O1', 'Temp_endD', bold)
worksheet.write('P1', 'Temp_progress', bold)
worksheet.write('Q1', 'Geoterm', bold)
worksheet.write('R1', 'Measurement parameters', bold)
worksheet.write('S1', 'Title Archive', bold)
worksheet.write('T1', 'Citations', bold)
worksheet.write('U1', 'person_ids', bold)



row = 1
col = 0

#make array for DasID's and other arrays to store info for excel inplementation
DasIDs = []
superiorrecord = []

with urllib.request.urlopen("http://www.assembleplus.eu//information-system?module=dataset&show=json&count=2000") as url:
    data = json.loads(url.read().decode())
    #print(json.dumps(data, indent=4, sort_keys=True))
    for archive in data:
        DasIDs.append(archive["DasID"])
    print(len(DasIDs))
    

for ids in DasIDs:
#while row < 10:
    with urllib.request.urlopen("http://www.assembleplus.eu//information-system?module=dataset&show=json&dasid="+str(ids)) as url:
    #with urllib.request.urlopen("http://www.assembleplus.eu//information-system?module=dataset&show=json&dasid="+str(DasIDs[row-1])) as url:
        data = json.loads(url.read().decode())
        #extract data
        Dasthemes = []
        dasthemeids = []
        Keywords = []
        dataornot=[] #yes/no
        urllink = []
        urlIDs = []
        access = []
        surname=[]
        firstname=[]
        Role=[]
        termtax=[]
        aphiaIDterm=[]
        tempbd=[]
        temped=[]
        temppro=[]
        geoterm=[]
        measpara=[]
        title=[]
        citation=[]
        persids=[]
        #print(json.dumps(data, indent=4, sort_keys=True))
        try:
            dasthemes = data["dasthemes"]
        except KeyError:
            dasthemes = ["NA"]
        try:
            keywords = data["keywords"]
        except KeyError:
            keywords = ["NA"]
        try:
            urls = data["urls"]
        except KeyError:
            urls = ["NA"]
        try:
            accessd = data["datasetrec"]["AccessConstraint"]
        except KeyError:
            accessd = ["NA"]
        try:
            ownership = data["ownerships"]
        except KeyError:
            ownership = ["NA"]
        try:
            taxinfo = data["taxterms"]
        except KeyError:
            taxinfo = ["NA"]
        try:
            temporald = data["temporal"]
        except KeyError:
            temporald = ["NA"]
        try:
            geodata = data["geographical"]
        except KeyError:
            geodata = ["NA"]
        try:
            mparameterd = data["meastypes"]
        except KeyError:
            mparameterd = ["NA"]
        
        try:
            for theme in dasthemes:
                Dasthemes.append(theme["DasTheme"])
                dasthemeids.append(theme["DasThemeID"])
        except:
            Dasthemes.append("NA")
            dasthemeids.append("NA")
        try:
            for keyword in keywords:
                Keywords.append(keyword["ThesaurusTerm"]) #look for other examples to see if thesaurusterm is only section in keywords
        except:
            Keywords.append("NA")      
        
        try:    
            for urlo in urls:
                dataornot.append(urlo["FileName"])
                urllink.append(urlo["URL"])
                urlIDs.append(urlo["URLTypID"])
        except:
                dataornot.append("NA")
                urllink.append("NA")
                urlIDs.append("NA")
        #access
        try:
            access.append(accessd)
        except:
            access.append("NA")
        #projectworkers
        try:
            for shiprecs in ownership:
                surname.append(shiprecs["Surname"])
                firstname.append(shiprecs["Firstname"])
                Role.append(shiprecs["Role"])
                persids.append(shiprecs["PersID"])
        except:
            surname.append("NA")
            firstname.append("NA")
            Role.append("NA")
        #taxonomy
        try:
            for taxos in taxinfo:
                termtax.append(taxos["TaxTerm"])
                aphiaIDterm.append(taxos["AphiaID"])
        except:
            termtax.append("NA")
            aphiaIDterm.append("NA")
        #temporal
        try:
            for taxos in temporald:
                tempbd.append(taxos["StartDate"])
                temped.append(taxos["EndDate"])
                temppro.append(taxos["Progress"])
        except:
            tempbd.append("NA")
            temped.append("NA")
            temppro.append("NA") 
        #geoterm
        try:
            for geos in geodata:
                geoterm.append(geos["GeoTerm"])
        except:
            geoterm.append("NA")
        #measurements
        try:
            for meas in mparameterd:
                measpara.append(meas["Parameter"])
        except:
            measpara.append("NA")
        #title archive
        try:
            title.append(data["datasetrec"]["StandardTitle"])
        except:
            title.append("NA")
        #citation
        try:
            citation.append(data["datasetrec"]["Citation"])
        except:
            citation.append("NA")
        
        #dump all arrays into superior array
        record = []
        record.extend([Dasthemes,dasthemeids,Keywords,dataornot,urllink,urlIDs,ids,access,surname,firstname,Role,termtax,aphiaIDterm,tempbd,temped,temporald,geoterm,measpara,title,citation,persids])
        #record.extend([Dasthemes,dasthemeids,Keywords,dataornot,urllink,urlIDs,DasIDs[row-1],access,surname,firstname,Role,termtax,aphiaIDterm,tempbd,temped,temporald,geoterm,measpara])
        worksheet.write(row, col,     record[6])
        worksheet.write(row, col + 1, str(record[5]))
        worksheet.write(row, col + 2, str(record[4]))
        worksheet.write(row, col + 3, str(record[3]))
        worksheet.write(row, col + 4, str(record[2]))
        worksheet.write(row, col + 5, str(record[0]))
        worksheet.write(row, col + 6, str(record[1]))
        worksheet.write(row, col + 7, str(record[7]))
        worksheet.write(row, col + 8, str(record[8]))
        worksheet.write(row, col + 9, str(record[9]))
        worksheet.write(row, col + 10, str(record[10]))
        worksheet.write(row, col + 11, str(record[11]))
        worksheet.write(row, col + 12, str(record[12]))
        worksheet.write(row, col + 13, str(record[13]))
        worksheet.write(row, col + 14, str(record[14]))
        worksheet.write(row, col + 15, str(record[15]))
        worksheet.write(row, col + 16, str(record[16]))
        worksheet.write(row, col + 17, str(record[17]))
        worksheet.write(row, col + 18, str(record[18]))
        worksheet.write(row, col + 19, str(record[19]))
        worksheet.write(row, col + 20, str(record[20]))
        row += 1
        superiorrecord.append(record)
        time.sleep(0.2)
        print("{} archives done \n".format(row-1))

#do tests to see if themes recur, same with keywords , and see if any of the urls lead to a file with the data itself
#combine all values into single file 

f= open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_metadata.txt","w+")
for record in superiorrecord:
    line = '|'.join([str(i) for i in record])  
    try:
        f.write(line + "\n") 
    except UnicodeEncodeError:
        print() 
f.close()   
workbook.close()
   
            
            