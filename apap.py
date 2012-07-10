from pySPL import DrugLabel
from utils import file_list
import csv
from datetime import date

filename = "output" + date.today().strftime("%d%m%y") + ".csv"

with open(filename, 'wb') as f:
	#pipe delimiter is so we can use commas elsewhere; nobody uses pipes and excel/google docs do not care
	writer = csv.writer(f,delimiter="|")
	
	#writes header row. need to keep this the same as how it's written below
	writer.writerow(
		["distributor",
		"drug name",
		"ndc",
		"label type",
		"dosage form",
		"marketing start date",
		"revision date",
		"warfarin mentioned?",
		"warfarin section",
		"warfarin time",
		"#actives",
		"actives",
		"url",
		])
	count = 1
	skipped = 0
	for xml_label in file_list:
		print "label ",count," of ",len(file_list),"(%s)" % xml_label.split("/")[-1]
		label = DrugLabel(xml_label)
		
		# exceptions:
		
		# skip kits
		if label.dosage_form() == "KIT" or label.dosage_form() == "BULK INGREDIENT" or label.label_type() == "BULK INGREDIENT":
			print "passing on %s - kit or bulk ingredient" % xml_label.split("/")[-1]
			skipped += 1
			pass
		
		# skip propoxyphene-containing drugs as per Dr. Horn's advice
		elif 'propoxyphene' in label.actives() or 'PROPOXYPHENE' in label.actives() or 'Propoxyphene' in label.actives():
			print "passing on %s - contains propoxyphene" % xml_label.split("/")[-1]
			skipped += 1
			pass
		else:
			writer.writerow([
				label.distributor(),
				label.name(),
				label.ndc(),
				label.label_type(),
				label.dosage_form(),
				label.start_date(),
				label.revision_date(),
				label.test_word("warfarin"),
				label.get_word_section("warfarin"),
				label.get_word_time("warfarin"),
				len(label.actives()),
				label.actives(),
				label.build_url(),
				])
		count+=1
	print "success! (skipped %s labels)" %skipped

f.close()