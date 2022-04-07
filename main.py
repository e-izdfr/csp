from time import time
from Binairo import *
from Cell import *
from State import *
import random
## w b

def main():
    input_numbers = []  ## first row = size of puzzle(n)  ## second row = number of cells that have color in the statrt  (m)  ## row 3 to row 3+m : 
    input = open('input2.txt').readlines()
    for line in input:
        line = line.rstrip()
        numbers = line.split(' ')
        n = [int(number) for number in numbers]
        input_numbers.append(n)

    board = []
    size_puzzle = input_numbers[0][0]
    for i in range(0, size_puzzle):
        row = []
        for j in range(0, size_puzzle):
            cell = Cell(i, j)
            row.append(cell)
        board.append(row) 
   
    for i in range(2, len(input_numbers)):
        if input_numbers[i][2] == 0: # w
            board[input_numbers[i][0]][input_numbers[i][1]].value = 'W'
            board[input_numbers[i][0]][input_numbers[i][1]].domain = ['n']

        if input_numbers[i][2] == 1:  # b
            board[input_numbers[i][0]][input_numbers[i][1]].value = 'B'
            board[input_numbers[i][0]][input_numbers[i][1]].domain = ['n']
       
    state = State(size_puzzle, board)  
    print('initial board:')
    state.print_board()
    start_time = time()
    
    def Whether_len_is_1_or_not(cell):
        return len(cell.domain) == 1 and cell.value == '_'
    
    def Whether_len_is_2_or_not(cell):
        return len(cell.domain) == 2 and cell.value == '_'
    
    def MRV(state):
        list_of_1s = []
        list_of_2s = []
        for row in state.board:
            list_of_1s += list(filter(Whether_len_is_1_or_not, row))
        if list_of_1s != []:
            rand_int = random.randint(0, len(list_of_1s - 1))
            return list_of_1s[rand_int]
        for row in state.board:
            list_of_2s += list(filter(Whether_len_is_2_or_not, row))
        if list_of_2s != []:
            rand_int = random.randint(0, len(list_of_2s - 1))
            return list_of_2s[rand_int]
        return 'failure'
    
    def find_empty_cells(state):
        empty_cells = []
        for row in state.board:
            for cell in row:
                if cell.value == '_':
                    empty_cells.append(cell)
        return empty_cells
    
    def is_consistant2(var, cell, state):
        if cell.x != var.x:
            if state.board[cell.x][var.y].value.upper() == var.value.upper():
                key = 0
                for j in range(var.y) + range(var.y + 1, state.size):
                    if state.board[cell.x][j].value.upper() != state.board[var.x][j].upper() or state.board[cell.x][j] == '_':
                        key = 1
                        break
                    
                if key == 0:
                    return False
            if cell.y != var.y:
                if state.board[var.x][cell.y].value.upper() == var.value.upper():
                    key = 0
                    for i in range(var.x) + range(var.x + 1, state.size):
                        if state.board[i][cell.y].value.upper() != state.board[i][var.y].upper() or state.board[i][cell.y] == '_':
                            key = 1
                            break
                        
                    if key == 0:
                        return False
            
            else:
                num_white_circles = 0
                num_black_circles = 0
                
                for i in range(0, state.size):
                    if(state.board[i][var.y].value.upper() == 'W'):
                        num_white_circles += 1
            
                    if(state.board[i][var.y].value.upper() == 'B'):
                        num_black_circles += 1
                        
                if num_white_circles > state.size / 2 or num_black_circles > state.size / 2:
                    return False
                
                if cell.x == var.x - 2:
                    if state.board[cell.x][var.y].value.upper() == state.board[var.x - 1][var.y].upper() and \
                    state.board[var.x - 1][var.y].upper() == var.value.upper():
                        return False
                
                elif cell.x == var.x - 1:
                    if((state.board[var.x - 2][var.y].value.upper() == state.board[cell.x][var.y].upper() and \
                        state.board[cell.x][var.y].upper() == var.value.upper()) or (state.board[cell.x][var.y].upper() == \
                            var.value.upper() and var.value.upper() == state.board[var.x + 1][var.y].value.upper())):
                        return False
                
                elif cell.x == var.x + 1:
                    if((state.board[var.x - 1][var.y] == var.value.upper() and var.value.upper() == \
                        state.board[cell.x][var.y].value.upper()) or (var.value.upper() == state.board[cell.x][var.y].value.upper() \
                            and state.board[cell.x][var.y].value.upper() == state.board[var.x + 2][var.y].value.upper())):
                        return False
                
                elif cell.x == var.x + 2:
                    if(var.value.upper() == state.board[var.x + 1][var.y].value.upper() and \
                        state.board[var.x + 1][var.y].value.upper() == state.board[cell.x][var.y].upper()):
                        return False
                        
        else:
            key = 0
            for i in range(var.x) + range(var.x + 1, state.size):
                if state.board[i][cell.y].value.upper() != state.board[i][var.y].upper() or state.board[i][cell.y] == '_':
                    key = 1
                    break
                
            if key == 0:
                return False
            
            num_white_circles = 0
            num_black_circles = 0
            
            for j in range(0, state.size):
                if(state.board[var.x][j].value.upper() == 'W'):
                    num_white_circles += 1
            
                if(state.board[var.x][j].value.upper() == 'B'):
                    num_black_circles += 1
                        
            if num_white_circles > state.size / 2 or num_black_circles > state.size / 2:
                return False
            
            if cell.y == var.y - 2:
                if state.board[var.x][cell.y].value.upper() == state.board[var.x][var.y - 1].upper() and \
                    state.board[var.x][var.y - 1].upper() == var.value.upper():
                        return False
                
            elif cell.y == var.y - 1:
                if((state.board[var.x][var.y - 2].value.upper() == state.board[var.x][cell.y].upper() and \
                    state.board[var.x][cell.y].upper() == var.value.upper()) or (state.board[var.x][cell.y].upper() == \
                        var.value.upper() and var.value.upper() == state.board[var.x][var.y + 1].value.upper())):
                    return False
                
            elif cell.y == var.y + 1:
                if((state.board[var.x][var.y - 1] == var.value.upper() and var.value.upper() == \
                    state.board[var.x][cell.y].value.upper()) or (var.value.upper() == state.board[var.x][cell.y].value.upper() and \
                        state.board[var.x][cell.y].value.upper() == state.board[var.x][var.y + 2].value.upper())):
                    return False
                
            elif cell.y == var.y + 2:
                if(var.value.upper() == state.board[var.x][var.y + 1].value.upper() and state.board[var.x][var.y + 1].value.upper() == \
                    state.board[var.x][cell.y].upper()):
                    return False
                
        return True
    
    def LCV(var, state):
        if len(var.domain) == 1:
            return var.domain[0]
        
        num_of_constraint_violations = []
        for value in var.domain:
            var.value = value
            
            count = 0
            for cell in find_empty_cells(state):
                for v in cell.domain:
                    cell.value = v
                    if not is_consistent2(state):
                        count += 1    
                cell.value = '_'
            num_of_constraint_violations.append(count)
        
        if num_of_constraint_violations[0] > num_of_constraint_violations[1]:
            return var.domain[1]
        
        elif num_of_constraint_violations[0] < num_of_constraint_violations[1]:
            return var.domain[0]
        
        return var.domain[random.randint(1)]
            
    def backTrack(state):  #implement backTrack and other csp functions in Binairo.py
        if check_termination(state):
            state.print_board()
        
        else:
            var = MRV(state)
            if var == 'failure':
                return 'failure'
            
            value = LCM(var, State)
            var.value = value
            if is_consistent(state):
                pass
            
            try:
                var.value = var.domain[1 - var.domain.index(value)]
                if is_consistent(state):
                    pass
                
                var.value = '_'
                return 'failure'
                
            except:
                var.value ='_'
                return 'failure'
            
    list_of_deletions = [[] for i in range(size_puzzle**2)]
    end_time = time()
    print('time: ',end_time-start_time)

if __name__ == '__main__':
    main() 