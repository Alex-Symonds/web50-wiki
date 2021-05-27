from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry_contents": entry
        })

    return render(request, "encyclopedia/error.html",{
        "title": title
    })

def search(request):
    search_term = request.GET.get("q", "")
    entry = util.get_entry(search_term)

    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": search_term,
            "entry_contents": entry
        })

    return render(request, "encyclopedia/results.html", {
        "search_term": search_term,
        "entries": [e for e in util.list_entries() if search_term.lower() in util.get_entry(e).lower()]
    })    

def create_new(request):

    if request.method == "POST":
        new_input = request.POST

        # Check if the article already exists
        if new_input["new_title"].lower() in (t.lower() for t in util.list_entries()):
            return render(request, "encyclopedia/exists.html", {
                "title": new_input["new_title"]
            })
        
        # Save it, then redirect the user to it
        util.save_entry(new_input["new_title"], new_input["new_content"])
        url = reverse("entry", kwargs={'title': new_input["new_title"]})
        return HttpResponseRedirect(url)
 
    return render(request, "encyclopedia/create.html")

    







