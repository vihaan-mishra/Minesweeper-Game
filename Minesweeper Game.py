#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import messagebox
import random

class MinesweeperCell(Label):
    def __init__(self, master, row, col):
        super().__init__(master, font=('Arial', 12, 'bold'), width=4, height=2, bg='lightgrey', relief=RAISED)
        self.master = master
        self.row = row
        self.col = col
        self.is_bomb = False
        self.is_revealed = False
        self.flagged = False
        self.bind("<Button-1>", self.reveal_cell)
        self.bind("<Button-2>", self.toggle_mark)

    def reveal_cell(self, event=None):
        if self.is_revealed == True or self.flagged == True:
            return
        self.is_revealed = True
        if self.is_bomb == True:
            self.config(text='*', relief=RAISED)
            messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
            self.master.reveal_all_bombs()      
            self.master.disable_cells()
        else:
            num_nearby_bombs = self.master.num_nearby_bombs(self.row, self.col)
            if num_nearby_bombs != 0:
                self.config(text=str(num_nearby_bombs), relief=SUNKEN, bg='lightgrey', fg=self.num_color(num_nearby_bombs))
            else:
                self.config(relief=SUNKEN)
                self.master.reveal_adj_cells(self.row, self.col)
            self.master.check_win()
            
    def toggle_mark(self, event=None):
        if not self.is_revealed:
            self.flagged = not self.flagged
            self.config(text='*')
            if self.flagged == True:
                self.master.flags += 1
            else: 
                self.master.flags - 1
            self.master.update_bomb_counter()
        
    def num_color(self, num):
        colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        return colormap[num]
        
class MinesweeperBoard(Frame):
    def __init__(self, master, row, column, numBombs):
        super().__init__(master)
        self.master = master
        self.row = row
        self.column = column
        self.numBombs = numBombs
        self.flags = 0
        self.cells = {}
        self.create_widget()
        self.create_board()
        
    def create_widget(self):
        self.bomb_counter = Label(self.master, text='Bombs left ' + str(self.numBombs), font=('Arial', 12, 'bold'))
        self.bomb_counter.pack()
    
    def update_bomb_counter(self):
        bombs_left = self.numBombs - self.flags
        self.bomb_counter.config(text=bombs_left)        
        
    def create_board(self):
        for r in range(self.row):
            for c in range(self.column):
                cell = MinesweeperCell(self, r, c)
                cell.grid(row = r, column = c)
                self.cells[(r, c)] = cell 
        self.place_bomb()        
                
    def place_bomb(self):
        bombCoord = random.sample(self.cells.keys(), self.numBombs)
        for bomb in bombCoord:
            self.cells[bomb].is_bomb = True
            
    def num_nearby_bombs(self, row, column):
        count = 0
        for r in range(max(0, row - 1), min(self.row, row + 2)):
            for c in range(max(0, column - 1), min(self.column, column + 2)):
                if (row, column) != (r, c) and self.cells[(r, c)].is_bomb:
                    count += 1
        return count
        
    def reveal_adj_cells(self, row, column):
        for r in range(max(0, row -1), min(self.row, row+2)):
            for c in range(max(0, column - 1), min(self.column, column + 2)):
                cell = self.cells[(r, c)]
                if not cell.is_bomb and not cell.is_revealed:
                    cell.reveal_cell()        
        
    def check_win(self):
        for cell in self.cells.values():
            if not cell.is_bomb and not cell.is_revealed:
                return False
        messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)
        self.disable_cells()
        
    def reveal_all_bombs(self):
        for cell in self.cells.values():
            if cell.is_bomb == True:
                cell.config(text='*', relief=RAISED, bg='red', fg='black')
        
    def disable_cells(self):
        for cell in self.cells.values():
            cell.config(state='disabled')

def play_minesweeper(rows, columns, numBombs):
    grid = Tk()
    grid.title("Minesweeper")
    board = MinesweeperBoard(grid, rows, columns, numBombs)
    board.pack()
    grid.mainloop()

play_minesweeper(12, 10, 15)


# In[ ]:





# In[ ]:




