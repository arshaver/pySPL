from lxml import etree
from datetime import date
import csv

"""contains a suit of functions that take a lxml.etree input drug and return a variety of info about the drug"""

def get_actives(drug):
    """returns a python list of all active moieties listed in the file"""
    actives = []
    for active in drug.findall("//{urn:hl7-org:v3}activeMoiety/{urn:hl7-org:v3}activeMoiety/{urn:hl7-org:v3}name"):
        actives.append(active.text)
    #here converting to a set removes duplicates
    return list(set(actives))

def get_start_date(drug):
    """returns start marketing date as a strftime formatted python date object"""
    date_string = drug.findall("//{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low")[0].attrib["value"]
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return date(year,month,day).strftime("%b %d, %Y")

def get_revision_date(drug):
    """returns label revision date"""
    date_string = drug.findall("//{urn:hl7-org:v3}effectiveTime")[0].attrib["value"]
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:8])
    return date(year,month,day).strftime("%b %d, %Y")

def get_label_type(drug):
    """returns the drug label type, typically 'HUMAN OTC DRUG LABEL' or 'HUMAN PRESCRIPTION DRUG LABEL' """
    drug_type = drug.findall("//{urn:hl7-org:v3}code")[0].attrib["displayName"]
    return drug_type

def get_ndc(drug):
    "returns the drug's NDC number"
    ndc = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}code").attrib["code"]
    return ndc

#TODO check to make sure full name is being returned (eg maybe other tags interfering)
def get_name(drug):
    """returns the drug's name"""
    drug_name = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}name").text
    return drug_name

def get_dosage_form(drug):
    """returns the drug's dosage form"""
    dosage_form = drug.find("//{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}formCode").attrib["displayName"]
    return dosage_form


#the next two functions take file input, not lxml.etree inputs

def check_word(file, word):
    """
    returns True if the string "word" or "Word" or "WORD" is found in any line in the file
    useful for checking if another drug, such as an interaction, is mentioned
    """
    drug = open(file)
    word = str(word).lower()
    for line in drug:
        if (word in line) or (word.capitalize() in line) or (word.upper() in line):
            return True
            break
    return False

def get_word_line(file, word):
    """
    returns the whitespace-stripped line that contains "word" or "Word" or "WORD"
    useful for checking if the "word" listing is legitimate for your purposes
    not that this only displays the first line found containing "word" or "Word" or "WORD"
    """
    drug = open(file)
    word = str(word).lower()
    for line in drug:
        if (word in line) or (word.capitalize() in line) or (word.upper() in line):
            return line.strip()
            break
    return False

def get_url(file):
    """builds and returns the accessdata.fda.gov URL given the XML file name/directory"""
    #first split to get the file name from the whole path, then split to get rid of the .xml
    file_name = str(file.split("/")[-1]).split(".")[0]
    #then build the url
    url = "http://www.accessdata.fda.gov/spl/data/"+file_name+"/"+file_name+".xml"
    return url