from django import forms
from .models import Post,ImageUpload,Category

class addPostForm(forms.ModelForm):
    CHOICES = Category.objects.filter(parent__isnull = True)
    
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':5,'cols':10}))
    category = forms.ModelChoiceField(initial=("Books"),queryset = CHOICES)
    terms_accepted = forms.BooleanField(initial=True,widget=forms.HiddenInput)
    main_image = forms.ImageField(label='Main Image',required=True)
    class Meta:
        model = Post
        fields = ('title','description','note','main_image','category','terms_accepted')

class termsForm(forms.Form):
    terms = forms.BooleanField(label= 'I agree to the Terms and Conditions',required=True,widget=forms.CheckboxInput)
    class Meta:
        fields = ('terms',)

class addImagesForm(forms.ModelForm):
    images = forms.ImageField(label='Extra Images',required=False, widget=forms.ClearableFileInput(attrs={'multiple': True,}))
    class Meta:
        model = ImageUpload
        fields = ('images',)




    

