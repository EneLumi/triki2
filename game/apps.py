from django.apps import AppConfig

#see on automaatne fail, mis tekib peale startapp käsklust
#konfigureerib selle appi django projektis, appi nime ja default välja tüübi primary key-de jaoks

class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' #64bit integer field (suurte datasetside jaoks)
    name = 'game'
