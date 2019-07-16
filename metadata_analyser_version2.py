#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re

##############################################         CONFIG         ###################################################
spcolids = ["27","910","896"] #make array for which i put the spcolids to see if they all are the same (all the same)
namesdatabases = ["ScheldeMonitor","jerico-_next","Lifewatch"]
savefolder="C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\" #here you define your folder in which you would like to save your documents

##########################################################################################################################
###############################   Making summary excelsheets/txt-files with calculations   ###############################
##########################################################################################################################

##########################################################################################################################
totaal=40000
step=5000
current=0
superiorrecord=[]
while current < totaal:
    with urllib.request.urlopen("http://www.vliz.be/en/imis?module=person&count="+str(step)+"&show=json&start"+str(current)) as url:
        data = json.loads(url.read().decode())
        #print(json.dumps(data, indent=4, sort_keys=True))
        for archive in data:
            surnames=[]
            firstnames=[]
            personid=[]
            surnames.append(archive["Surname"])
            firstnames.append(archive["Firstname"])
            personid.append(archive["PersID"])
            superiorrecord.extend([[surnames,firstnames,personid]])
    time.sleep(1)
    current+=step
    
f= open(savefolder+"info_contactpersons.txt","w+")
for record in superiorrecord:
    line = '|'.join([str(i) for i in record])
    try:
        f.write(line + "\n") 
    except UnicodeEncodeError:
        print()
        
f.close() 

#######################################    start with keywords and themes:    ############################################
for names in namesdatabases:
    workbook = xlsxwriter.Workbook('Metadata_scraping_summary_themes_keywords_'+names+'.xlsx')
    bold = workbook.add_format({'bold': True})
    worksheetarh = workbook.add_worksheet("archive_summary")
    worksheetcount = workbook.add_worksheet("count_summary_theme_keywords")
    #make file so that raw info can be used to make changes 
    with open(savefolder+"info_metadata_"+names+".txt") as csv_file:
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
        f= open(savefolder+"info_themes_metadata_"+names+".txt","w+")
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
        f= open(savefolder+"info_keywords_metadata_"+names+".txt","w+")
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
    f= open(savefolder+"sunburst_data_"+names+".csv","w+")
    f.write("ids,values,parents,label\n") 
    for x, y in countallinfo.items():
        #make labels by breaking down x
        info = x.split("-")
        label = info[len(info)-1]
        line = ','.join([str(x),str(y[0]),str(y[1]),str(label)])
        f.write(line + "\n") 
    f.close()

#######################################           taxonomic info:           ############################################
    ArchivesIDskeywordsnon=[]
    ArchivesIDsAphianon=[]
    with open(savefolder+"info_metadata_"+names+".txt") as csv_file:
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

    workbook = xlsxwriter.Workbook('Metadata_scraping_summary_taxonomic_info_'+names+'.xlsx')
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
    
#######################################           email info:           ############################################

    with open(savefolder+"info_metadata_"+names+".txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="|")
        line_count = 1
        #make variables
        surnames_metadata=[]
        firstnames_metadata=[]
        roles_metadata=[]
        archiveid=[]
        persid=[]
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                line_count+=1
                surnames_metadata.append(row[8]) 
                firstnames_metadata.append(row[9])
                roles_metadata.append(row[10])
                persid.append(row[6])
                #begin exstraction
        print(f'Processed {line_count} lines.')

    with open(savefolder+"info_contactpersons.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="|")
        line_count = 1
        surnames_contactdata=[]
        firstnames_contactdata=[]
        contactid_contactdata=[]
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                line_count+=1
                surnames_contactdata.append(row[0])
                firstnames_contactdata.append(row[1])
                contactid_contactdata.append(row[2])
        print(f'Processed {line_count} lines.')

        
    #split contacts in the array of the metadata into new arrays
    individual_surnames_metadata=[]
    individual_firstnames_metadata=[]
    individual_roles_metadata=[]
    individual_ids_archive_metadata=[]
    for surnames in surnames_metadata:
        stn_split = surnames.split(',')
        for splits in stn_split:
            #clean out data
            splits = splits.replace("[","")
            splits = splits.replace(" ","")
            splits = splits.replace("]","")
            individual_surnames_metadata.append(splits)
            
    for firsnames in firstnames_metadata:
        stn_split = firsnames.split(',')
        for splits in stn_split:
            splits = splits.replace("[","")
            splits = splits.replace(" ","")
            splits = splits.replace("]","")
            individual_firstnames_metadata.append(splits)
            
    for roles in roles_metadata:
        stn_split = roles.split(',')
        for splits in stn_split:
            splits = splits.replace("[","")
            splits = splits.replace(" ","")
            splits = splits.replace("]","")
            individual_roles_metadata.append(splits)
            
    for ids in persid:
        stn_split = ids.split(',')
        for splits in stn_split:
            splits = splits.replace("[","")
            splits = splits.replace(" ","")
            splits = splits.replace("]","")
            individual_ids_archive_metadata.append(splits)
    
    i=0  
    fullnames_dataset=[]
    while i < len(individual_firstnames_metadata):
        fullnames_dataset.append(' '.join([individual_surnames_metadata[i],individual_firstnames_metadata[i]]))
        i+=1
        
    fullnames_contactdata=[]
    i=0
    while i < len(surnames_contactdata):
        surnames_contactdata[i] = surnames_contactdata[i].replace("[","")
        surnames_contactdata[i] = surnames_contactdata[i].replace("]","")
        surnames_contactdata[i] = surnames_contactdata[i].replace(" ","")
        firstnames_contactdata[i] = firstnames_contactdata[i].replace("[","")
        firstnames_contactdata[i] = firstnames_contactdata[i].replace("]","")
        firstnames_contactdata[i] = firstnames_contactdata[i].replace(" ","")
        fullnames_contactdata.append(' '.join([surnames_contactdata[i],firstnames_contactdata[i]]))
        i+=1

    #do test on the contactids in datasets list 
    contactids_in_dataset = []
    i=0
    while i < len(fullnames_contactdata):
        if fullnames_contactdata[i] in fullnames_dataset:
            contactids_in_dataset.append(contactid_contactdata[i])
        i+=1
        
    f= open(savefolder+"info_contactpersons_in_datasets_"+names+".txt","w+")  
    f.write("PersID,Name,Email,DasID\n") 
    #get records on the contactpersons 
    tick=0
    recordperson_in_dataset = []
    for i in contactids_in_dataset:
        i=i.replace("[","")
        i=i.replace("]","")
        with urllib.request.urlopen("http://www.vliz.be/en/imis?module=person&persid="+str(i)+"&show=json") as url:
            result = json.loads(url.read().decode())
            #print(json.dumps(result, indent=4, sort_keys=True))
            datapersonname=[]
            emailperson=[]
            phoneperson=[]
            gsmperson=[]
            recordperson=[]
            datasetsperson=[]
            datapersonname.append(result["personrec"]["PersName"])
            try:
                for institutes in result["institutes"]:
                    emailperson.append(institutes["instituterec"]["Email"])
                    phoneperson.append(institutes["instituterec"]["Phone"])
                    gsmperson.append(institutes["instituterec"]["GSM"])
            except:
                emailperson.append("NA")
                phoneperson.append("NA")
                gsmperson.append("NA")
            try:
                for xed in result["datasets"]:
                    if str(xed["DasID"]) in individual_ids_archive_metadata:
                        datasetsperson.append(xed["DasID"])
            except:
                datasetsperson.append("NA")  
                
                
                
            recordperson_in_dataset.extend([i,datapersonname,emailperson,phoneperson,gsmperson])  
            recordperson.append(i) 
            recordperson.append(datapersonname) 
            recordperson.append(emailperson) 
            #recordperson.append(phoneperson) 
            #recordperson.append(gsmperson) 
            recordperson.append(datasetsperson)
            print(datasetsperson)
            line = '|'.join([str(i) for i in recordperson])   
            time.sleep(0.2)
            tick+=1
            print("done {}/{} persons".format(tick,len(contactids_in_dataset)))
            try:
                f.write(line + "\n") 
            except UnicodeEncodeError:
                print("code error for contactid {}".format(i)) 

    f.close()