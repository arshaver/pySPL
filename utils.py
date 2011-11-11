from lxml.html import parse
from lxml import etree


#gets all XML files from a directory and returns them as a list with full directory
def get_xml_files(dir):
    import os
    filename_list = []
    for file in os.listdir(dir):
        if file.split(".")[-1] == "xml":
            filename_list.append(dir+file)
    return filename_list


#this directory contains all of the results (eg the *.xml files) of this query: http://labels.fda.gov/getIngredientName.cfm?beginrow=1&numberperpage=10000&searchfield=acetaminophen&OrderBy=IngredientName
file_list = get_xml_files("./apap_labels/") #need trailing slash


def is_xml(url):
    """checks if an url is xml based on extension"""
    if url.split(".")[-1] == "xml":
        return True
    else:
        return False

def get_urls(search_url="http://labels.fda.gov/getIngredientName.cfm?beginrow=1&numberperpage=10000&searchfield=acetaminophen&OrderBy=IngredientName"):
    
    """returns a list of unique xml urls from a 
    labels.fda.gov/getIngredientName search
    the default search is for activeingredient=acetaminophen"""    
       
    #parse the search_url document
    page = parse(search_url)
    
    #get a list of all urls
    urls = page.xpath('//a/@href')
    
    #filter out the non *.xml links
    #set gets rid of duplicates
    return list(set(filter(is_xml, urls))) #returning 1497 urls as of 11/10/11 (?!)


#############################################################
#####To download files from FDA site into ./apap_labels/#####
#############################################################

import urllib2
import os
import utils

path = "./apap_labels/"
def download(url):
    xmlfile = urllib2.urlopen(url)
    file_name = url.split("/")[-1]
    output = open(os.path.join(path,file_name),'wb')
    output.write(xmlfile.read())
    output.close()


urls = utils.get_urls()
length = len(urls)

count = 1
for url in urls:
    print count," of ",length
    try:
        download(url)
    except:
        print "problem with %s" % url
    count+=1

#produced 3 errors for:
#http://www.accessdata.fda.gov/spl/data/e7a619eb-7ecf-45a6-a545-41cdabb16b58/e7a619eb-7ecf-45a6-a545-41cdabb16b58.xml
#http://www.accessdata.fda.gov/spl/data/c78c1005-b621-42fa-8fef-918a9d824e5d/c78c1005-b621-42fa-8fef-918a9d824e5d.xml
#http://www.accessdata.fda.gov/spl/data/bf6aa0e2-0400-4db6-95d1-994e547b52ba/bf6aa0e2-0400-4db6-95d1-994e547b52ba.xml