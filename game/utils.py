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

    score = 0  # skoor enne streak-e
    breakdown = []  # dictionary,peab arvet kõikide vastuste punktide üle ja kas vastus oli õige või vale. Siia lisanduvad hiljem ka streakid
    correct_answers = []  # boolean list hoiustab iga vastuse tulemust, õige/True, vale/False. Vajalik hiljem streakide arvutamiseks

    # Arvutab baas-skoori (ilma streakideta) ja õigeid/valesid vastuseid
    for i in range(num_questions): #käib läbi iga küsimuse ühes quizis
        is_correct = i < len(answer_list) and answer_list[i] #kontrollib kas vastus oli õige (kas indeks oli õiges vahemikus ja kas vastus oli õige)
        points_earned = difficulty_multiplier.get(difficulty) if is_correct else 0
        correct_answers.append(is_correct)

        if is_correct:
            score += points_earned
            breakdown.append({
                "question": f"Question {i + 1}",
                "points": f"+{points_earned} points",
                "result": "Correct"
            })
        else:
            breakdown.append({
                "question": f"Question {i + 1}",
                "points": "0 points",
                "result": "Incorrect"
            })

    # Streakide arvutamine
    total_score = score #lõplik skoor, peale streake
    streak_count = 0 #loeb, mitu õiget vastust järjest on
    streak_start = None  # märgib küsimuse indeksi, et millal streak algas. Alguses on None, sest alguses pole ühtegi õiget vastust.
    streaks = []  # streakide boonuspunkide detailid

    for i, is_correct in enumerate(correct_answers):
        if is_correct:
            if streak_start is None:
                streak_start = i  # uue streaki algus
            streak_count += 1 #hakkab lugema, mitu õiget vastust järjest on
        else:
            # kui tuleb vale vastus, siis kontrollib, mitu õiget vastust järjest oli
            while streak_count > 0:
                if streak_count >= 5:  # kui on viis või rohkem
                    # Pane x3 multiplier esimesele viiele streakist
                    bonus_points = 2 * 5 * difficulty_multiplier.get(difficulty) #korrutab tegelikult kahega, sest baaspunktidele tuleb juurde boonus
                    total_score += bonus_points
                    streaks.append({
                        "question": f"Streak Bonus (x3 for questions {streak_start + 1} to {streak_start + 5})",
                        "points": f"x3 multiplier applied (+{bonus_points} points)",
                        "result": "" #tabelis seda välja ei täida
                    })
                    streak_count -= 5  # tõmbab streak-counti nulli, et uuesti alustada
                    streak_start += 5  # liigutab start-indeksi viie võrra edasi
                elif streak_count >= 3:  # kui on 3 õiget järjest
                    # paneb x2 multiplier esimesele kolmele strakist
                    bonus_points = 1 * 3 * difficulty_multiplier.get(difficulty)
                    total_score += bonus_points
                    streaks.append({
                        "question": f"Streak Bonus (x2 for questions {streak_start + 1} to {streak_start + 3})",
                        "points": f"x2 multiplier applied (+{bonus_points} points)",
                        "result": ""
                    })
                    streak_count -= 3  # vähendab kolme võrra
                    streak_start += 3  # liigutab kolme võrra edasi
                else:
                    break  # rohkem ei saa lisada streake

            # resetib streaki
            streak_count = 0
            streak_start = None

    # Järjestikuste streakide arvestus. Kontrollib, kas peale loopi on veel streake. Sama loogika nagu enne.
    if streak_count > 0:
        while streak_count > 0:
            if streak_count >= 5:
                bonus_points = 2 * 5 * difficulty_multiplier.get(difficulty)
                total_score += bonus_points
                streaks.append({
                    "question": f"Streak Bonus (x3 for questions {streak_start + 1} to {streak_start + 5})",
                    "points": f"x3 multiplier applied (+{bonus_points} points)",
                    "result": ""
                })
                streak_count -= 5
                streak_start += 5
            elif streak_count >= 3:
                bonus_points = 1 * 3 * difficulty_multiplier.get(difficulty)
                total_score += bonus_points
                streaks.append({
                    "question": f"Streak Bonus (x2 for questions {streak_start + 1} to {streak_start + 3})",
                    "points": f"x2 multiplier applied (+{bonus_points} points)",
                    "result": ""
                })
                streak_count -= 3
                streak_start += 3
            else:
                break

    # lisa boonused breakdowni
    breakdown.extend(streaks)

    return total_score, breakdown



