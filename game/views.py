from django.shortcuts import render, redirect
import html
from game.forms import QuizSettingsForm, QuizForm
from .models import Score
from usermanager.utils import get_default_user
from .utils import (
    get_questions_pool,
    shuffle_choices,
    calculate_score,
)


# quiz-i alustamine, valikute tegemine
def start_quiz(request):
    if request.method == "POST":
        form = QuizSettingsForm(request.POST)
        if form.is_valid():
            # salvestab minu valikud
            request.session["category"] = form.cleaned_data.get("category")
            request.session["amount"] = form.cleaned_data.get("amount")
            request.session["difficulty"] = form.cleaned_data.get("difficulty")

            # paneb funktsioonis muutujad nulli, et oleks puhas leht
            request.session["current_question_index"] = (
                0  # alustab esimesest küsimusest
            )
            request.session["correct_answers"] = 0  # alguses on õigete vastuste arv 0
            request.session["answer_list"] = []  # salvestab õiged vastused
            request.session["feedback"] = (
                None  # uut mängu alustades kustutab vana info (valikud)
            )

            return redirect("play_game")
    form = QuizSettingsForm()  # kui request method ei "post"-i, siis nullib settingud

    return render(request, "start_quiz.html", {"form": form})


# mäng ise
def play_game(request):
    try:
        current_index = request.session.get(
            "current_question_index", 0
        )  # järjestab küsimusi
        total_questions = request.session.get("amount", 10)
        difficulty = request.session.get("difficulty", "easy")
        question_pool = request.session.get(
            "question_pool", []
        )  # api antud küsimuste list

        if request.method == "GET":
            if current_index == 0:
                # tee kindlaks, et kogu vajalik info on olemas
                category = request.session.get("category")
                if not category:
                    return redirect("start_quiz")  # kui kategooriat pole valitud

                question_pool = get_questions_pool(
                    total_questions, category, difficulty  # see info peab olemas olema
                )
                request.session["question_pool"] = question_pool
                request.session["answer_list"] = []

            if (not question_pool):  # kui pole piisavalt küsimusi siis saadab algusesse tagasi
                return redirect("start_quiz")

            # kui on piisavalt küsimusi, siis valmistab ette valikuvariandid, segab vastused jne
            if current_index < len(question_pool):
                question = question_pool[current_index]
                question_text = html.unescape(question["question"])
                choices = question.get("incorrect_answers")  # võtab valed vastused
                choices.append(question.get("correct_answer"))  # ja õige vastuse
                shuffled_choices = shuffle_choices(choices)  # ja segab need ära

                request.session["current_question"] = question_text
                request.session["correct_answer"] = html.unescape(
                    question.get("correct_answer"))  # unescape tähendab, et näitab sümboleid ilusti
                request.session["choices"] = shuffled_choices

                # võtab form-i ja formuleerib selle
                form = QuizForm(
                    choices=[
                        (choice, html.unescape(choice)) for choice in shuffled_choices
                    ]
                )
                return render(
                    request,
                    "quiz.html",
                    {
                        "question": question_text,
                        "form": form,
                        "progress": f"{current_index + 1}/{total_questions}",
                    },
                )
        # kasutaja saadab oma vastuse variandi
        elif request.method == "POST":
            user_choice = request.POST.get("choice")
            correct_choice = request.session.get("correct_answer")

            if (
                    not user_choice
            ):  # kui ei teegi valikut, siis on aeg otsas ja vastus vale
                request.session["feedback"] = (
                    f"Time is up! The correct answer was {correct_choice}."
                )
                request.session["answer_list"].append(False)
            elif user_choice == correct_choice:
                request.session["correct_answers"] += 1
                request.session["feedback"] = (
                    f"Correct! The correct answer was {correct_choice}."
                )
                request.session["answer_list"].append(True)
            else:
                request.session["feedback"] = (
                    f"Wrong! The correct answer was {correct_choice}."
                )
                request.session["answer_list"].append(False)

            request.session["current_question_index"] += 1  # annab järgmise küsimuse

            # kui mäng on läbi, kalkuleerib punktid ja näitab tulemust
            if request.session.get("current_question_index") >= total_questions:
                score, breakdown = calculate_score(
                    difficulty, total_questions, request.session.get("answer_list")
                )
                request.session["score"] = score
                request.session["breakdown"] = breakdown
                return redirect("result")

            return redirect("play_game")

    except KeyError as e:
        # kui on key-d puudu
        print(f"Missing session key: {e}")
        return redirect("start_quiz")
    except Exception as e:
        # kui on muud errorid
        print(f"Unexpected error: {e}")
        return redirect("start_quiz")


def result_view(request):  # tulemuste jaoks
    try:
        # tõmbab vajalikud andmed
        correct_answers = request.session.get("correct_answers", 0)
        total_questions = request.session.get("amount", 10)
        score = request.session.get("score", 0)
        breakdown = request.session.get("breakdown", [])

        # kindlustab, et skoor on salvestatud andmebaasi
        difficulty = request.session.get("difficulty", "easy")

        if not score:
            # kui pole skoori kalkuleeritud, siis teeb selle nüüd
            score, breakdown = calculate_score(
                difficulty, total_questions, request.session.get("answer_list", [])
            )
        # andmebaasi minev info (skoor koosneb):
        score_instance = Score(
            user=request.user if request.user.is_authenticated else get_default_user(),
            difficulty=difficulty,
            num_questions=total_questions,
            num_correct=correct_answers,
            score=score,
        )
        score_instance.save()  # kindlusta, et skoor oleks databaasi salvestatud

        # näita quizi tulemusi netilehel
        return render(
            request,
            "result.html",
            {
                "correct_answers": correct_answers,
                "total_questions": total_questions,
                "score": score,
                "breakdown": breakdown,
            },
        )
    except Exception as e:
        print(f"Error in result_view: {e}")
        return redirect("start_quiz")


def rules(request):
    return render(request, "rules.html", {})
