import csv

def save_to_file(data_table):
  file = open("jobs.csv", mode ="w")
  writer = csv.writer(file)
  writer.writerow(list(data_table[0].keys()))
  for row in data_table:
    writer.writerow(list(row.values()))
  return