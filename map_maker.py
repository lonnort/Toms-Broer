import csv as c
import re


def matrix_maker():
    with open(r"maps/mapmatrix03v3.txt", "r") as map:
        reader = c.reader(map)
        matrix = list()
        i = 1
        for row in reader:
            i+= 1
            #print(i)
            #print(row[0])
            beter = row[0].replace(" ", '0')
            beter = re.sub('[^0-9]', '1', beter)
            beter = row[0].replace("\t", ",")
            print(beter)
            #beter = row.replace("")
            matrix.append(beter)
    return matrix


def matrix_writer():
    matrix = matrix_maker()
    with open(r"maps/mapmatrix04v3.txt", "w") as write_map:
        writer = c.writer(write_map)
        for i in matrix:
            writer.writerow(i)

    print(matrix)

def debug_listmaker():
    with open(r"debug.txt", "r") as debug:
        reader = c.reader(debug)
        inlist = list()
        i = 0
        for row in reader:
            inlist.append(row)



def matrix_reader():
    with open(r"maps/mapmatrix03v3.txt", "r") as map:
        reader = c.reader(map)
        matrix = list()
        i = 0
        for row in reader:
            i += 1
            new_row = list()
            for x in row:
                new_row.append(int(x))
            #print(i)
            #addition = [e for e in row if e]
            #print(addition)
            matrix.append(list(new_row))
    better = [e for e in matrix if e]
    #print(better[15][80])
    return(better)

#matrix_maker()
matrix_writer()
#print(matrix_reader())