import csv

write_data = []
with open('topic_classification.txt', 'r') as f:
    while True:
    #for i in range(10):
        read_data = f.readline()
        if read_data == "-------------------------\n":
            review = ''
            #for i in range(100):
            while True:
                read_data = f.readline()
                #print(read_data)
                if read_data == 'delete\n' or read_data == '--------------------------------------------------\n':
                    break
                elif read_data.startswith('p,'):
                    write_data.append([review, 1])
                    break
                elif read_data.startswith('n,'):
                    write_data.append([review, 0])
                    break
                else:
                    review = review + read_data 
        elif read_data == '----------------------------------------------------------------------------------------------------':
            break
        else:
            print(read_data)
f.close()

with open('topic_classification_less_5.txt', 'r') as f:
    while True:
    #for i in range(10):
        read_data = f.readline()
        if read_data == "-------------------------\n":
            review = ''
            #for i in range(100):
            while True:
                read_data = f.readline()
                #print(read_data)
                if read_data == 'delete\n' or read_data == '--------------------------------------------------\n':
                    break
                elif read_data.startswith('p,'):
                    write_data.append([review, 1])
                    break
                elif read_data.startswith('n,'):
                    write_data.append([review, 0])
                    break
                else:
                    review = review + read_data 
        elif read_data == '----------------------------------------------------------------------------------------------------':
            break
        else:
            print(read_data)
f.close()

header = ['text', 'sentiment']
with open('sentiment.csv', 'w', newline='') as f:
    writer=csv.writer(f)
    writer.writerow(header)
#    print(write_data)
    writer.writerows(write_data)
f.close()

