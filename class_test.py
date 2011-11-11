from pySPL import DrugLabel

file = "file://localhost/Users/anthonyshaver/Documents/Pharmacy%20School/apap%20warfarin%20interaction%20project/apap_labels/d625c7f1-b5d2-44c3-8675-9141d4b3f8bc.xml"

label = DrugLabel(file=file)

print label.name()

