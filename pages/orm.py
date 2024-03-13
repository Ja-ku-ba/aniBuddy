from django.db.models import Count, Min, Value
from django.db.models.functions import Concat


# is used to specify if post have attached image, if do then, get how many,
# and then get first image path.
# Chceck if post is not deleted
def get_post(querryset, **conditions):
    if "id" in conditions:
        id_query = conditions.get("id")
        query = querryset.objects.filter(id=id_query)
    else:
        query = querryset.objects

    if "deleted" in conditions:
        deleted_query = conditions.get("deleted")
    else:
        deleted_query = False

    result = (
        query.annotate(
            images_quantity=Count("postimage__post_id", distinct=True),
            image_first=Min("postimage__image"),
            image_first_id=Min("postimage__id"),
            username=Concat("owner__username", Value("")),
        )
        .order_by("-added")
        .filter(deleted=deleted_query)
        .values(
            "id",
            "added",
            "owner",
            "username",
            "content",
            "description",
            "images_quantity",
            "image_first",
            "image_first_id",
        )
    )
    return result
