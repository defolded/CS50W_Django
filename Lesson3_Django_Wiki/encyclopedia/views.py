from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import markdown
import re
import random
import time

from . import util


def index(request):
    topics = util.list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": topics,
        "randomIndex": topics[random.randint(0,len(util.list_entries())-1)]
    })

def wiki(request, name):
    topics = util.list_entries()
    if util.get_entry(name) == None:
        return HttpResponse("This page is not available.")
    else:
        with open(f'entries/{name}.md', 'r') as f:
            tempMd = f.read()
    if request.POST.get('edit'):
        util.save_entry(name, request.POST.get('edit'))
        return HttpResponseRedirect(f"/wiki/{name}")
    return render(request, 'encyclopedia/page.html', {
        "text": markdown.markdown(tempMd),
        "title": name,
        "randomIndex": topics[random.randint(0,len(util.list_entries())-1)]
    })
    
def edit(request, name):
    topics = util.list_entries()
    if request.POST.get('edit'):
        util.save_entry(name, request.POST.get('edit'))
        return HttpResponseRedirect(f"/wiki/{name}")
    return render(request, 'encyclopedia/edit.html', {
        "baseText": util.get_entry(name),
        "title": name,
        "entries": topics,
        "randomIndex": topics[random.randint(0,len(util.list_entries())-1)]
    })
    
def search(request):
    topics = util.list_entries()
    res = []
    search_post = request.GET.get('q')
    if search_post:
        for entry in util.list_entries():
            if re.search(search_post.lower(), entry.lower()):
                res.append(entry)
    else:
        res.append('None')
    return render(request, "encyclopedia/search.html", {
        "res": res,
        "randomIndex": topics[random.randint(0,len(util.list_entries())-1)]
    })

def create(request):
    topics = util.list_entries()
    title = request.POST.get('title')
    if request.method == 'POST':
        if util.get_entry(title) == None:
            util.save_entry(title, request.POST.get('text'))
        else:
            return HttpResponse("This page already exists.")
        return HttpResponseRedirect(f"/wiki/{title}")
    return render(request, "encyclopedia/create.html", {
        "randomIndex": topics[random.randint(0,len(util.list_entries())-1)]
    })