from django.contrib.auth.models import User


# vaja selleks, et kui ei ole veel kasutajaid, siis loob selle, selleks et ei oleks vigasid
def get_default_user():
    user = User.objects.first()  # tõmba esimine kasutaja User model-ist
    if not user:
        user = User.objects.create_user(
            username="defaultuser",
            password="defaultpassword",
        )
    return user.pk  # annab kasutaja primary key (ID), kui kasutaja on olemas, siis tema oma, kui pole, siis loob selle
