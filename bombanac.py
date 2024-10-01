import random
import time

class Minefield:
    def __init__(self, input_size):
        self.size = input_size
        self.field = [[0] * self.size for _ in range(self.size)]
        self.player_field = [['?'] * self.size for _ in range(self.size)]
        self.visited = [[False] * self.size for _ in range(self.size)]
        self.mine_count = self.size * self.size * 15 // 100
        self.first_click = True
        self.clicked_tiles = 0
        random.seed(time.time())


    def place_bombs(self):
        placed_mines = 0

        while placed_mines < self.mine_count:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)

            if self.field[row][col] == 9:
                continue

            self.field[row][col] = 9

            # Increment neighboring cells
            for i in range(1, -2, -1):
                for j in range(-1, 2):
                    if 0 <= row + i < self.size and 0 <= col + j < self.size:
                        if self.field[row + i][col + j] != 9 and not (i == 0 and j == 0):
                            self.field[row + i][col + j] += 1

            placed_mines += 1

    def create_safe_field(self, row, col):
        while True:
            for i in range(self.size):
                for j in range(self.size):
                    self.field[i][j] = 0
                    self.visited[i][j] = False

            self.place_bombs()

            if self.field[row][col] == 0:
                break

    def click(self, row, col):
        if self.first_click:
            self.create_safe_field(row, col)
            self.first_click = False

        rtn = self.reveal(row, col)
        print()
        if rtn == False:
            self.flag_mines()
        self.print_player_field()
        if self.clicked_tiles == self.size*self.size-self.mine_count:
            self.print_happy()
            return False
        if rtn == True:
            self.print_bomb()
        return not rtn

    def reveal(self, row, col):
        self.player_field[row][col] = str(self.field[row][col])

        if self.visited[row][col] == False:
            self.clicked_tiles += 1
        self.visited[row][col] = True
        if self.field[row][col] != 0:
            if self.field[row][col] == 9:
                return True
            return False

        for i in range(1, -2, -1):
            for j in range(-1, 2):
                if 0 <= row + i < self.size and 0 <= col + j < self.size:
                    if not self.visited[row + i][col + j] and self.field[row + i][col + j] != 9 and not (i == 0 and j == 0):
                        self.reveal(row + i, col + j)

        return False

    def flag_mines(self):
        for i in range(self.size):
            for j in range(self.size):
                count = 0
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        if 0 <= i + di < self.size and 0 <= j + dj < self.size:
                            if self.player_field[i + di][j + dj] in ('?', 'F'):
                                count += 1

                if self.player_field[i][j].isdigit() and int(self.player_field[i][j]) == count:
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if 0 <= i + di < self.size and 0 <= j + dj < self.size:
                                if self.player_field[i + di][j + dj] == '?':
                                    self.player_field[i + di][j + dj] = 'F'

    def get_next_move(self):
        if self.first_click:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            print(f"Trying {row},{col} ")
            return row,col

        else:
            for i in range(self.size):
                for j in range(self.size):
                    count = 0
                    for di in range(-1, 2):
                        for dj in range(-1, 2):
                            if 0 <= i + di < self.size and 0 <= j + dj < self.size:
                                if self.player_field[i + di][j + dj] == 'F':
                                    count += 1

                    if self.player_field[i][j].isdigit() and int(self.player_field[i][j]) == count:
                        for di in range(-1, 2):
                            for dj in range(-1, 2):
                                if 0 <= i + di < self.size and 0 <= j + dj < self.size:
                                    if self.player_field[i + di][j + dj] == '?':
                                        print(f"Trying {i+di},{j+dj} ")
                                        return i+di,j+dj
        #Last resort pick a random  "?"
        for i in range(self.size):
            for j in range(self.size):
                if self.player_field[i][j] == '?':
                    print(f"Randomly picking... {i},{j}")
                    return i,j
        return 0,0




    def print_field(self):  # For debugging
        for i in range(self.size):
            for j in range(self.size):
                print(f" {self.field[i][j]} ", end="")
            print()

    def print_player_field(self):  # For normal usage
        print("   | " + "  ".join(map(str, range(self.size))))
        print("_" * self.size * 4)
        for i in range(self.size):
            if i < 10:
                print(f"{i}  |", end="")
            else:
                print(f"{i} |", end="")
            for j in range(self.size):
                if j < 10:
                    print(f" {self.player_field[i][j]} ", end="")
                else:
                    print(f" {self.player_field[i][j]}  ", end="")
                
            print()

    def print_bomb(self):
        print("     _.-^^---....,,--       ")
        print(" _--                  --_  ")
        print("<                        >)")
        print("|                         | ")
        print(" \\._                   _./  ")
        print("    ```--. . , ; .--'''       ")
        print("          | |   |             ")
        print("       .-=||  | |=-.   ")
        print("       `-=#$%&%$#=-'   ")
        print("          | ;  :|     ")
        print("______.,-#%&$@%#&#~,._____")
        print("          I LOST!? ")

    def print_happy(self):
        print('     .-""""""-.')
        print("   .'          '.")
        print("  /   O      O   \\")
        print(" :                :")
        print(" |                |")
        print(" : ',          ,' :")
        print("  \\  '-.____.-'  /")
        print("   '.     U    .'")
        print("     '-......-'")
        print("       I win!")

def main():
    while True:
        invalid = True
        while invalid:
            size_input = input("Enter field size: ")
            try:
                size = int(size_input)
                if size >= 0:
                    invalid = False
                else:
                    size*=-1
                    invalid = False
            except ValueError:
                print("Invalid size..")
        m = Minefield(size)
        m.print_player_field()
        game_not_over = True

        while game_not_over:
            game_not_over = m.click(*m.get_next_move())
    


if __name__ == "__main__":
    main()
