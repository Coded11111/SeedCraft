import os
import random
import configparser
from tqdm import tqdm
import pyfiglet
from termcolor import colored

ascii_art = pyfiglet.figlet_format("SeedCraft", font="slant")
colored_ascii_art = colored(ascii_art, color="cyan")
print(colored_ascii_art)
print(colored("Seed Phrase Generator v1.0", "yellow"))
print("GitHub: https://github.com/7GitGuru/SeedCraft\n")


def words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        wordlist = file.readlines()
    return [word.strip() for word in wordlist]


def generate_seeds(wordlist, min_length, max_length):
    length = random.randint(min_length, max_length)
    seed_phrase = random.sample(wordlist, length)
    return ' '.join(seed_phrase)


def main(config_file, wordlist_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    num_seeds = int(config['DEFAULT']['num_seeds'])
    min_length = int(config['DEFAULT']['min_length'])
    max_length = int(config['DEFAULT']['max_length'])

    wordlist = words(wordlist_file)

    output_dir = 'results'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_count = 0
    output_file = os.path.join(output_dir, f'generated_seeds.txt')
    while os.path.exists(output_file):
        file_count += 1
        output_file = os.path.join(output_dir, f'generated_seeds({file_count}).txt')

    with open(output_file, 'w', encoding='utf-8') as file:
        with tqdm(total=num_seeds, ncols=80, unit=' seeds', unit_scale=True, unit_divisor=1000) as pbar:
            for _ in range(num_seeds):
                seed_phrase = generate_seeds(wordlist, min_length, max_length)
                file.write(seed_phrase + '\n')
                pbar.update(1)

    print(" ")
    print(colored(f"{num_seeds} seed phrases generated and saved to {output_file}\n", "green"))
    print(colored("Press Ctrl+C to exit.", "red"))


if __name__ == "__main__":
    main('config/config.ini', 'words/bip39.txt')

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting the program...")
