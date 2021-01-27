import csv
from sys import argv, exit
from cs50 import get_string
import re


# check for 2 command line arguments
if len(argv) != 3:
    print("Missing arguments")
    exit(1)


#  DNA database
file_database = argv[1]

with open(file_database, 'r', newline = "") as csvfile:
    database = csv.reader(csvfile, delimiter=',')
# List with items from header of CSV file
    header = next(database)
    database_list = list(database)

#Lista de pessoas sem o header


#  DNA sequence investigated
file_sequence = argv[2]
with open(file_sequence, 'r') as sequence_file:
    sequence = (sequence_file.read())
# A sequencia investigada esta correta

current_count = []
max_count = []
snippets = []

for x in range(1, len(header)):
    snippets.append(header[x])
# A lista de snippets esta correta


for i in range(len(sequence)):
    final = 0 # final count to be appended to max_count array at the end of each iteration
    temp = 0
    first = sequence.find(snippets[i])
    if first < 0:
        max_count.append(0)
        break
    else:
        while sequence[first:first+len(snippets[i])] == snippets[i]:
            temp += 1
            first += len(snippets[i])
        if temp > final:
            final = temp
    max_count.append(final)
print(final)
print(temp)
print(max_count)



#     for j in range(len(sequence)):
#         if sequence[j:j+len(snippets[i])] == snippets[i]:
#             final += 1
#             while sequence[j + len(snippets[i]) + 1 : j + 2 * (len(snippets[i])) + 1] == snippets[i] and sequence[j + 2 * (len(snippets[i])) + 2 : j + 2 * (len(snippets[i])) + 1] == snippets[i]:
#                 temp+=1
#                 if temp > final:
#                     final = temp
#             else:
#                 temp = 0

#     max_count.append(final)

# print(max_count)
# print(temp)
# print(final)


# for i in range(len(sequence)):
#     if sequence[i:i+len(snippets[k])] == snippets[k]:
#         current_count[k] = 1
#         max_count[k] = 1
#         while(sequence[i + len(snippets[k]) + 1 : i + 2 * len(snippets[k]) + 1] == snippets[k]):
#             current_count[k] += 1
#         if current_count[k] > max_count[k]:
#             max_count[k] = current_count[k]
# print(max_count)

# for i in range(len(database_list)):
#     match = True
#     final = 0
#     for j in range(1, len(header)):
#         if int(database_list[i][j]) is not max_count[j-1]:
#             match = match & False
#         if match == True:
#             print(database_list[i][0])
#         else:
#             final += 1
#             if final == (len(database_list))-1:
#                     print("No match")











