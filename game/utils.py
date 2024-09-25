import requests
import random


# tõmba küsimused api-st
def get_questions_pool(amount: int, category: int, difficulty: str):
    try:
        url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type=multiple"
        response = requests.get(url)  # teeb apiga ühenduse
        response.raise_for_status()  # kontrollib, kas api vastab
        response_json = response.json()  # vastus läheb json faili
        return response_json.get("results", [])  # võtab json failist vastuse
    except requests.RequestException as e:  # kui saab errori
        print(f"Error fetching questions: {e}")
        return []


# segab vastuste asukohti, et poleks järjekorras
def shuffle_choices(choices: list):
    random.shuffle(choices)
    return choices


# võtab arvesse kasutaja kategooriate valikut
def get_categories():
    url = 'https://opentdb.com/api_category.php'
    response = requests.get(url)
    response_json = response.json()
    return [(category['id'], category['name']) for category in response_json['trivia_categories']]


# võtab arvesse kasutaja raskusastme valikut
def get_difficulties():
    url = 'https://opentdb.com/api.php'
    response = requests.get(url, params={'command': 'get_difficulties'})
    response_json = response.json()
    return [(difficulty, difficulty.capitalize()) for difficulty in ['easy', 'medium', 'hard']]



# kalkuleerib skoori vastavalt valitud raskusastmele ja õigetele vastustele + streaks
def calculate_score(difficulty, num_questions, answer_list):
    difficulty_multiplier = {"easy": 10, "medium": 20, "hard": 30}

    streak_count = 0
    score = 0
    breakdown = []

    for i in range(num_questions):
        is_correct = i < len(answer_list) and answer_list[i]
        points_earned = difficulty_multiplier.get(difficulty) if is_correct else 0

        if is_correct:
            score += points_earned
            streak_count += 1
            breakdown.append(
                {
                    "question": f"Question {i + 1}",
                    "points": f"+{points_earned} points",
                    "result": "Correct",
                }
            )
        else:
            streak_count = 0
            breakdown.append(
                {
                    "question": f"Question {i + 1}",
                    "points": "",
                    "result": "Incorrect",
                }
            )

        # lisa streak-i boonused
        if streak_count == 3:
            score *= 2
            breakdown.append(
                {
                    "question": "Streak Bonus",
                    "points": f"x2 multiplier applied",
                    "result": "",
                }
            )
        elif streak_count == 5:
            score *= 3
            breakdown.append(
                {
                    "question": "Streak Bonus",
                    "points": f"x3 multiplier applied",
                    "result": "",
                }
            )

    return score, breakdown
