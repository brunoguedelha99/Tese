import csv

# Open the CSV file with the open() function
# This returns a file object that you can use to read the data in the file
with open('data.csv', 'r') as csvfile:
    # Create a CSV reader object with the csv.reader() function
    # This will allow us to read the data in the file line by line
    reader = csv.reader(csvfile)

    # Loop through each row in the reader object
    for row in reader:
        # Print each row to the console
        print(row)
