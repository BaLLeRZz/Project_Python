class TicTacToe:
    def __init__(self):
        self.turn = 1
        self.results_file = "results.txt"
        self.rankings_file = "rankings.txt"
        self.rankings = []

    # Printing the board in the terminal
    def print_board(self):
        size = self.board_size * self.board_size
        count = 1
        for i in range(size):
            # Checking whether i is at the last square of the row so it doesnt print |
            if i == self.board_size * count - 1:
                count += 1
                print(f" {self.board[i]}")
                if i != size - 1:
                    # The range of the "-" depends on the number of squares on a row.
                    # We place 3 "-" for each square and 1 for each |
                    for j in range(self.board_size * 3 + self.board_size - 1):
                        print("-", end="")
                    print("\n", end="")
                continue
            print(f" {self.board[i]} |", end="")

    # Checking whether the board is full
    def is_full(self):
        return not ' ' in self.board

    # Check whether the current state of the game results a win
    def is_win(self):
        size = len(self.board)
        count = 0
        # helper -
        # 1) fixing the bug when there are the winning length consequent equal letters,
        #    but one or more of them are on the next line
        # 2) fixing the bug when due to a small sized board, during the subtractions
        #   some letters that are not in a diagonal are taken for comparison for the win
        helper = 1
        for i in range(size):
            if self.board[i] != ' ':
                # Horizontal:
                if i + self.winning_length < size:
                    if all(self.board[i + j] == self.board[i] and i + j < helper * self.board_size for j in range(self.winning_length)):
                        return True
                # Vertical:
                if i + self.board_size * (self.winning_length - 1) < size:
                    if all(self.board[i + j * self.board_size] == self.board[i] for j in range(self.winning_length)):
                        return True
                # Left Diagonal:
                if i + self.board_size * (self.winning_length - 1) + (self.winning_length - 1) < size:
                    if all(self.board[i + j * (self.board_size + 1)] == self.board[i] for j in range(self.winning_length)):
                        return True
                # Right Diagonal:
                if 0 <= i + self.board_size * (self.winning_length - 1) - (self.winning_length - 1) < size:
                    if all(self.board[i + j * (self.board_size - 1)] == self.board[i] and i + j * (self.board_size - 1) > j * helper * self.board_size - 1 for j in range(self.winning_length)):
                        return True
            count += 1
            if count == self.board_size:
                helper += 1
                count = 0
        return False

    def update_rankings(self, winner, loser, is_bot, is_draw):
        # Creating unique dictionaries with player's names as keys and number of wins as values
        self.rankings = []
        try:
            with open(self.rankings_file, 'r') as ranks:
                for line in ranks:
                    name, wins = line.strip().split(" - ")
                    self.rankings.append({"Name": name, "Wins": int(wins)})
        except:
            with open(self.rankings_file, 'w') as ranks:
                if not is_draw:
                    ranks.write(f"{winner} - 1")
                else:
                    ranks.write(f"{winner} - 0")
                if not is_bot:
                    ranks.write(f"{loser} - 0")
        winner_exists = False
        loser_exists = False
        for dict in self.rankings:
            if winner in dict.values():
                winner_exists = True
                if not is_draw:
                    dict["Wins"] += 1
            if loser in dict.values():
                loser_exists = True
        if not winner_exists:
            if not is_draw:
                self.rankings.append({"Name": winner, "Wins": 1})
            else:
                self.rankings.append({"Name": winner, "Wins": 0})
        if not loser_exists and not is_bot:
            self.rankings.append({"Name": loser, "Wins": 0})
        # Sorting the rankings in descending order and writing them to a file
        self.rankings.sort(key=lambda x: x["Wins"], reverse=True)
        with open(self.rankings_file, 'w') as ranks:
            for dict in self.rankings:
                ranks.write(f'{dict["Name"]} - {dict["Wins"]}\n')

    def minimax(self, isMaximizingPlayer, max_depth, turn, bot_letter, player_letter):
        if self.is_win() and turn == 1:
            return 1
        elif self.is_win() and turn == -1:
            return -1
        elif self.is_full() or max_depth == 5: # Change the max_depth here if you want to change the waiting time
            return 0
        if isMaximizingPlayer:
            best_score = -2
            for i in range(self.board_size * self.board_size):
                if self.board[i] == ' ':
                    self.board[i] = bot_letter
                    current_score = self.minimax(False, max_depth + 1, -turn, bot_letter, player_letter)
                    self.board[i] = ' '
                    if current_score > best_score:
                        best_score = current_score
            return best_score
        else:
            best_score = 2
            for i in range(self.board_size * self.board_size):
                if self.board[i] == ' ':
                    self.board[i] = player_letter
                    current_score = self.minimax(True, max_depth + 1, -turn, bot_letter, player_letter)
                    self.board[i] = ' '
                    if current_score < best_score:
                        best_score = current_score
            return best_score

    def one_player(self):
        #Play the game with one player against the bot
        player_name = input("Enter your name: ")
        player_letter = input ("What would you like to play with (X/O)?: ").upper().strip()
        while player_letter != 'X' and player_letter != 'O':
            player_letter = input("Incorrect input! Type 'x' or 'o' to choose side!: ").upper().strip()
        bot_letter = 'O' if player_letter == 'X' else 'X'
        first = input("Would you like to be first (yes/no)?: ").lower().strip()
        while first != "yes" and first != "no":
            first = input("Incorrect input! Type 'yes' or 'no' to determine the turn: ").lower().strip()
        self.print_board()
        self.turn = 1 if first == "yes" else -1
        while not self.is_full():
            if self.turn == 1:
                print(f"{player_name}'s turn!")
                row = int(input("Enter a row: ").strip())
                if row > self.board_size or row < 1:
                    print(f"Incorrect row input! The board size is {self.board_size}x{self.board_size}")
                    continue
                col = int(input("Enter a column: ").strip())
                if col > self.board_size or col < 1:
                    print(f"Incorrect column input! The board size is {self.board_size}x{self.board_size}")
                    continue
                if self.board[(row - 1) * self.board_size + col - 1] != ' ':
                    print("This spot is taken!")
                    continue
                self.board[(row - 1) * self.board_size + col - 1] = player_letter
                self.print_board()
                if self.is_win():
                    print(f"{player_name} is Winner!")
                    with open(self.results_file, 'a') as results:
                        results.write(f"{player_name} won against The Bot as {player_letter}\n")
                    self.update_rankings(player_name, "Bot", True, False)
                    return
                self.turn *= -1
            elif self.turn == -1:
                print("The Bot's turn!")
                best_score = -2
                best_move = 0
                for i in range(self.board_size * self.board_size):
                    if self.board[i] == ' ':
                        self.board[i] = bot_letter
                        score = self.minimax(False, 0, 1, bot_letter, player_letter)
                        self.board[i] = ' '
                        if (score > best_score):
                            best_score = score
                            best_move = i
                self.board[best_move] = bot_letter
                self.print_board()
                if self.is_win():
                    print("The Bot is Winner!")
                    with open(self.results_file, 'a') as results:
                        results.write(f"{player_name} lost against The Bot as {player_letter}\n")
                    return
                self.turn *= -1
        print("The game is a Draw!")
        with open(self.results_file, 'a') as results:
            results.write(f"{player_name} got a draw against The Bot as {player_letter}\n")
        self.update_rankings(player_name, "Bot", True, True)

    def two_players(self):
        player_one_name = input("Enter Player 1's name: ")
        player_two_name = input("Enter Player 2's name: ")
        player_one_letter = input (f"{player_one_name} what would you like to play with (X/O)?: ").upper().strip()
        while player_one_letter != 'X' and player_one_letter != 'O':
            player_one_letter = input("Incorrect input! Type 'x' or 'o' to choose side!: ").upper().strip()
        player_two_letter = 'O' if player_one_letter == 'X' else 'X'
        self.print_board()
        self.turn = 1
        while not self.is_full():
            if self.turn == 1:
                print(f"{player_one_name}'s turn!")
            elif self.turn == 2:
                print(f"{player_two_name}'s turn!")
            row = int(input("Enter a row: ").strip())
            if row > self.board_size or row < 1:
                print(f"Incorrect row input! The board size is {self.board_size}x{self.board_size}")
                continue
            col = int(input("Enter a column: ").strip())
            if col > self.board_size or col < 1:
                print(f"Incorrect column input! The board size is {self.board_size}x{self.board_size}")
                continue
            if self.board[(row - 1) * self.board_size + col - 1] != ' ':
                print("This spot is taken!")
                continue
            if self.turn == 1:
                self.board[(row - 1) * self.board_size + col - 1] = player_one_letter
                self.print_board()
                if self.is_win():
                    print(f"{player_one_name} is Winner!")
                    with open(self.results_file, 'a') as results:
                        results.write(f"{player_one_name} won against {player_two_name} as {player_one_letter}\n")
                    self.update_rankings(player_one_name, player_two_name, False, False)
                    return
                self.turn = 2
            elif self.turn == 2:
                self.board[(row - 1) * self.board_size + col - 1] = player_two_letter
                self.print_board()
                if self.is_win():
                    print(f"{player_two_name} is Winner!")
                    with open(self.results_file, 'a') as results:
                        results.write(f"{player_two_name} won against {player_one_name} as {player_two_letter}\n")
                        self.update_rankings(player_two_name, player_one_name, False, False)
                    return
                self.turn = 1
        print("The game is a Draw!")
        with open(self.results_file, 'a') as results:
            results.write(f"{player_one_name} got a draw against {player_two_name} as {player_one_letter}\n")
        self.update_rankings(player_one_name, player_two_name, False, True)

    def execute(self):
        print("Welcome to the Tic Tac Toe game!\n")
        print("Here is a list of the available commands:\n")
        print("1) Help - Shows the current list of commands.")
        print("2) Play - Starts the game.")
        print("3) Rank - Shows information about all the players and their wins so far.")
        print("4) Score - Shows information about all the games that have been played so far.")
        print("5) Exit - Stops the application.\n")
        command = ""
        while command != "exit":
            command = input("Choose a command: ").lower().strip()
            if command == "help":
                print("Here is a list of the available commands:\n")
                print("1) Help - Shows the current list of commands.")
                print("2) Play - Starts the game.")
                print("3) Rank - Shows information about all the players and their wins so far.")
                print("4) Score - Shows information about all the games that have been played so far.")
                print("5) Exit - Stops the application.\n")
            elif command == "play":
                b_size = int(input("Choose the size of the board (3-10): "))
                while b_size < 3 or b_size > 10:
                    b_size = int(input("Incorrect board size! Choose between 3 and 10!: "))
                self.board_size = b_size
                self.winning_length = 3 if b_size == 3 else 4
                self.board = [' '] * (b_size * b_size)
                player_count = int(input("How many players are going to play (1/2)?: "))
                while player_count != 1 and player_count != 2:
                    player_count = int(input("Incorrect input number! Choose between 1 and 2!: "))
                if player_count == 1:
                    self.one_player()
                elif player_count == 2:
                    self.two_players()
            elif command == "rank":
                try:
                    with open(self.rankings_file, 'r') as ranks:
                        print(ranks.read())
                except:
                    print("The file did not open or is not created yet!\n")
            elif command == "score":
                try:
                    with open(self.results_file, 'r') as results:
                        print(results.read())
                except:
                    print("The file did not open or is not created yet!\n")
            elif command == "exit":
                return
            else:
                print("Invalid command!\n")

game = TicTacToe()
game.execute()
