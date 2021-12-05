from django.core.management.base import BaseCommand
from authapp.models import ShopUser, ShopUserProfile
import json, os
#
# from mainapp.models import ProductCategory, Product
# from authapp.models import ShopUser
#
# JSON_PATH = 'mainapp/jsons'
#
#
# def load_from_json(file_name):
#     with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf8') as infile:
#         return json.load(infile)
#


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            user_profile = ShopUserProfile.objects.create(user=user)
            user_profile.save()
