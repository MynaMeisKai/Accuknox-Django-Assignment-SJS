
import json
import os
from django.core.management.base import BaseCommand, CommandError
from api.models import *
from random import Random
from math import floor
from rest_framework.authtoken.models import Token

random_generator = Random()
random_number = random_generator.random()




def finpass():  
    return floor(random_number*10000)

class Command(BaseCommand):
    help = 'Upload JSON data to the SQLite database'
    
    
    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(os.path.dirname(__file__), 'generated.json')
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                for item in data:
                    user = CustomUser.objects.create(
                        email=item['email'],
                        name=item['name'],
                        username=item['username'],
                        password = finpass()
                    )
                    token = Token.objects.create(user=user)
                    
            self.stdout.write(self.style.SUCCESS(f'Successfully uploaded data from {json_file_path}.'))
        except FileNotFoundError:
            raise CommandError(f'File "{json_file_path}" does not exist.')
        except json.JSONDecodeError:
            raise CommandError(f'File "{json_file_path}" is not a valid JSON file.')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')
