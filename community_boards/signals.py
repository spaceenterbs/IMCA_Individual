# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import Review, Board


# @receiver([post_save, post_delete], sender=Review)
# def update_board_metrics(sender, instance, **kwargs):
#     board = instance.board
#     board.get_reviews_count()


# # @receiver([post_save, post_delete], sender=Board)
# # def update_board_metrics(sender, instance, **kwargs):
# #     board = instance.board
# #     board.get_likes_count()
