def transpose(a):          #function to transpose
    return list(map(list, zip(*a)))

def restore(filename):      #function to transfrom puzzle into matrix list
    with open(filename,'r') as r:
        matrix1 = []
        for line in r:
            row = []
            for x in line.split():
                row.append(x)
            matrix1.append(row)
        return matrix1
    
from abc import ABC, abstractmethod

class Puzzle(ABC):
    def __init__(self, file_name):
        self.file_name = file_name
    @abstractmethod
    def solve(self): 
        pass

class WordPuzzle(Puzzle):
    def __init__(self, file_name):
        super().__init__(file_name)
        self.wordset = target_word
 
    def solve(self):
        print('\nPuzzle:')
        with open(self.file_name, 'r') as f: 
            next(f)  #skip first line
            for line in f.readlines():
                print(line, end='')  #print puzzle   
        print('\nWords found:')  
        matrix = restore(self.file_name)[1:]    #remove first line in file
        indices = []    #get the word indices in the puzzle
        for row in matrix:
            my_str = ''.join(row)      #turn list into string
            for target in target_word:
                try:
                    location = my_str.index(target) #Throws ValueError if target not in my_str
                    for y in range(location,location+len(target)):
                        indices.append(( matrix.index(row), y ))  #get each index of the words 
                    print(f'row {matrix.index(row)}: {target}')                 
                except ValueError:
                    pass # line skipped if ValueError
        for col in transpose(matrix):
            my_str = ''.join(col)
            for target in target_word:
                try:
                    location = my_str.index(target) #Throws ValueError if target not in my_str
                    for x in range(location,location+len(target)):
                        indices.append((x, transpose(matrix).index(col)))   #get each index of the words          
                    print(f'col {transpose(matrix).index(col)}: {target}')
                except ValueError:
                    pass  #line skipped if ValueError
        print('\nPuzzle solved:')
        for (x, y) in indices:              #capitilze the words in vocab
            matrix[x][y] = matrix[x][y].upper()
        for line in matrix: 
            print(' '.join(line))
        print()

class MathPuzzle(Puzzle):
    def __init__(self, file_name):
        super().__init__(file_name)

    def solve(self):
        print('\nPuzzle:')
        with open(self.file_name, 'r') as f: 
            next(f)                  #skip first line
            for line in f.readlines():
                print(line, end='')  #print puzzle          
        row_s, col_s = restore(self.file_name)[0][0], restore(self.file_name)[0][1]
        row, col = int(row_s), int(col_s)           #turn row and column into integer
        only_num = restore(self.file_name)[1:]    #remove first line in file
        grid = [[int(x) for x in lst] for lst in only_num]   #turn string list into integer
        hor_max, ver_max, dr_max, dl_max = 0, 0, 0, 0
        h_row, h_col, v_row, v_col, dr_row, dr_col, dl_row, dl_col = 0, 0, 0, 0, 0, 0, 0, 0
        for i in range(row):          #find horizontal             
            for j in range(col-3):
                hor_product = grid[i][j] * grid[i][j+1] * grid[i][j+2] * grid[i][j+3]
                index_row, index_col = i , j
                if hor_product > hor_max:
                    hor_max = hor_product
                    h_row, h_col = index_row, index_col 
        best_h = (hor_max, h_row, h_col)
        for i in range(col):          #find vertical
            for j in range(row-3):
                ver_product = grid[j][i] * grid[j + 1][i] * grid[j + 2][i] * grid[j+3][i]
                index_row, index_col = j , i
                if ver_product > ver_max:
                    ver_max = ver_product
                    v_row, v_col = index_row, index_col
        best_v = (ver_max, v_row, v_col)
        for k in range(row-3):        #find diaginal-right
            for l in range(col-3):
                diag_right_product = grid[k][l] * grid[k + 1][l + 1] * grid[k + 2][l + 2] * grid[k + 3][l + 3]
                index_row, index_col = k , l
                if diag_right_product > dr_max:
                    dr_max = diag_right_product
                    dr_row, dr_col = index_row, index_col
        best_dr = (dr_max, dr_row, dr_col)
        for k in range(row-3):        #find diaginal-left
            for l in range(col-3):
                diag_left_product = grid[k][l + 3] * grid[k + 1][l + 2] * grid[k + 2][l + 1] * grid[k + 3][l]
                index_row, index_col = k , l + 3
                if diag_left_product > dl_max:
                    dl_max = diag_left_product
                    dl_row, dl_col = index_row, index_col
        best_dl = (dl_max, dl_row, dl_col)
        tuplelist = [best_v, best_h, best_dr, best_dl] 
        best = (0,0,0)                #desired tuple of max value, index row, index col  
        for item in tuplelist:        #compare the max value from all four directions  
          if item[0]>best[0]:
            best = item
        print('\nPuzzle solved:\n', best, '\n')

import os.path
from os import path


try:    
    dic_file = str(input('Enter dictionary file name: '))
    if dic_file.endswith(".txt"):
        dict1 =[] #word list in chosen dictionary file
        with open(dic_file,'r') as reader:
            for line in reader:
                for x in line.split():
                    dict1.append(x)
        total_words = dict1[0]
        longest_word = dict1[1] # length of the longest word 
        del dict1[0], dict1[1]
        target_word = [i for i in dict1 if 3 <=  len(i)] #remove words less than 3 characters in word list
        print (f'Dictionary loaded with {total_words} words')
        while True:    
            puzz_file = str(input('Enter puzzle file name: '))
            if puzz_file.endswith(".txt") and path.exists(puzz_file):
                if puzz_file.startswith('word'):
                    wp = WordPuzzle(puzz_file)
                    wp.solve()
                elif puzz_file.startswith('math'):
                    mp = MathPuzzle(puzz_file)
                    mp.solve()
            elif not puzz_file.endswith(".txt"): 
                print(f'Failed to open file {puzz_file}')
                break
            elif FileNotFoundError:
                print(f"Couldn't find {puzz_file}")
                break
            ok = input('Continue with next puzzle? (y/n):')
            while ok.lower() not in ('y', 'n'):
                ok = input('Continue with next puzzle? (y/n):')
            if ok.lower() == ('y'):
                continue 
            if ok.lower() == ('n'):
                break
    else:
        print(f'Failed to open file {dic_file}')
except FileNotFoundError:
    print(f"Couldn't find {dic_file}")