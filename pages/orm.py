# from django.db.models import BooleanField, Case, Count, When

# from .models import Post, PostImage

# result = Post.objects.annotate(
#     ilosc=Case(
#         When(postimage__id__gt=0, then=True), default=False, output_field=BooleanField()
#     )
# ).values("id", "other_fields_here", "ilosc")


# print(result)
