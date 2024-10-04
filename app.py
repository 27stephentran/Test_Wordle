from flask import Flask, render_template, request
import random

app = Flask(__name__)

# List of possible words (You can expand this)
WORDS = ["apple", "grape", "melon", "pearl", "bread"]

# Choose a random word for the game
secret_word = random.choice(WORDS).upper()

@app.route('/', methods=['GET', 'POST'])
def index():
    guess = [''] * len(secret_word)  # Initialize guess with empty characters

    if request.method == 'POST':
        # Collect each letter from the form
        guess = [
            request.form.get(f'letter{i+1}', '').upper()
            for i in range(len(secret_word))
        ]

        guess_word = ''.join(guess)

        if len(guess_word) != len(secret_word):
            return render_template('index.html', error="Word must be the correct length.", word_length=len(secret_word), guess=guess)

        feedback = check_guess(guess_word, secret_word)

        if guess_word == secret_word:
            return render_template('index.html', feedback=feedback, success=True, word_length=len(secret_word), guess=guess)

        return render_template('index.html', feedback=feedback, guess=guess, word_length=len(secret_word))

    return render_template('index.html', word_length=len(secret_word), guess=guess)

def check_guess(guess, secret_word):
    feedback = []
    for i in range(len(secret_word)):
        if guess[i] == secret_word[i]:
            feedback.append('correct')  # Letter in the correct position
        elif guess[i] in secret_word:
            feedback.append('Right')  # Letter is in the word but wrong position
        else:
            feedback.append('Wrong')  # Letter is not in the word
    return feedback

if __name__ == '__main__':
    app.run(debug=True)
