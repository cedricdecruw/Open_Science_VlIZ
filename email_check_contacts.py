#!python3
#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re
import sys

#variabelen maken voor binnenhalen id info 

totaal=40000
step=5000
current=0

'''
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
    
f= open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_contactpersons.txt","w+")
for record in superiorrecord:
    line = '|'.join([str(i) for i in record])
    try:
        f.write(line + "\n") 
    except UnicodeEncodeError:
        print()
        
f.close()  
'''
#open raw document from earlier made files 
with open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_metadata.txt") as csv_file:
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

with open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_contactpersons.txt") as csv_file:
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
     
f= open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_contactpersons_in_datasets.txt","w+")  
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


        

            
        

        
        


