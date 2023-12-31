from django import forms

from catalog.models import Product, Version
from catalog.services import get_wrong_words

WRONG_WORDS = get_wrong_words()


class ProductForm(forms.ModelForm):
    '''
    форма для создания и редактирования товара
    '''

    class Meta:
        model = Product
        exclude = ('created_at', 'last_change', 'user', 'is_published',)

    def __clean_inappropriate_words(self, cleaned_data) -> None:
        for word in WRONG_WORDS:
            if word.lower().strip() in cleaned_data.lower():
                raise forms.ValidationError(f'Слово {word} запрещено указывать в названии товара!')

    def clean_name(self) -> str:
        cleaned_data = self.cleaned_data['name']
        self.__clean_inappropriate_words(cleaned_data)

        return cleaned_data

    def clean_description(self) -> str:
        cleaned_data = self.cleaned_data['description']
        self.__clean_inappropriate_words(cleaned_data)

        return cleaned_data


class VersionForm(forms.ModelForm):
    '''
    Форма для создания версии продукта
    '''
    CURRENT_COUNTER = 0

    class Meta:
        model = Version
        fields = '__all__'

    def clean(self) -> str:
        cleaned_data = super().clean()
        clean_is_current = cleaned_data['is_current']

        if cleaned_data['number'] == 1:
            VersionForm.CURRENT_COUNTER = 0

        if clean_is_current:
            VersionForm.CURRENT_COUNTER += 1

        if VersionForm.CURRENT_COUNTER > 1:
            raise forms.ValidationError('У продукта может быть лишь одна активная версия')

        return cleaned_data


class ModeratorProductForm(ProductForm):
    '''
    форма для создания и редактирования товара
    '''

    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published',)
