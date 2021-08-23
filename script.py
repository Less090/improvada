import json
import csv
import xmltodict


filenames = (
    'csv_data_1.csv',
    'csv_data_2.csv',
    # 'basic_results.tsv',
    # 'advanced_results.tsv',
    'json_data.json',
    'xml_data.xml'
)

filename_to_file_map = {
    f: open(f)
    for f in filenames
}

fieldnames = []
for filename, file in filename_to_file_map.items():
    if filename.endswith('.csv'):
        reader = csv.DictReader(file)
        fieldnames.extend(reader.fieldnames)
    elif filename.endswith('.tsv'):
        reader = csv.DictReader(file, delimiter='\t')
        fieldnames.extend(reader.fieldnames)
    elif filename.endswith('.json'):
        data = json.loads(file.read())['fields']
        json_fieldnames = data[0].keys()
        fieldnames.extend(json_fieldnames)
    elif filename.endswith('.xml'):
        parsed_file = xmltodict.parse(file.read())
        object_rows = parsed_file['root']['objects']
        # incorrect format of file - objects must be list, not dict
        row = {
            v['@name']: v['value']
            for v in object_rows['object']
        }
        fieldnames.extend(row.keys())

fieldnames = set(fieldnames)

with open('b_result.tsv', 'w') as result_file:
    writer = csv.DictWriter(
        result_file,
        fieldnames=list(sorted(fieldnames)),
        delimiter='\t',
    )
    writer.writeheader()
    for filename, file in filename_to_file_map.items():
        file.seek(0)
        if filename.endswith('.csv'):
            reader = csv.DictReader(file)
            for row in reader:
                writer.writerow(row)
        elif filename.endswith('.tsv'):
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                writer.writerow(row)
        elif filename.endswith('.json'):
            data = json.loads(file.read())['fields']
            for row in data:
                writer.writerow(row)
        elif filename.endswith('.xml'):
            parsed_file = xmltodict.parse(file.read())
            object_rows = parsed_file['root']['objects']
            # incorrect format of file - objects must be list, not dict
            row = {
                v['@name']: v['value']
                for v in object_rows['object']
            }
            writer.writerow(row)
