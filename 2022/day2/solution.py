ROCK_SCORE = 1
PAPER_SCORE = 2
SCISSOR_SCORE = 3

LOST_SCORE = 0
DRAW_SCORE = 3
WIN_SCORE = 6

class Player():
    def __init__(self, rock, paper, scissor):
        self.play = {
            rock: "Rock",
            paper: "Paper",
            scissor: "Scissor"
        }

def parse_row_first_puzzle(dirty_row):
    cleaned_row = dirty_row.strip()
    opponent_play = opponent.play[cleaned_row[0]]
    your_play = you.play[cleaned_row[2]]
    return opponent_play, your_play

def parse_row_second_puzzle(dirty_row):
    cleaned_row = dirty_row.strip()
    opponent_play = opponent.play[cleaned_row[0]]
    match cleaned_row[2]:
        case "X":
            outcome = "lost"
        case "Y":
            outcome = "draw"
        case "Z":
            outcome = "win"
    return opponent_play, outcome

def derive_play(opponent_play, outcome):
    outcome_check = {
        "Rock" : ["Scissor", "Paper"],
        "Paper" : ["Rock", "Scissor"],
        "Scissor" : ["Paper", "Rock"]
    }
    match outcome:
        case "win":
            return outcome_check[opponent_play][1]
        case "draw":
            return opponent_play
        case "lost":
            return outcome_check[opponent_play][0]
        case _ :
            raise Exception("You shouldnt get here")


def calc_shape_score(play):
    # The score for a single round is the score for the shape
    match play:
        case "Rock":
            return ROCK_SCORE
        case "Paper":
            return PAPER_SCORE
        case "Scissor":
            return SCISSOR_SCORE

def calc_outcome_score(opponent_play, your_play):
    # plus the outcome for the round:
    # lost = 0
    # draw = 3
    # won = 6
    if opponent_play == your_play:
        return DRAW_SCORE
    match your_play, opponent_play:
        case "Rock", "Scissor":
            return WIN_SCORE
        case "Paper", "Rock":
            return WIN_SCORE
        case "Scissor", "Paper":
            return WIN_SCORE
        case _ :
            return LOST_SCORE

def print_round(index, your_play, opponent_play, shape_score, outcome_score):
    print(f"# ROUND {index + 1} #")
    print(f"You play: {your_play}, opponent plays: {opponent_play}")
    print(
        f"shape {shape_score} + "
        f"outcome {outcome_score} = "
        f"{round_score}"
    )


if __name__ == "__main__":
    print_rounds = 0

    print("\n\n##### PUZZLE 1 #####")    
    # puzzle 1
    # X means Rock, 
    # Y means Paper,
    # Z means Scizzor
    opponent = Player("A", "B", "C")
    you = Player("X", "Y", "Z")
    
    # Total score is the sum of your shape and outcome score for each round
    total_score = 0
    with open("input.txt", "r") as f:
        for index, row in enumerate(f):
            round_score = 0              
            opponent_play, your_play = parse_row_first_puzzle(row)
            shape_score = calc_shape_score(your_play)
            outcome_score = calc_outcome_score(opponent_play, your_play)
            round_score = shape_score + outcome_score
            if index < print_rounds:
                print_round(
                    index,
                    your_play,
                    opponent_play,
                    shape_score,
                    outcome_score
                )
            total_score += round_score
    
    print("###TOTAL SCORE PUZZLE 1###")
    print(total_score)

    print("\n\n##### PUZZLE 2 #####")
    # puzzle 2
    # X means you need to lose, 
    # Y means you need to end the round in a draw, and 
    # Z means you need to win.

    total_score_puzzle_two = 0
    with open("input.txt", "r") as f:
        for index, row in enumerate(f):
            round_score = 0              
            opponent_play, outcome = parse_row_second_puzzle(row)
            your_play = derive_play(opponent_play, outcome)
            shape_score = calc_shape_score(your_play)
            outcome_score = calc_outcome_score(opponent_play, your_play)
            round_score = shape_score + outcome_score
            total_score_puzzle_two += round_score
            if index < print_rounds:
                print_round(
                    index,
                    your_play,
                    opponent_play,
                    shape_score,
                    outcome_score
                )
   
    print("###TOTAL SCORE PUZZLE 2###")
    print(total_score_puzzle_two)
