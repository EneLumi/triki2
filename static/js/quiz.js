let timeLeft = 20;
const timerElement = document.getElementById("timer");
const quizForm = document.getElementById("quiz-form");
const buttons = document.querySelectorAll(".quiz-option");
const choiceInput = document.getElementById("choice-input");
const submitButton = document.getElementById("submit-button");
let selectedButton = null;

const correctAnswer = correctAnswerData; // korrektne vastus Django templatest

const countdown = setInterval(() => {
    timeLeft--;
    timerElement.textContent = timeLeft;

    if (timeLeft <= 0) {
        clearInterval(countdown);
        // Naitab oiget vastust, kui popup tuleb yles
        alert(`Time is up! The correct answer was: ${correctAnswer}`);
        quizForm.submit();  // submittib formi seejärel
    }
}, 1000);

buttons.forEach((button) => {
    button.addEventListener("click", function () {
        // paneb nupud algseks
        buttons.forEach((btn) =>
            btn.classList.remove("btn-success", "btn-danger", "active")
        );

        // vajutatud nupp aktiivseks
        this.classList.add("active");
        choiceInput.value = this.getAttribute("data-value");
        selectedButton = this;

        // Submitingi nupp aktiivseks
        submitButton.disabled = false;
    });
});

quizForm.addEventListener("submit", function (event) {
    event.preventDefault();  // Ei saada kohe vormi minema

    // Check the answer
    if (choiceInput.value) {
        const correctAnswer = correctAnswerData;  // Oige vastus django templatist
        if (choiceInput.value === correctAnswer) {
            selectedButton.classList.add("btn-success");
        } else {
            selectedButton.classList.add("btn-danger");

            // oige vastus roheliseks
            buttons.forEach((button) => {
                if (button.getAttribute("data-value") === correctAnswer) {
                    button.classList.add("btn-success");
                }
            });
        }

        // ei saa muhvigi teha, kui popup on yleval
        buttons.forEach((btn) => (btn.disabled = true));
        submitButton.disabled = true;

        // taimer
        setTimeout(() => {
            quizForm.submit();
        }, 2000);  // siit saab delay-d muuta
    }
});
