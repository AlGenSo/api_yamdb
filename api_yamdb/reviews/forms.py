from django import forms

from .models import category, genre, title


class TitleForm(forms.ModelForm):

    class Meta:
        model = title.Title
        fields = '__all__'


class CategoryForm(forms.ModelForm):

    class Meta:
        model = category.Category
        fields = '__all__'


class GenreForm(forms.ModelForm):

    class Meta:
        model = genre.Genre
        fields = '__all__'
