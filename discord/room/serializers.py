from  rest_framework import serializers
from . import models

class Topics(serializers.ModelSerializer):
   class Meta:
      model=models.Topics
      fields=[]
