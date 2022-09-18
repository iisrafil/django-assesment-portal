from django.contrib import messages
from django.shortcuts import render, redirect
from PIL import Image

from AssessmentPortal.settings import MEDIA_URL, BASE_DIR
from .forms import ImageFormset, PdfForm
from .models import PdfFile, Images, File



def upload_pdf_image(request):
    template_name = 'PdfConverter/create_pdf.html'
    if request.method == 'GET':
        formset = ImageFormset(request.GET or None)
        form = PdfForm(request.GET or None)
    elif request.method == 'POST':
        formset = ImageFormset(request.POST, request.FILES)
        form = PdfForm(request.POST)
        if formset.is_valid():
            pdf_form = form.save()
            for form in formset:
                image = form.cleaned_data['name']
                photo = Images(PdfFile=pdf_form, image=image)
                photo.save()

        File = convertToPdf(photo,pdf_form.name)
        return redirect(File.file.url)

    context = {
        'formset': formset,
        'form': form,
    }
    return render(request, template_name, context)


# def convertToPdf(image, name):
#     PDF_FILE = name+'.pdf'
#     image1 = Image.open(image.image.path)
#     rgb = image1.convert('RGB')
#     file = rgb.save(PDF_FILE, 'PDF', resoultion=100.0, commite=False)
#     Files = File()
#     Files.file = file
#     Files.save()
#     return Files


def convertToPdf(image, name):
    PDF_FILE = name+'.pdf'
    image1 = Image.open(image.image.path)
    rgb = image1.convert('RGB')
    file = rgb.save(f'{BASE_DIR}{MEDIA_URL}converted-pdf/{PDF_FILE}', 'PDF', resoultion=100.0, commite=False)
    Files = File(file=file)
    Files.file = f'converted-pdf/{PDF_FILE}'
    Files.save()
    return Files
