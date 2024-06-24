from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from celery_demo.project_core.forms import UploadImageForm
from celery_demo.project_core.tasks import resize_image


class ImageUploadView(TemplateView):
    template_name = "image-uploaded.html"


class UploadImageView(View):
    template_name = 'upload-image-template.html'
    form_class = UploadImageForm
    success_url = 'uploaded'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = default_storage.save(image.name, image)
            resize_image.delay(image_path, 800, 600)

            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})