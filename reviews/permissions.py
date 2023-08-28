from rest_framework import permissions


class IsReviewOrBigreviewOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a review or bigreview to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the review or bigreview
        return obj.review_writer == request.user or obj.bigreview_writer == request.user
