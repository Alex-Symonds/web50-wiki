from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Grab the entry and display it
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry_contents": entry
        })

    # Show an error page
    return render(request, "encyclopedia/error.html",{
        "title": title
    })

def search(request):
    search_term = request.GET.get("q", "")
    
    # If the search term is the exact title of a page, redirect
    if search_term.lower() in (t.lower() for t in util.list_entries()):
        return HttpResponseRedirect(reverse("entry", kwargs={'title': search_term}))

    # Otherwise show a list of pages containing the search term as a substring
    return render(request, "encyclopedia/results.html", {
        "search_term": search_term,
        "entries": [e for e in util.list_entries() if search_term.lower() in util.get_entry(e).lower()]
    })

def create_new(request):
    # POST = try to add the new entry
    if request.method == "POST":
        new_input = request.POST

        # Check if the article already exists
        if new_input["new_title"].lower() in (t.lower() for t in util.list_entries()):
            return render(request, "encyclopedia/exists.html", {
                "title": new_input["new_title"]
            })
        
        # Save it, then redirect the user to it
        util.save_entry(new_input["new_title"], new_input["new_content"].replace("\r", ""))
        return HttpResponseRedirect(reverse("entry", kwargs={'title': new_input["new_title"]}))
 
    # GET = show the create page
    return render(request, "encyclopedia/create.html")

def edit(request):

    if request.method == "POST":
        util.save_entry(request.POST["edit_title"], request.POST["edit_content"].replace("\r", ""))
        return HttpResponseRedirect(reverse("entry", kwargs={'title': request.POST["edit_title"]}))       

    title = request.GET.get("t", "")
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry_contents": util.get_entry(title)
    })

