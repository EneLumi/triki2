# TriKi2
## Trivia King the 2nd
Trivia game

TriKi2 is an interactive quiz game that challenges players across various categories, testing their knowledge and quick thinking. Players earn points for each correct answer, and their scores are tracked on a leaderboard. Trivia king is a fun way to learn new facts and compete for the top spot. 

![demo image](1.png)

## Installation and usage

git clone https://github.com/EneLumi/triki2.git

## Local installation

1. Clone the repository and create a virtual environment for it.<br/>
   Currently, TriKi2 uses Python 3.11

       python3.11 -m venv venv
       source venv/bin/activate


2. Install the requirements
   
      `pip install -r requirements.txt`


## Database

Use MySQL or PostgreSQL as db.
You need to create .env file with these values:

* SECRET_KEY="" # You need to create your own Django key
* DEBUG="True"
* DB_ENGINE="" # Choose your database
* DB_USER="" # Your database user name
* DB_PASSWORD="" # Your database password 
* DB_PORT="" # Choose your database port 
* DB_HOST="" # Choose your database host 
* DB_NAME="" # Choose your database name


Run commands in order: 

   `python manage.py makemigrations`   
   `python manage.py migrate`

   `python manage.py createsuperuser` (optional)
   
## Run the game

Start the game by running the following command:

`python manage.py runserver`

Navigate to http://127.0.0.1:8000/ 

Enjoy the game!

## Usage

In order to play, you need to create a user. After that you can start a game.

To start the game, follow the instructions
1. Select your favorite category to start your trivia challenge
3. Select length. Choose how many questions you want to answer
4. Choose difficulty level
5. Answer questions: You’ll be given a series of multiple choice questions to answer within a set time (of 20 seconds). 
6. Choose your answer and press check answer

![demo image](/2.png)

![demo image](/3.png)

Check the leaderboard: after completing the game, see where you stand on the leaderboard

![demo image](/4.png)

Play again! Challenge yourself again or compete against friends.

## Testing

To run tests, run command:<br/>
   `python manage.py test`

## GIT

1. Each new branch should be created from the `main` branch.

2. For the branch naming, start each branch name with the prefix according to the work you intend to do in it:

    - feature/
    - fix/

3. For the merge request, target the working branch to the `master` branch.

## Contact

If you have any questions, suggestions, or feedback, feel free to reach out:

GitHub: [EneLumi](https://github.com/EneLumi/triki2)

