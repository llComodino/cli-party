import random
import time
import sys
import keyboard
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Initialize colorama

def load_words(filename):
    with open(filename, 'r') as file:
        return set(word.strip().lower() for word in file)

def load_letter_set(filename):
    with open(filename, 'r') as file:
        return set(letter.strip().lower() for letter in file)

def load_syllables(filename):
    syllables = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                syllable, difficulty = line.split(';')
                syllables[syllable.strip().upper()] = int(difficulty)
    return syllables

def save_used_word(word, duration, score):
    with open('used_words.txt', 'a') as file:
        file.write(f"{word},{duration},{score}\n")

def update_used_letters(word, used_letters, all_letters):
    for letter in word:
        if letter in all_letters:
            used_letters.add(letter)
    return used_letters

def clear_used_words():
    try:
        with open('used_words.txt', 'w') as file:
            pass
    except Exception as e:
        print(f"An error occurred while clearing the file: {e}")

def print_game_state(score, word_count, all_letters, used_letters, syllable):
    print("\033[2J\033[H", end="")  # Clear screen and move cursor to top-left
    print(f"{Fore.RED}Score: {score} | Words: {word_count}{Style.RESET_ALL}")
    
    print("Letters: ", end="")
    for letter in sorted(all_letters):
        if letter in used_letters:
            print(f"{Fore.LIGHTBLACK_EX}{letter}{Style.RESET_ALL}", end=" ")
        else:
            print(f"{Fore.YELLOW}{letter}{Style.RESET_ALL}", end=" ")
    print()
    
    print(f"{Fore.BLUE}Your syllable is: {Fore.MAGENTA}{syllable}{Style.RESET_ALL}")

def main():
    words = load_words('wordlist.txt')
    all_letters = load_letter_set('letter_set.txt')
    syllables = load_syllables('syllables.txt')
    clear_used_words()
    
    print("Welcome to CLI Party!")
    print("A single player endurance version of the famous jklm.fun bomb party.")
    print("Press CTRL+C or ESC to end the game.")
    input("Press Enter to start...")
    
    min_difficulty = int(input("Enter the starting difficulty (1-5): "))
    while min_difficulty < 1 or min_difficulty > 5:
        min_difficulty = int(input("Invalid input. Please enter a number between 1 and 5: "))

    used_letters = set()
    score = 0
    word_count = 0
    used_words = set()

    try:
        while True:
            available_syllables = [syl for syl, diff in syllables.items() if diff >= min_difficulty]
            if not available_syllables:
                print("No syllables available at this difficulty. Game over!")
                break

            syllable = random.choice(available_syllables)
            retry_count = 0

            while retry_count < 10:
                print_game_state(score, word_count, all_letters, used_letters, syllable)

                start_time = time.time()
                user_word = input("Enter a word containing this syllable: ").strip().lower()

                duration = time.time() - start_time

                if user_word in used_words:
                    print("You've already used this word!")
                elif user_word not in words:
                    print("This word is not in the word list!")
                    retry_count += 1
                elif syllable.lower() not in user_word:
                    print(f"The word doesn't contain the syllable {syllable}!")
                    retry_count += 1
                else:
                    print("Correct!")
                    used_words.add(user_word)
                    save_used_word(user_word, duration, score)
                    words.remove(user_word)
                    word_count += 1
                    
                    used_letters = update_used_letters(user_word, used_letters, all_letters)
                    if used_letters == all_letters:
                        score += 1
                        print("You used all the letters! +1 point")
                        used_letters.clear()
                    
                    break  # Correct word found, break out of retry loop

                if retry_count < 10:
                    input("Press Enter to continue...")
                else:
                    print("Max retries reached. Changing syllable.")
                    input("Press Enter to continue...")

    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
    
    print(f"Final Score: {score}")
    print(f"Total Words: {word_count}")

if __name__ == "__main__":
    main()
