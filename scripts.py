import json
import re
def check_mean_interval(mean_value):
    # Define the intervals and corresponding labels for the correct answer
    intervals = [(1, 2.5), (2.5, 4.5), (4.5, 6), (6, float('inf'))]
    # 4 labeals for each one of four choices
    labels = [0, 1, 2, 3]
    
    # Checks which interval the mean_value belongs to and return the corresponding label
    for interval, label in zip(intervals, labels):
        if mean_value >= interval[0] and mean_value < interval[1]:
            return label
    return None

def create_dataset(tsv_file, jsonl_file, columns_to_convert, column_mapping, choices, encoding='utf-8'):
    counter_id=1

    with open(tsv_file, 'r', encoding=encoding) as tsvfile, open(jsonl_file, 'w') as jsonlfile:
        # The first line contains headers for each feature: mean, N, sd, se, Reference, task
        headers = tsvfile.readline().strip().split('\t')
        column_indices = [headers.index(column) for column in columns_to_convert]
        # Start numbering for 'id' column from 1
        id_counter = 1
        for line in tsvfile:
            data = line.strip().split('\t')
            record = {}
            for i, column_index in enumerate(column_indices):
                original_column_name = columns_to_convert[i]
                new_column_name = column_mapping.get(original_column_name, original_column_name)
                if original_column_name == 'id':
                    record[new_column_name] = str(id_counter)  # Convert to string for consistency with JSON
                    id_counter += 1
                else:
                    record[new_column_name] = data[column_index]
            
            # Calculate the label based on the mean value
            mean_value = float(record['mean'])
            record['label'] = check_mean_interval(mean_value)
            record['text'] = re.sub(r'[^\x00-\x7F]+', '', record['text'])
            # Create a new dictionary with only 'id', 'text', 'choices', and 'label' fields
            reduced_record = {
                'id': counter_id,
                'text': record['text'],  # 'sentence' instead of 'text'
                'label': record['label']
            }
            counter_id+=1

            # Write the reduced record to the JSONL file
            jsonlfile.write(json.dumps(reduced_record) + '\n')
            
# Run the function for each dataset
create_dataset('ACCEPT-Corpus-training.tsv', 'acceptability-train.jsonl', ['id','mean', 'sentence'], {'id': 'id', 'sentence': 'text'}, ['Scarsa', 'Buona','Ottima', 'Eccellente'], encoding='utf-8')
create_dataset('acceptability-set-test.tsv', 'acceptability-test.jsonl', ['id','mean', 'sentence'], {'id': 'id', 'sentence': 'text'}, ['Scarsa', 'Buona', 'Ottima', 'Eccellente'], encoding='utf-8')
create_dataset('COMPL-Corpus-training.tsv', 'complexity-train.jsonl', ['id','mean', 'sentence'], {'id': 'id', 'sentence': 'text'}, ['Basa', 'Moderata', 'Alta', 'Massima'], encoding='utf-8')
create_dataset('complexity-set-test.tsv', 'complexity-test.jsonl' , ['id','mean', 'sentence'], {'id': 'id', 'sentence': 'text'}, ['Basa', 'Moderata', 'Alta', 'Massima'], encoding='utf-8')
