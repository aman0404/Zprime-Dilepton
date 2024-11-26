import sys

# Function to filter the rows based on Lambda values
def filter_rows(file_path, lambda_values):
    filtered_rows = []
    with open(file_path, 'r') as file:
        for line in file:
            lambda_value, limit = map(float, line.split())
            if int(lambda_value) in lambda_values:
                filtered_rows.append(line.strip())
    return filtered_rows

# Main function to handle command-line arguments and process files
def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <file1> <file2> <output_file>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_file_path = sys.argv[3]

    # Lambda values to keep from each file
    lambda_values_file1 = {4, 6, 8, 10}
    lambda_values_file2 = {14, 18}

    # Filter rows from both files
    filtered_rows_file1 = filter_rows(file1_path, lambda_values_file1)
    filtered_rows_file2 = filter_rows(file2_path, lambda_values_file2)

    # Combine the filtered rows and write them to a new file
    with open(output_file_path, 'w') as output_file:
        for row in filtered_rows_file1 + filtered_rows_file2:
            output_file.write(f"{row}\n")

    print(f"Filtered rows have been written to {output_file_path}.")

if __name__ == "__main__":
    main()

