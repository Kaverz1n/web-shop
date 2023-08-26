from django import forms

from catalog.models import Product, Version
from catalog.utils import get_wrong_words

WRONG_WORDS = get_wrong_words()


class ProductForm(forms.ModelForm):
    '''
    форма для создания и редактирования товара
    '''

    class Meta:
        model = Product
        exclude = ('created_at', 'last_change',)

    def __clean_inappropriate_words(self, cleaned_data):
        for word in WRONG_WORDS:
            if word.lower().strip() in cleaned_data.lower():
                raise forms.ValidationError(f'Слово {word} запрещено указывать в названии товара!')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        self.__clean_inappropriate_words(cleaned_data)

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        self.__clean_inappropriate_words(cleaned_data)

        return cleaned_data


class VersionForm(forms.ModelForm):
    '''
    Форма для создания версии продукта
    '''
    CURRENT_COUNTER = 0
    OBJECT_COUNTER = 0

    class Meta:
        model = Version
        fields = '__all__'

    def clean_is_current(self):
        cleaned_data = self.cleaned_data['is_current']
        objects = len(Version.objects.filter(product=self.instance.product))
        VersionForm.OBJECT_COUNTER += 1
        error = False

        # проверяет, что форма имеет активную версию, для инкрементирования счётчика активных версий
        if cleaned_data:
            VersionForm.CURRENT_COUNTER += 1

        # проверяет, что активных версий больше 1
        if VersionForm.CURRENT_COUNTER > 1:
            error = True

        # проверяет, что форма объекта является последней для обнуления счётчика активных версий
        if objects == VersionForm.OBJECT_COUNTER:
            VersionForm.OBJECT_COUNTER, VersionForm.CURRENT_COUNTER = 0, 0

        if error:
            raise forms.ValidationError('У продукта может быть лишь одна активная версия')

        return cleaned_data
