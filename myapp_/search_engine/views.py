from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from . import modules
from . import models
from urllib.parse import urlencode
import json

# Create your views here.
def main(request):
    if request.method == 'POST':
        key_word = request.POST.get('key')
        mode = request.POST.get('mode')
        titles, abstracts, files, suggestword = modules.findByKeyWord(key_word, mode)
        num_result = len(files)
        articles = zip(titles, abstracts, files)
        return render(request, 'main.html', {'articles': articles, 'num_result': num_result, 'key': key_word, 'mode': mode, 'suggestword': suggestword})
    
    if 'change' in request.GET:
        mode = request.GET.get('mode')
        
        if mode == 'None':
            mode = 'Full'
        else:
            mode = 'None'
    elif 'mode' in request.GET:
        mode = request.GET.get('mode')
    else:
        mode = 'None'

        
    return render(request, 'main.html', {'key': None, 'mode': mode})

def Abstract(request):
    xml_file = request.GET.get('title')
    key = request.GET.get('key')
    mode = request.GET.get('mode')
    present = request.GET.get('present')
    title = modules.highlight_text(modules.findtitle(xml_file), key, mode)
    Abstract = modules.highlight_text(modules.findAbstract(xml_file), key, mode)
    num_sentences, num_words, num_characters, num_ascii, num_nonascii = modules.staticsINFO(xml_file)
    return render(request, 'Abstract.html', {'title': title, 'Abstract': Abstract, 'num_sentences': num_sentences, 'num_words': num_words, 'num_characters': num_characters, 'num_ascii': num_ascii, 'num_nonascii': num_nonascii, 'key': key, 'present': present, 'mode': mode})


def upload(request):
    key = request.GET.get('key')
    if request.method == 'POST':
        xmlist = request.FILES.getlist('xml')
        key_error = []
        fail = []
        for xml in xmlist:
            file_name = xml.name
            if file_name.split('.')[1] != 'xml':
                key_error.append(key)
                fail.append(file_name)
            uploadxml = models.Uploadxml(file = xml)
            uploadxml.save()
            abstract = modules.findAbstract(file_name)
            words = modules.Token(abstract)
            for word in words:
                if models.Words.objects.filter(term = word).exists():
                    term = models.Words.objects.filter(term = word)[0]
                else:
                    porter_term = modules.porter(word)
                    term = models.Words.objects.create(term = word, porter_term = porter_term)
                article = models.article.objects.create(file = xml, word = term)
        
        if len(fail) > 0:
            return render(request, 'upload.html', {'key': key_error, 'fail': fail})

        # save word to db
        
    
        return render(request, 'upload.html', {'key': key, 'file_name': file_name})

    return render(request, 'upload.html', {'key': key})

def main_two_xml(request):
    if request.method == 'POST':
        key_word = request.POST.get('key')
        mode = request.POST.get('mode')
        if 'Previous' in request.POST:
            page = int(request.POST.get('page')) - 1
        elif 'Next' in request.POST:
           page = int(request.POST.get('page')) + 1 
        else:
            page = 1
        titles, abstracts, files, suggestword = modules.findByKeyWord(key_word, mode)
        print(page)
        num_result = len(files[2*page-2: 2*page])
        articles = zip(titles[2*page-2: 2*page], abstracts[2*page-2: 2*page], files[2*page-2: 2*page])
        return render(request, 'main_two_xml.html', {'articles': articles, 'key': key_word, 'mode': mode, 'page': page, 'num': num_result, 'suggestword': suggestword})
    
    if 'change' in request.GET:
        mode = request.GET.get('mode')
        
        if mode == 'None':
            mode = 'Full'
        else:
            mode = 'None'
    elif 'mode' in request.GET:
        mode = request.GET.get('mode')
        print(mode)
    else:
        mode = 'None'

        
    return render(request, 'main_two_xml.html', {'key': None, 'mode': mode})

def present_type(request):
    key = request.GET.get('key')
    mode = request.GET.get('mode')
    present = request.GET.get('present')

    data = {
        'key': key,
        'mode': mode,
    }

    query_string = urlencode(data)

    if present == 'two':
        return redirect(f'/search_engine/main_two_xml?{query_string}')
    
    return redirect(f'/search_engine/main?{query_string}')

def main_statics(request):
    
    return render(request, 'main_statics.html')

def initial_chart(request):
    labels, data, labels_porter, data_porter = modules.Distributionbyterm()

    return JsonResponse([{'data': data, 'labels': labels, 'data_porter': data_porter, 'labels_porter': labels_porter}], safe=False)

def add_chart(request):
    labels, data, labels_porter, data_porter = modules.Distributionbyterm(modules.wordsuggest(request.POST.get('term')))

    return JsonResponse([{'data': data, 'labels': labels, 'data_porter': data_porter, 'labels_porter': labels_porter}], safe=False)
    