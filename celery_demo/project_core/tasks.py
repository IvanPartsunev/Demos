import io

from PIL import Image
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


@shared_task
def resize_image(image_path, width, height):
    with default_storage.open(image_path, 'rb') as f:
        image = Image.open(f)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()

        format_extension = image.format if image.format else 'JPEG'

        image.save(buffer, format=format_extension)
        new_image_content = ContentFile(buffer.getvalue())

    default_storage.delete(image_path)
    new_image_path = default_storage.save(image_path, new_image_content)
    return new_image_path
