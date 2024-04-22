import jsonlines
import random
import shutil

def split_train_validate_test(train_file, test_file, train_output, validate_output, test_output, validation_ratio=0.2):
    # Read training data from input JSONL file
    train_data = []
    with jsonlines.open(train_file, 'r') as reader:
        for line in reader:
            train_data.append(line)
    
    # Shuffle the training data
    random.shuffle(train_data)
    
    # Split training data into training and validation sets
    validation_size = int(validation_ratio * len(train_data))
    validation_data = train_data[:validation_size]
    training_data = train_data[validation_size:]
    
    # Write training data to train_output file
    with jsonlines.open(train_output, 'w') as writer:
        for item in training_data:
            writer.write(item)
    
    # Write validation data to validate_output file
    with jsonlines.open(validate_output, 'w') as writer:
        for item in validation_data:
            writer.write(item)
    
    # Copy test data to test_output file
    shutil.copyfile(test_file, test_output)

def reset_and_sort_indices(input_file, output_file):
    # Read data from input JSONL file
    data = []
    with jsonlines.open(input_file, 'r') as reader:
        for line in reader:
            data.append(line)
    
    # Reset idx and sort the data
    for idx, entry in enumerate(data, start=1):
        entry['idx'] = idx
    data.sort(key=lambda x: x['idx'])
    
    # Write data to output JSONL file
    with jsonlines.open(output_file, 'w') as writer:
        for item in data:
            writer.write(item)

# Split and validate the training data
split_train_validate_test('acceptability-train.jsonl', 'acceptability-test.jsonl', 
                          'acceptability-train.jsonl1', 'acceptability-validate.jsonl1', 'acceptability-test1.jsonl', 
                          validation_ratio=0.2)

# Reset and sort indices for all files
reset_and_sort_indices('acceptability-train1.jsonl', 'acceptability-train-updated.jsonl')
reset_and_sort_indices('acceptability-test1.jsonl', 'acceptability-test-updated.jsonl')
reset_and_sort_indices('acceptability-validate1.jsonl', 'acceptability-validate-updated.jsonl')
