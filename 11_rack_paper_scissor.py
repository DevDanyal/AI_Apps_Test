import random

def get_computer_choice():
    """Randomly selects between rock, paper, and scissors."""
    return random.choice(['rock', 'paper', 'scissors'])

def get_winner(player_choice, computer_choice):
    """Determines the winner of a round."""
    if player_choice == computer_choice:
        return 'tie'
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'scissors' and computer_choice == 'paper') or \
         (player_choice == 'paper' and computer_choice == 'rock'):
        return 'player'
    else:
        return 'computer'

def main():
    """Main function to run the game."""
    player_score = 0
    computer_score = 0
    
    print("Welcome to Rock, Paper, Scissors!")

    while True:
        player_choice = input("Enter your choice (rock, paper, or scissors): ").lower()
        while player_choice not in ['rock', 'paper', 'scissors']:
            player_choice = input("Invalid choice. Please enter rock, paper, or scissors: ").lower()

        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")

        winner = get_winner(player_choice, computer_choice)
        if winner == 'tie':
            print('It\'s a tie!')
        elif winner == 'player':
            print('You win this round!')
            player_score += 1
        else:
            print('Computer wins this round!')
            computer_score += 1

        print(f"Score: Player {player_score}, Computer {computer_score}")

        play_again = input("Do you want to play another round? (yes/no): ").lower()
        if play_again != 'yes':
            break

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
