import datetime
from django import forms
from django.template.loader import render_to_string

from .models import Image

class DragAndDropImageField(forms.widgets.ClearableFileInput):
    def render(self, *args, **kwargs):
        original = super(DragAndDropImageField, self).render(*args, **kwargs)
        context = {
            "original": original
        }
        return render_to_string("widgets/drag_and_drop_image.html", context)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        widgets = {
            'image': DragAndDropImageField(),
        }

    def is_valid(self, *args, **kwargs):
        if super(ImageUploadForm, self).is_valid(*args, **kwargs):
            # Everything is valid, return away
            return True

        if not self.instance.pk:
            self.attempt_auto_upload(*args, **kwargs)

        return False

    def save(self, *args, **kwargs):
        return super(ImageUploadForm, self).save(*args, **kwargs)
