import time
import tkinter as tk
from tkinter import messagebox
import random

class SudokuSolverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [row[:] for row in self.grid]
        self.cells = []
        self.solving = False
        self.create_grid()

        solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=0, columnspan=3, pady=20)

        reset_button = tk.Button(self.master, text="Reset", command=self.reset_grid)
        reset_button.grid(row=9, column=3, columnspan=3, pady=20)
        
        new_puzzle_button = tk.Button(self.master, text="New Puzzle", command=self.generate_new_puzzle)
        new_puzzle_button.grid(row=9, column=6, columnspan=3, pady=20)

    def create_grid(self):
        for i in range(9):
            row_cells = []
            for j in range(9):
                frame = tk.Frame(self.master, highlightbackground="black", highlightthickness=1)
                if (i + 1) % 3 == 0 and i != 8:
                    frame.grid(row=i, column=j, padx=(1, 1), pady=(1, 3))
                elif (j + 1) % 3 == 0 and j != 8:
                    frame.grid(row=i, column=j, padx=(1, 3), pady=(1, 1))
                else:
                    frame.grid(row=i, column=j, padx=1, pady=1)

                entry = tk.Entry(frame, width=2, font=('Arial', 18), justify='center', borderwidth=2, relief="solid")
                entry.pack()
                row_cells.append(entry)
            self.cells.append(row_cells)

    def get_user_input(self):
        new_grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[i][j].get().strip()
                if value == '':
                    row.append(0)
                elif value.isdigit() and 1 <= int(value) <= 9:
                    row.append(int(value))
                else:
                    messagebox.showerror("Invalid Input", "Please enter numbers between 1 and 9.")
                    return None
            new_grid.append(row)
        return new_grid

    def update_grid(self, row, col, num):
        if num == 0:
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].config(bg="white")
        else:
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].insert(0, str(num))
            self.cells[row][col].config(bg="lightgreen")
        self.master.update()

    def solve(self):
        if self.solving:
            return
        self.grid = self.get_user_input()
        if self.grid is None:
            return
        self.solving = True
        if self.solve_sudoku(self.grid, 0, 0):
            print("Solved Sudoku!")
        else:
            messagebox.showerror("No Solution", "This Sudoku puzzle cannot be solved.")
        self.solving = False

    def is_valid_move(self, grid, row, col, number):
        for x in range(9):
            if grid[row][x] == number or grid[x][col] == number:
                return False
        corner_row = row - row % 3
        corner_col = col - col % 3
        for x in range(3):
            for y in range(3):
                if grid[corner_row + x][corner_col + y] == number:
                    return False
        return True

    def solve_sudoku(self, grid, row, col):
        if not self.solving:
            return False
        if row == 9:
            return True
        if col == 9:
            return self.solve_sudoku(grid, row + 1, 0)
        if grid[row][col] > 0:
            return self.solve_sudoku(grid, row, col + 1)
        for num in range(1, 10):
            if self.is_valid_move(grid, row, col, num):
                grid[row][col] = num
                self.update_grid(row, col, num)
                time.sleep(0.05)
                if self.solve_sudoku(grid, row, col + 1):
                    return True
            grid[row][col] = 0
            self.update_grid(row, col, 0)
        return False

    def reset_grid(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solving = False
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(state='normal')
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(bg="white")

    def generate_new_puzzle(self):
        if self.solving:
            return
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku_no_display(self.grid, 0, 0)
        self.remove_numbers(40)
        self.original_grid = [row[:] for row in self.grid]
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(state='normal')
                self.cells[i][j].delete(0, tk.END)
                if self.grid[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.grid[i][j]))
                    self.cells[i][j].config(state='disabled')
                else:
                    self.cells[i][j].config(bg="white")

    def solve_sudoku_no_display(self, grid, row, col):
        if row == 9:
            return True
        if col == 9:
            return self.solve_sudoku_no_display(grid, row + 1, 0)
        if grid[row][col] > 0:
            return self.solve_sudoku_no_display(grid, row, col + 1)
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid_move(grid, row, col, num):
                grid[row][col] = num
                if self.solve_sudoku_no_display(grid, row, col + 1):
                    return True
            grid[row][col] = 0
        return False

    def remove_numbers(self, num_remove):
        count = 0
        while count < num_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                count += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
