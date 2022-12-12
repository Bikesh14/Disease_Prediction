# import csv
# import json


# reader = csv.reader(open('symptom_precaution.csv', 'r'))
# dict = {}
# for row in reader:
#    key, value = row
#    dict[key] = value

# print(dict)

# with open('symptom_precaution.txt', 'w') as convert_file:
#      convert_file.write(json.dumps(dict))


import json
with open('symptom_Description.txt') as f1:
    s_d = f1.read()
symptom_description=json.loads(s_d)

print(symptom_description["Allergy"])

with open('symptom_precaution.txt') as f2:
    s_p = f2.read()
symptom_precaution=json.loads(s_p)

symptom_precaution=symptom_precaution["Allergy"]
symptom_precaution=list(symptom_precaution.split(","))
print(type(symptom_precaution["Allergy"]))
print(symptom_precaution["Allergy"])