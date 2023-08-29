from django.apps import AppConfig


class CommunityBoardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "community_boards"

    # def ready(self):
    #     import community_boards.signals  # Import the signals module
