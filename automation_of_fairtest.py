#!/usr/bin/env python
#script made by Decruw Cedric
import urllib.request, json, time
import requests
import numpy 
import xlsxwriter

'''
=> automation_of_fairtest.py
        * purpose      : To analyse and automise the test of the metadata from assemble+ to determine if the metadata is fair.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : excelsheet named Fairtest_data_database_NAME-OF-DATASET.xlsx and
                         all the json responses if initial amalysis failed.
        * Author       : Decruw Cedric
        * DOC          : ‎Friday, ‎July ‎12, ‎2019, ‏‎10:52:04 AM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : WP2
'''

#config
contact = "0000-0002-7934-1996"
organisation ="VLIZ"
spcolids = ["951","952"] #make array for which i put the spcolids to see if they all are the same (all the same) "27","910","896",
namesdatabases = ["Assemblemarine","Assembleplus"] #"ScheldeMonitor","jerico-_next","Lifewatch",
savefolder="C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\"
totaal=10000
step=5000
nameolol=0
nametests = ["F1: FAIR Metrics Gen2- Unique Identifier","F1: FAIR Metrics Gen2 - Identifier Persistence","F1: FAIR Metrics Gen2 - Data Identifier Persistence",
             "F2: FAIR Metrics Gen2 - Structured Metadata","F2: FAIR Metrics Gen2 - Grounded Metadata","F3: FAIR Metrics Gen2 - Data Identifier Explicitly In Metadata",
             "F3: FAIR Metrics Gen2- Metadata Identifier Explicitly In Metadata","F4: FAIR Metrics Gen2 - Searchable in major search engine",
             "A1.1: FAIR Metrics Gen2 - Uses open free protocol for data retrieval","A1.1: FAIR Metrics Gen2 - Uses open free protocol for metadata retrieval",
             "A1.2: FAIR Metrics Gen2 - Data authentication and authorization","A1.2: FAIR Metrics Gen2 - Metadata authentication and authorization",
             "A2: FAIR Metrics Gen2 - Metadata Persistence","I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (weak)",
             "I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (strong)","I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (weak)",
             "I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (strong)","I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (weak)",
             "I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (strong)","I3: FAIR Metrics Gen2 - Metadata contains qualified outward references)",
             "R1.1: FAIR Metrics Gen2 - Metadata Includes License (strong)","R1.1: FAIR Metrics Gen2 - Metadata Includes License (weak)"]
short_metric=["F1U","F1I","F1D","F2S","F2G","F3D","F3M","F4S","A1D","A1M","A1DA","A1MA","A2M","I1MW","I1MS","I1DW","I1DS","I2MW","I2MS","I3MR","R1LS","R1LW"]
#to import a new collection:
#curl -L -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{"name": "JSON test Test of 2 Metrics", "contact": "0000-0001-6960-357X", "organization": "Hackathon", "description": "A collection of two identifier metrics", "include_metrics": ["http://linkeddata.systems/cgi-bin/FAIR_Tests/gen2_metadata_identifier_in_metadata"]}'  https://w3id.org/FAIR_Evaluator/collections

# to do: make request so that all the metrics can be assigned and can be used
for spcolid in spcolids:
    current=0
    DasIDs=[]
    superiorrecord=[]
    
    #make excelfile 
    workbook = xlsxwriter.Workbook('Fairtest_data_database_'+namesdatabases[nameolol]+'.xlsx')
    bold = workbook.add_format({'bold': True})
    worksheetnor = workbook.add_worksheet("Fairtest_extended_data")
    worksheetcount = workbook.add_worksheet("Summary_fairtest_metrics")
    worksheetsum = workbook.add_worksheet("Summary_datasets")
    worksheetnor.write('A1',"archive")
    worksheetnor.write('B1',"url")
    worksheetnor.write('D1',"succ/fail")
    worksheetnor.write('C1',"metric")
    worksheetnor.write('E1',"Info_fail/succ")
    
    worksheetcount.write('A1',"Metric test")
    worksheetcount.write('B1',"shortmetric")
    worksheetcount.write('C1',"succes(%)")
    
    worksheetsum.write('A1',"archive")
    worksheetsum.write('B1',"url")
    worksheetsum.write('C1',"percentage succes (%)")

    while current < totaal:
        with urllib.request.urlopen("http://www.vliz.be/en/imis?module=dataset&count="+str(step)+"&show=json&start="+str(current)+"&spcolid="+str(spcolid)) as url:
            try:
                data = json.loads(url.read().decode())
                #print(json.dumps(data, indent=4, sort_keys=True))
                for archive in data:
                    DasIDs.append(archive["DasID"])      
                time.sleep(1)
                current+=step
            except:
                print(len(DasIDs))
                pass
    rownor=1
    rowsum=0
    col=0
    #dictionary for tests and count
    counttestdictionary={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0}
    x=0
    totalfairtests=0
    for ids in DasIDs:
        with urllib.request.urlopen("http://www.assembleplus.eu/information-system?module=dataset&show=json&dasid="+str(ids)) as url:
            data = json.loads(url.read().decode())
            #try and search for gbif number 
            try:
                gbifid = data["datasetrec"]["GBIF_UUID"]
                #begin with the fairtests here if succesfull gbif
                #array maken waarin urls komen voor te testen 
                testurls =[]
                urlnormal = "http://www.assembleplus.eu/information-system?module=dataset&show=xml&dasid="+str(ids)
                urlgbif = "https://www.gbif.org/dataset/"+gbifid
                testurls.append(urlnormal)
                testurls.append(urlgbif)
                for url in testurls:  
                    totalfairtests+=1
                    #put tests in here once done
                    #de namen genereren voor de test te doen 
                    description = "Evaluation test of the archive "+str(ids)+" of the database collection "+namesdatabases[nameolol]+" of url: "+url
                    #url = "http://www.assembleplus.eu/information-system?module=dataset&show=xml&dasid="+str(ids)
                    #de curl uitvoeren op de file
                    headers = {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    }
                    
                    data = '{"resource": "'+url+'", "executor": "'+contact+'", "title": "'+description+'"}'
                    response = requests.post("https://w3id.org/FAIR_Evaluator/collections/6/evaluate", headers=headers, data=data, allow_redirects=True)
                    data = response.content
                    print(response.status_code)
                    data = json.loads(data.decode())
                    
                    #open file to put data in it 
                    if "gbif" in url:
                        f= open(savefolder+"jsondumpfolder\\info_jsondumpfile_gbif_dataset"+str(ids)+".txt","w+")
                    else:
                        f= open(savefolder+"jsondumpfolder\\info_jsondumpfile_xml_dataset"+str(ids)+".txt","w+")
                    f.write(json.dumps(data, indent=4, sort_keys=True)) 
                    f.close()

                    results = data["evaluationResult"]
                    testdataresults=results.split("https://w3id.org/FAIR_Evaluator/metrics/")
                    #analyse the chunks
                    #array of results
                    resultsdata = []
                    test = 0
                    succestest=0
                    for result in testdataresults:
                        #extract all data 
                        if "@id" in result:
                            rowdata=[]
                            testname=nametests[test]
                            valueresults = result.split("@value")
                            for values in valueresults:
                                print(values[0:10])
                                #do tests for getting data
                                if '":"0"' in values[0:10]:
                                    print("0 added")
                                    resultsdata.append(ids)
                                    resultsdata.append(url)
                                    resultsdata.append(nametests[test])
                                    resultsdata.append("FAILLURE")
                                    resultsdata.append(result)
                                    test+=1   
                                if '":"1"' in values[0:10]:
                                    print("1 added")
                                    resultsdata.append(ids)
                                    resultsdata.append(url)
                                    resultsdata.append(nametests[test])
                                    resultsdata.append("SUCCESS")
                                    resultsdata.append(result)
                                    counttestdictionary[test]=counttestdictionary[test]+1
                                    succestest+=1
                                    test+=1 
                            #write data to excelsheet nor
                            worksheetnor.write(rownor, col,     resultsdata[0])
                            worksheetnor.write(rownor, col + 1, resultsdata[1])
                            worksheetnor.write(rownor, col + 2, resultsdata[2])
                            worksheetnor.write(rownor, col + 3, resultsdata[3])
                            worksheetnor.write(rownor, col + 4, resultsdata[4])
                            rownor += 1
                        
                    #write overview of dataset to other excelsheet 
                    
                    worksheetsum.write(rowsum, col,     ids)
                    worksheetsum.write(rowsum, col + 1, url)
                    worksheetsum.write(rowsum, col + 2, ((succestest/22)*100))
                    rowsum+=1
                        
            except KeyError:
                print("No Gbif found for DasID {}".format(ids)) 
            time.sleep(1)
            print("DasID {} done".format(ids))
    #on this level write for global summary of database
    row=1
    for x,y in counttestdictionary.items():
        #overview of the metrictests
        worksheetcount.write(row, col,     nametests[x])
        worksheetcount.write(row, col + 1, short_metric[x])
        try:
            worksheetcount.write(row, col + 2, ((y/totalfairtests)*100))
        except:
            worksheetcount.write(row, col + 2, "NA")
        row+=1
        
                   
        
    workbook.close()  
    nameolol+=1
    
#app was made now just get usefull data out of response
#figure out how to exstract the usefull data 
    