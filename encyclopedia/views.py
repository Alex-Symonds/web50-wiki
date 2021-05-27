from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/error.html",{
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry_contents": entry
        })

def search(request):
    search_term = request.GET.get("q", "")

    entry = util.get_entry(search_term)
    if entry == None:
        return render(request, "encyclopedia/results.html", {
            "search_term": search_term,
            "entries": [e for e in util.list_entries() if search_term.lower() in util.get_entry(e).lower()]
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": search_term,
            "entry_contents": entry
        })      


    







