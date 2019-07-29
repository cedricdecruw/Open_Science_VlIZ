# Open_Science_VlIZ
Collection of code used by the Open Science team at VLIZ

Each file has:
* purpose
* input
* output : (if file contains ammount fields #)
* Author
* Date of creation (DOC)
* Requirements
* Project for which file was created for (PCF) 

# Summary of files:


##Assemble+ Scripts:

    => assembleplus_Emodneteurobis_checker.py:
        * purpose      : To check if the datasets that are present in Assemble+ are also present in Emodnet or eurobis.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : textfile named info_eurobis_emodnet_assembleplus.txt containing 3 fields
        * Author       : Decruw Cedric
        * DOC          : Wednesday, ‎July ‎10, ‎2019, ‏‎1:25:49 PM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : Assemble+
    
    => assembleplus_publications_analyser.py:
        * purpose      : To analyse the metadata from the extracted imis databases.
        * input        : requires the input of the metadatafile of required databases eg: info_metadata__publications_assemble.txt.
        * output       : textfile named info_asfathesaurusterms_NAME-OF-DATASET.txt containing 2 fields and 
                         a excelfile named Metadata_publications_scraping_summary_thesaurusterms_NAME-OF-DATASET.xlsx
        * Author       : Decruw Cedric
        * DOC          : Monday, ‎July ‎15, ‎2019, ‏‎10:37:03 AM
        * Requirements : Requires spcols_metadata_extraction_version3.py to be ran.
        * PCF          : Assemble+

    => assembleplus_vliz_checker.py:
        * purpose      : To analyse the metadata from the extracted imis databases.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : textfile named metadata_vliz_checker__NAME-OF-DATASET.txt containing 5 fields
        * Author       : Decruw Cedric
        * DOC          : Wednesday, ‎July ‎10, ‎2019, ‏‎1:02:43 PM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : Assemble+
    
    => email_check_contacts.py:
        * purpose      : To analyse the contacts that are in given datasets to extract information about people_ids.
        * input        : requires the input of the metadatafile of required databases eg: info_metadata_NAME-OF-DATASET.txt
        * output       : textfile named info_contactpersons_in_datasets_NAME-OF-DATASET.txt containing 4 fields
        * Author       : Decruw Cedric
        * DOC          : ‎Friday, ‎July ‎5, ‎2019, ‏‎2:18:33 PM
        * Requirements : Requires spcols_metadata_extraction_version3.py to be ran.
        * PCF          : Assemble+
    
    => metadata_analyser_version2.py:
        * purpose      : To analyse the metadata gathered from metadata extraction script.
        * input        : requires the input of the metadatafile of required databases eg: info_metadata_NAME-OF-DATASET.txt
        * output       : analysis files (contact analysis, geolocation analysis, sunburst.csv file, etc)
        * Author       : Decruw Cedric
        * DOC          : ‎Wednesday, ‎July ‎10, ‎2019, ‏‎11:36:52 AM
        * Requirements : Requires spcols_metadata_extraction_version3.py to be ran.
        * PCF          : Assemble+
    
    => spcols_metadata_extraction_version3.py:
        * purpose      : To gqther metadata from urls.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : info_metadata_NAME-OF-DATASET.txt with 23 fields and excelfile
        * Author       : Decruw Cedric
        * DOC          : ‎‎Wednesday, ‎July ‎10, ‎2019, ‏‎10:11:34 AM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : Assemble+
    



##WP2 Related Scripts:

    => automation_of_fairtest.py
        * purpose      : To analyse and automise the test of the metadata from assemble+ to determine if the metadata is fair.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : excelsheet named Fairtest_data_database_NAME-OF-DATASET.xlsx and
                         all the json responses if initial amalysis failed.
        * Author       : Decruw Cedric
        * DOC          : ‎Friday, ‎July ‎12, ‎2019, ‏‎10:52:04 AM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : WP2
    
    => Fairtest.py
        * purpose      : To analyse and automise the test of the metadata from assemble+ to determine if the metadata is fair.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : excelsheet named Fairtest_data_database_NAME-OF-DATASET.xlsx
        * Author       : Decruw Cedric
        * DOC          : ‎Monday, ‎July ‎1, ‎2019, ‏‎3:29:29 PM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : WP2
    

##Other Scripts:
    => tussenscript.py
        * purpose      : Dumpfile for code.
        * input        : no fileinput required.
        * output       : no output.
        * Author       : Decruw Cedric
        * DOC          : ‎Friday, ‎July ‎5, ‎2019, ‏‎13:52:04 AM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : Others