from django import forms
from .models import Post,ImageUpload

class addPostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':5,'cols':10}))
    class Meta:
        model = Post
        fields = ('title','description','category')

class addImagesForm(forms.ModelForm):
    images = forms.ImageField(label='',required=True, widget=forms.ClearableFileInput(attrs={'multiple': True,}))
    class Meta:
        model = ImageUpload
        fields = ('images',)


    

