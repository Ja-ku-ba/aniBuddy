from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Value
from django.db.models.functions import Concat

from .models import Post


# is used to specify if post have attached image, if do then, get how many,
# and then get first image path.
# Chceck if post is not deleted
def get_post(querryset, **conditions):
    query = querryset.objects

    if "deleted" in conditions:
        deleted_query = conditions.get("deleted")
    else:
        deleted_query = False

    if "id" in conditions:
        try:
            query = querryset.objects.filter(id=conditions.get("id"))
        except:
            return None

    result = (
        query.annotate(
            images_quantity=Count("postimage__post_id", distinct=True),
            image_first=Min("postimage__image"),
            image_first_id=Min("postimage__id"),
            username=Concat("owner__username", Value("")),
        )
        .order_by("-added")
        .filter(deleted=deleted_query)
    )
    print(result)
    return result

    # .values(
    #     "id",
    #     "added",
    #     "owner",
    #     "username",
    #     "content",
    #     "description",
    #     "images_quantity",
    #     "image_first",
    #     "image_first_id",
    # )
