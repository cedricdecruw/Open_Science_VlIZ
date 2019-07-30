#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re

'''
=> metadata_analyser_version2.py:
        * purpose      : To analyse the metadata gathered from metadata extraction script.
        * input        : requires the input of the metadatafile of required databases eg: info_metadata_NAME-OF-DATASET2.txt
        * output       : analysis files (contact analysis, geolocation analysis, sunburst.csv file, etc)
        * Author       : Decruw Cedric
        * DOC          : ‎Wednesday, ‎July ‎10, ‎2019, ‏‎11:36:52 AM
        * Requirements : Requires spcols_metadata_extraction_version3.py to be ran.
        * PCF          : Assemble+
'''

##############################################         CONFIG         ###################################################
spcolids = ["952"] #make array for which i put the spcolids to see if they all are the same (all the same) "27","910","896",
namesdatabases = ["Assembleplus"] #"ScheldeMonitor","jerico-_next","Lifewatch",
savefolder="S:\\datac\\Projects\\AssemblePlus\\NA2_DataAccess\\Development4AssemblePCollection\\" #here you define your folder in which you would like to save your documents

##########################################################################################################################
###############################   Making summary excelsheets/txt-files with calculations   ###############################
##########################################################################################################################
'''
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
'''
##########################################################################################################################
###############################   delete dasids from metadata for better representation    ###############################
##########################################################################################################################
for names in namesdatabases:

    with open(savefolder+"Dasids_to_delete.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 1
        dasidstodelete = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                dasidstodelete.append(row[0])
                line_count += 1
        csv_file.close()

    with open(savefolder+"info_metadata_"+names+".txt") as csv_file, open(savefolder+"info_metadata_"+names+"2.txt","w+") as out:
        csv_reader = csv.reader(csv_file, delimiter="|")
        line_count = 1
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                test = 0
                dasids = row[6]
                for i in dasidstodelete:
                    if i == dasids:
                        print("deleted archive {} from file".format(dasids))
                        test = 1
                if test == 0:
                    line = '|'.join([str(i) for i in row])  
                    try:
                        out.write(line + "\n") 
                    except UnicodeEncodeError:
                        print("Unicode Encode Error")                
                line_count += 1
        csv_file.close()
        out.close()

#######################################    start with keywords and themes:    ############################################

    workbook = xlsxwriter.Workbook('Metadata_scraping_summary_themes_keywords_'+names+'.xlsx')
    bold = workbook.add_format({'bold': True})
    worksheetarh = workbook.add_worksheet("archive_summary")
    worksheetcount = workbook.add_worksheet("count_summary_theme_keywords")
    #make file so that raw info can be used to make changes 
    with open(savefolder+"info_metadata_"+names+"2.txt") as csv_file:
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
                        info= re.sub(r"\s+", "", info)
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
        i= i.replace(">", "-")
        i= i.replace("\t", "")
        #delete leading spaces
        i=re.sub(r"\s+", "", i)
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
                #childpart=childpart.replace(" ","")
                childpart=childpart.replace("\t","")
                parentpart=parentpart.replace(" ","")
                #parentpart=parentpart.replace("\t","")
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
        lastword = info[len(info)-1]
        searchkeywords = lastword.split("_")
        #clean up keywords so i don't have to do that in R
        blabla=0
        for i in searchkeywords:  
            i=i.replace("(","")
            i=i.replace(")","")
            i=i.replace("e.g."," ")
            i=i.replace("&"," ")
            i=i.replace("/"," ")
            #i splitsen op spatie om errors te voorkomen
            kek = i.split(" ")
            if kek[0] == "Watercomposition":
                searchterms = "Water+composition"
                stjson = "Water%20composition"
            elif kek[0] == "Bulkchemistry":
                searchterms = "Bulk+chemistry"
                stjson = "Bulk%20chemistry"
            elif kek[0] == "Pollutionlevels":
                searchterms = "Pollution"
                stjson = "Pollution"
            elif kek[0] == "Environmentalquality":
                searchterms = "Environmental+quality"
                stjson = "Environmental%20quality"  
            elif kek[0] == "Suspendedmatter":
                searchterms = "Suspended+matter"
                stjson = "Suspended%20matter"  
            elif kek[0] == "Upperairobservations":
                searchterms = "Upper+air+observations"
                stjson = "Upper%20air%20observations" 
            elif kek[0] == "Underwateracoustics":
                searchterms = "Underwater+acoustics"
                stjson = "Underwater%20acoustics" 
            elif kek[0] == "Otherinorganicchemistry":
                searchterms = "Other+inorganic+chemistry"
                stjson = "Other%20inorganic%20chemistry"   
            elif kek[0] == "Siteassessments":
                searchterms = "Site+assessments"
                stjson = "Site%20assessments"  
            elif kek[0] == "Coastalstudies":
                searchterms = "Coastal+studies"
                stjson = "Coastal%20studies" 
            elif kek[0] == "Dissolvedgases":
                searchterms = "Dissolved+gases"
                stjson = "Dissolved%20gases" 
            elif kek[0] == "Opticalmeasurements":
                searchterms = "Optical+measurements"
                stjson = "Optical%20measurements" 
            elif kek[0] == "Exploratoryfishing":
                searchterms = "Exploratory+fishing"
                stjson = "Exploratory%20fishing"           
            else:
                #put custom input here
                i = kek[0]
                if blabla == 0:
                    searchterms= i
                    stjson = i
                    blabla+=1
                else:
                    searchterms=searchterms+"+"+i
                    stjson = stjson+"%20"+i
        golink = "http://www.assembleplus.eu/datasetsearch?ktpKO=169548&imisfpspcol=990&Field="+searchterms+"&year=&bentaut=#vlizimisfp"
        #use link to get real info of biology file info 
        print(stjson)
        with urllib.request.urlopen("http://www.assembleplus.eu/node/2047?show=jsonportal&cnt=1&module=dataset&count=50&Field="+stjson+"&spcol=990") as url:
            data = json.loads(url.read().decode())
            count = data["cnt"]
            if count == 0:
                print("Nothing found for {}".format(searchterms))
            else:
                label = "<b><a href='"+golink+"'>"+lastword+"</a></b>"
                line = ','.join([str(x),str(count),str(y[1]),str(label)])
                f.write(line + "\n") 
                time.sleep(0.3)
    f.close()

#######################################           taxonomic info:           ############################################
    ArchivesIDskeywordsnon=[]
    ArchivesIDsAphianon=[]
    with open(savefolder+"info_metadata_"+names+"2.txt") as csv_file:
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

    with open(savefolder+"info_metadata_"+names+"2.txt") as csv_file:
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

############################################## date extractor of datasets ##############################################
#put back tab when puttting back for all databases 
with open(savefolder+"info_metadata_"+names+"2.txt") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="|")
    line_count = 1
    #make variables
    begindate =[]
    enddate = []
    archiveids=[]
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count+=1
            archiveids.append(row[6])
            begindate.append(row[13]) 
            enddate.append(row[14])
    
    #extract beginyear endyear and total time investigation
    #clean up data
    beginyears =[]
    tofillindatestart=0
    for date in begindate:
        date = date.replace("[","") 
        date = date.replace("]","") 
        #split date into multiple if any 
        stn_split = date.split(',')
        x=0
        for i in stn_split:
            if x ==0:
                begindateproject = i
                x+=1
        #dissect date
        begindateproject = begindateproject.replace("'","") 
        if begindateproject == "NA":
            tofillindatestart = "Not known"
        else:
            stn_split = begindateproject.split('-')
            x=0
            for i in stn_split:
                if x ==0:
                    tofillindatestart = i
                    x+=1
        beginyears.append(tofillindatestart)
    #same for enddate
    endyears=[]
    tofillindateend=0
    for date in enddate:
        date = date.replace("[","") 
        date = date.replace("]","") 
        #split date into multiple if any 
        stn_split = date.split(',')
        x=0
        for i in stn_split:
            if x ==0:
                begindateproject = i
                x+=1
        
        
        #dissect date
        if begindateproject == "None":
            tofillindateend="None"
        else:
            begindateproject = begindateproject.replace("'","") 
            if begindateproject == "NA":
                tofillindateend = "Not known"
            else:
                stn_split = begindateproject.split('-')
                x=0
                for i in stn_split:
                    if x == (len(stn_split)-3):
                        tofillindateend = i
                    x+=1
        endyears.append(tofillindateend)

    #make runtime dates
    runtimedatasets=[]
    x=0
    for i in endyears:
        try:
            runtime = int(i)-int(beginyears[x])
            runtimedatasets.append(runtime)
        except ValueError:
            runtimedatasets.append("Not known")
        x+=1
    
    #make file to put info in 
    f= open(savefolder+"info_runtime_in_datasets.txt","w+")  
    f.write("DasID,beginyear,endyear,runtime\n") 
    x=0
    for i in endyears:
        f.write(archiveids[x]+","+str(beginyears[x])+","+str(i)+","+str(runtimedatasets[x])+"\n")
        x+=1
    f.close()
    
############################################### make the coordinates file ##########################################
    #make file 
    f= open(savefolder+"info_coordinates_"+names+".txt","w+")
    f.write("DasID!document type!extension!region!lat!long!popup\n")
    with open(savefolder+"info_metadata_"+names+"2.txt") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="|")
        line_count = 1
        #make the variables 
        archiveids = []
        geolocation = []
        urlsofdata = []
        geoids=[]
        reallinkdata=[]
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #get info here Dasthemes,dasthemeids,Keywords,dataornot,urllink,urlIDs,ids
                geolocation.append(row[16])
                urlsofdata.append(row[3])
                archiveids.append(row[6])
                geoids.append(row[23])
                reallinkdata.append(row[4])
                line_count += 1
        #split geloaction on '
        x=0
        for geo in geolocation:
            geoidarh = geoids[x]
            reallink = reallinkdata[x]
            indgeoid = []
            localareas = []
            coordinates = {}
            document_name = []
            idarchive = archiveids[x]
            url = urlsofdata[x]
            coordinateslong = []
            coordinateslat = []
            typedoc = []
            actuallink=[]
            reallink = reallink.replace("[","")
            reallink = reallink.replace("]","")
            reallink = reallink.replace(" ","")
            reallink = reallink.replace("'","")
            fucklinks = reallink.split(",")
            for real in fucklinks:
                actuallink.append(real)
                print(real)
            locations = geo.split("'")
            for locs in locations:
                if locs != "[" and locs != "]" and locs != " ," and locs!= ", ":
                    localareas.append(locs)
                    #print(locs)
            geoidarh = geoidarh.replace("[","")
            geoidarh = geoidarh.replace("]","")
            geoidarh = geoidarh.replace(" ","")
            locations = geoidarh.split(",")
            for locs in locations:
                indgeoid.append(locs)
            url = url.replace("[","")
            url = url.replace("]","")
            url = url.replace("'","")
            indivurls = url.split(",")
            ba=0
            for iurl in indivurls:
                try:
                    golink = actuallink[ba]
                except IndexError:
                    pass
                popuptext = ""
                if iurl != "NA" and iurl != "None" and iurl != " None" and iurl != "None ":
                    #foreach indgeoid get long and lat
                    z=0
                    for i in indgeoid:
                        if i != "None" and i !="":
                            with urllib.request.urlopen("http://www.marineregions.org/rest/getGazetteerRecordByMRGID.json/"+str(i)+"/") as urlp:
                                data = json.loads(urlp.read().decode())
                                coordinates[localareas[z]]=[data["longitude"],data["latitude"]]
                                #coordinateslat.append(data["latitude"]) 
                                #coordinateslong.append(data["longitude"])
                                time.sleep(0.3)
                        else:
                            #coordinateslat.append("NA") 
                            #coordinateslong.append("NA")
                            coordinates[localareas[z]]=["NA","NA"]
                    #get extension
                    iurlsplit = iurl.split(".")
                    try:
                        extension = iurlsplit[1]
                        extension= extension.replace(" ","")
                    except IndexError:
                        extension = iurl
                        pass
                        #print(extension)
                    #define the category based on the extension
                    test=0
                    if extension == "xls" or extension == "xlsx":
                            typedoc.append("Spreadsheet")
                            test=1
                    if "doc" in extension:
                        typedoc.append("Word-document")
                        test=1
                    if "rar" in extension or "zip" in extension:
                        typedoc.append("compressed")
                        test=1
                    if "mdb" in extension:
                        typedoc.append("Microsoft database")
                        test=1
                    if "BAK" in extension:
                        typedoc.append("Backup file")
                        test=1
                    if "wk4" in extension:
                        typedoc.append("Lotus 4 Worksheet")
                        test=1
                    if test != 1:
                        typedoc.append("others")

                    #make popupbox text
                    popuptext = "<b><a href='"+golink+"'>"+iurl+"</a></b><br/><b>Dataset: "+str(archiveids[x])+"</b>"
                    
                    #put everything together in a line 
                    for target,co in coordinates.items():
                        for doc in typedoc:
                            try:
                                line = str(archiveids[x])+"! "+doc+"! "+extension+"! "+target+"! "+str(co[0])+"! "+str(co[1])+"! "+popuptext
                            except IndexError:
                                pass
                            print(line)
                            f.write(line+"\n")
                    z+=1
                ba+=1
            x+=1

    f.close()
