from django.shortcuts import render, redirect
import markdown
from django.contrib import messages
from django.urls import reverse
from . import util
from django.http import HttpResponseRedirect
from django import forms
import random




# Since we're going to be needing the markdown...a converter is needed
def md_converter(variable):
    content = util.get_entry(variable)
    mark_down = markdown.Markdown()
    if content == None:
        return None
    else:
        converted_content = mark_down.convert(content)
        return converted_content

# then we'd need the title showing on the url 
def entry(request, title):
    approved_content = md_converter(title)
    if approved_content is None:
        return render(request, "encyclopedia/404.html", {'message': messages.error(request, 'Does not Exist'), 'title': title})    
    else:
        return render(request, "encyclopedia/entry.html",{'title': title, 'approved_content': approved_content})

def index(request):
    if request.method == 'POST':
        title_form = request.POST.get('form_title')
        form_text = request.POST.get('text_form')
        if title_form and form_text:
            if util.get_entry(title_form):
                error_message = f"'{title_form}' already exists."
                return render(request, 'encyclopedia/index.html', {'entries': util.list_entries(), 'error_message': error_message})
            new_saves = util.save_entry(title_form, form_text)
            if new_saves:
                request.session['new_saves'] = new_saves
                return redirect('encyclopedia:new_entry', title=title_form)   
    return render(request, 'encyclopedia/index.html', {'entries': util.list_entries()})
    
def new_entry(request, title):
    entryy = util.get_entry(title)
    if entryy is None:
        return render(request, 'encyclopedia/404.html', {'error_message': f"'{title}' not found."})
    return render(request, 'encyclopedia/new_entry.html', {'title': title, 'entry': entryy})


def search(request):
    if request.method == 'POST':
        result = request.POST['q']
        
        if result is not None:
            entry = md_converter(result)   
            if entry is None:
                all_entries = util.list_entries()
                partial_matches = [entry for entry in all_entries if result.lower() in entry.lower()]# check for the partial_match to the entry
                if partial_matches:
                    return render(request, 'encyclopedia/partial_matches.html', {'partial_matches': partial_matches})
            return render(request, 'encyclopedia/search.html', {'entry': entry})
    return render(request, 'encyclopedia/404.html')
            
# new_page

class NewEntryForm(forms.Form):
    text_form = forms.CharField(widget=forms.Textarea)
    form_title = forms.CharField(label="form_title")
    
def create(request):
    if request.method == 'POST':
        entry_form = NewEntryForm(request.POST)
        if entry_form.is_valid():
            print(entry_form.cleaned_data)
            form_title = entry_form.cleaned_data["form_title"]
            text_form = entry_form.cleaned_data["text_form"]
            approved_contents = util.save_entry(form_title,text_form)
            if approved_contents:
                request.session['approved_contents'] = True
                return redirect(reverse('encyclopedia:index') + f'?title_form={form_title}')
            else:
                return render(request, 'encyclopedia/404.html')
                # If not approved, redirect to the newly created entry's page                
    entry_form = NewEntryForm()    
    return render(request, 'encyclopedia/create.html', {'form': entry_form})



def edit_entry(request, title):
    entry_content = util.get_entry(title)
    print(title)
    if entry_content is None:
        return render(request, 'encyclopedia/404.html', {'error_message': f"'{title}' not found."})
    
    if request.method == 'POST':
        edit_contents = request.POST.get('edit_contents')
        util.save_entry(title,edit_contents)
        if edit_contents:
            request.session['edit_success'] = True
            return redirect('encyclopedia:title', title=title)
        return redirect('encyclopedia:index', title=title)

    return render(request, 'encyclopedia/edit.html', {"title": title, 'entry_content':entry_content})

def random_page(request):
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect('encyclopedia:title', title = random_title)
    return render(request,'encyclopedia/404.html')
    



        
        
            
    
   
  

        
    

 