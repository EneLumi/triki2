from django.test import TestCase
from django.contrib.auth.models import User
from .models import Score
import requests


# see testib, kas skoor luuakse, loetakse, uuendatakse, kustutatakse
class ScoreModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        self.score = Score.objects.create(
            user=self.user,
            difficulty='Easy',
            num_questions=10,
            num_correct=8,
            score=80.00
        )

    def test_create_score(self):
        self.assertEqual(self.score.score, 80.00)

    def test_read_score(self):
        self.assertEqual(Score.objects.count(), 1)
        self.assertEqual(Score.objects.first(), self.score)

    def test_update_score(self):
        updated_score = Score.objects.get(id=self.score.id)
        updated_score.score = 90.00
        updated_score.save()
        self.assertEqual(Score.objects.get(id=self.score.id).score, 90.00)

    def test_delete_score(self):
        self.score.delete()
        self.assertEqual(Score.objects.count(), 0)

    def test_score_str_representation(self):
        self.assertEqual(str(self.score), "testuser - 80.00 points (Easy, 10 questions, 8 correct)")


class OpenTDBApiTestCase(TestCase):
    def test_api_provides_questions(self):
        # pane paika api parameetrid
        endpoint = 'https://opentdb.com/api.php'
        params = {
            'amount': 10,
            'category': 9,
            'difficulty': 'medium',
            'type': 'multiple'
        }

        # tee api taotlus
        response = requests.get(endpoint, params=params)

        # kui saad errori 429, siis vasta nii
        if response.status_code == 429:
            self.fail("API rate limit exceeded. Please try again later.")

        # kontrolli, kas api vastas (kood 200 on ok)
        self.assertEqual(response.status_code, 200, "API request failed")

        # pane info ajutisse json faili
        data = response.json()

        # kontrolli, kas vastus on vajalike "key"-dega
        self.assertIn('response_code', data, "Response does not contain response_code")
        self.assertIn('results', data, "Response does not contain results")

        # kontrolli, kas vatuse kood näitab, et kõik on ok, (0 tähendab ok)
        self.assertEqual(data['response_code'], 0, "API returned an error with the response code")

        # kontrolli kas said sama palju küsimusi kui taotlesid
        self.assertEqual(len(data['results']), 10, "API did not return the expected number of questions")

        # kontrolli kas igal küsimusel on olemas vajalikud väljad
        for question in data['results']:
            self.assertIn('category', question, "Question is missing category field")
            self.assertIn('type', question, "Question is missing type field")
            self.assertIn('difficulty', question, "Question is missing difficulty field")
            self.assertIn('question', question, "Question is missing question field")
            self.assertIn('correct_answer', question, "Question is missing correct_answer field")
            self.assertIn('incorrect_answers', question, "Question is missing incorrect_answers field")

            # kontrolli, kas raskusaste vastab küsitule
            self.assertEqual(question['difficulty'], 'medium',
                             "Question difficulty does not match the requested difficulty level")
