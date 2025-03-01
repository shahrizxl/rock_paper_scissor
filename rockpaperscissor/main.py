from flask import Flask, render_template, request, jsonify
import random
import csv
import os

app = Flask(__name__)

# CSV file to store game results
CSV_FILE = "game_results.csv"

# Choices available in the game
CHOICES = ["Rock", "Paper", "Scissors"]

def get_computer_choice():
    return random.choice(CHOICES)

def determine_winner(player, computer):
    if player == computer:
        return "Draw"
    elif (player == "Rock" and computer == "Scissors") or \
         (player == "Scissors" and computer == "Paper") or \
         (player == "Paper" and computer == "Rock"):
        return "Player Wins"
    else:
        return "Computer Wins"

def save_result(player, computer, result):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Player Choice", "Computer Choice", "Result"])
        writer.writerow([player, computer, result])

def calculate_statistics():
    stats = {"Rock": {"wins": 0, "losses": 0, "draws": 0, "total": 0},
             "Paper": {"wins": 0, "losses": 0, "draws": 0, "total": 0},
             "Scissors": {"wins": 0, "losses": 0, "draws": 0, "total": 0}}
    
    if not os.path.exists(CSV_FILE):
        return stats
    
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            choice = row["Player Choice"]
            result = row["Result"]
            if choice in stats:
                stats[choice]["total"] += 1
                if result == "Player Wins":
                    stats[choice]["wins"] += 1
                elif result == "Computer Wins":
                    stats[choice]["losses"] += 1
                elif result == "Draw":
                    stats[choice]["draws"] += 1
    
    for choice in CHOICES:
        total = stats[choice]["total"]
        if total > 0:
            stats[choice]["win_percentage"] = round((stats[choice]["wins"] / total) * 100, 2)
            stats[choice]["loss_percentage"] = round((stats[choice]["losses"] / total) * 100, 2)
            stats[choice]["draw_percentage"] = round((stats[choice]["draws"] / total) * 100, 2)
        else:
            stats[choice]["win_percentage"] = 0
            stats[choice]["loss_percentage"] = 0
            stats[choice]["draw_percentage"] = 0
    
    return stats

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    player_choice = data.get("choice")
    computer_choice = get_computer_choice()
    result = determine_winner(player_choice, computer_choice)
    save_result(player_choice, computer_choice, result)
    return jsonify({"computer": computer_choice, "result": result})

@app.route('/stats', methods=['GET'])
def stats():
    statistics = calculate_statistics()
    return jsonify(statistics)

if __name__ == '__main__':
    app.run(debug=True)
