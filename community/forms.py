from django import forms
from .models import Community, Comment

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
         # fields = '__all__'
         
        exclude = ['user','hits','like_users','recommend_users','date']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #fields = '__all__'
        exclude=['article', 'user']