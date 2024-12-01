import random, markdown2
from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_page(request, title):
    content_markdown = util.get_entry(title)
    if content_markdown:
        content_html = markdown2.markdown(content_markdown)
        return render(request, "encyclopedia/render.html", {
            "content": content_html,
            "title": title 
        })
    else:
        return render(request, "encyclopedia/render_error.html", {
            "title": title
        })

def search_page(request):
    if request.method == "POST":
        search = request.POST.get('q')
        content = util.get_entry(search)
        if content:
            return redirect("render_page", title=search)
        else:
            entries = util.list_entries()
            results = [entry for entry in entries if search.lower() in entry.lower()]
            return render(request, "encyclopedia/search_results.html", {
                "query": search,
                "results": results
            })
        
def new_page(request):
    if request.method == "POST":
        title = request.POST.get('pageTitle')
        content = request.POST.get('markdownContent')
        entries = util.list_entries()
        if title and content:
            if any(entry.lower() == title.lower() for entry in entries):
                return render(request, "encyclopedia/newpage_error.html", {
                    "title": title.capitalize()
                })
            else:
                util.save_entry(title, content)
                return redirect("render_page", title=title)
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
        title = request.POST.get("pageTitle")
        content = request.POST.get("markdownContent")

        if title and content:
            # Update Entry
            util.save_entry(title, content)
            # Redirect to Render the Page
            return redirect("render_page", title=title)
        
        # Fetch the content to prefill the Text area
    content = util.get_entry(title)
    if content is None:
        return render("encyclopedia/render_error.html", title=title)
        
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect("render_page", title=random_title)
    else:
        return render(request, "encyclopedia/render_error.html", {
            "title": ""
        })