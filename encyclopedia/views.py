# Returns what's in a page.
from django.shortcuts import render

# imports utils file
from . import util

# Import mark down to convert markdown content to html before displaying it
from markdown2 import Markdown

# Import form class from forms.py
from . forms import New

# import secret library to choose secretly an entry page
import secrets


# Index page func
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# entry page func
# get the entry name from urls.py as parameter of the func
def entry(request, entry):
    markConverter = Markdown()
    # get the entry content  by inserting it as parameter in util.get_entry()
    page = util.get_entry(entry)

    # if page is none(don't exist) then return page do not exist
    if page is None:
        return render(request, "encyclopedia/NotExist.html", {
            "entryTitle": entry  # entry = the title of the page requested
        })

    # Otherwise the page exist , display it
    else:
        return render(request, "encyclopedia/exist.html", {
            "try": entry,  # entry = the title of the page requested
            # content = convert page requested to html
            "content": markConverter.convert(page)
        })


# A function to get query from the search bar,
# then process, if the query name exist it
# redirect to the entry page, otherwise it will
# display a list of entries that have the
# query as a substring, by clicking on any of the
# list, it should display the entry page.


def search(request):
    query = request.POST.get('q', '')
    page = util.get_entry(query)
    markConverter = Markdown()

    if page is not None:
        # if query exist as an entry then display it
        return render(request, "encyclopedia/exist.html", {
            "try": query,  # entry = the title of the page requested
            # content = convert page requested to html
            "content": markConverter.convert(page)
        })
    else:
        # else it doesn't exist as an entry, therefore
        # display All entries with query as substring.
        querySubstring = []
        for sub in util.list_entries():
            if query.lower() in sub.lower():
                query.lower() == sub.lower()
                querySubstring.append(sub)
        return render(request, "encyclopedia/index.html", {
            "contents": querySubstring,
            "search": True,
            "try": query
        })


""" Create a func that get data from a form
to create new entry"""


def new_entry(request):
    # convert entry to html markup
    markConverter = Markdown()
    # Setting method to post ensure it to be the only way to alter the data
    if request.method == "POST":
        # gets content from form
        form = New(request.POST)
        # checks if form content satisfy all requirement
        if form.is_valid():
            # form fields: title and entry content
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # get the page by its title
            page = util.get_entry(title)
            # Ensures the page don't exist or wether we are editing
            # it by passing the new/editing page title to 'util.get_entry()',
            # if that's true then it save the page with the new content,
            # else it will render error message that the page exist .
            if (page is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return render(request, "encyclopedia/exist.html", {
                    # entry = the title of the page requested
                    "try": title,
                    # content = convert page requested to html
                    "content": markConverter.convert(content)
                })
            else:
                # If above condition aren't met error is displayed
                return render(request, "encyclopedia/entry_Form.html", {
                    # return the newly added data that didn't,
                    # met up the above conditions.
                    "form": form,
                    "existing": True,  # this is to flag out that the page exist
                    "entry": title
                })
        else:
            # If form is not valid display
            return render(request, "encyclopedia/entry_Form.html", {
                "form": form,  # return the form as it is
                "existing": False,  # flags out the title don't exist
            })
    else:
        # Otherwise represent a new form fields.
        return render(request, "encyclopedia/entry_Form.html", {
            "form": New(),  # returns new page
            "existing": False  # flags out page don't exist.
        })


# edit function edits when edit button is clicked.
# get the entry title to be edited from urls.py
def edit(request, entryEdit):
    # get the entry content by passing
    # through util.get_entry func
    page = util.get_entry(entryEdit)
    # display new form
    form = New()
    # populate the form with: entry title & content
    form.fields["title"].initial = entryEdit
    form.fields["content"].initial = page
    # flag edit flag to true .
    form.fields["edit"].initial = True
    return render(request, "encyclopedia/entry_Form.html", {
        "form": form,
        "edit": form.fields["edit"].initial,
        "entryTitle": form.fields["title"].initial
    })


# randomPage func displays secretly random entries
# using secret library,
# when page is clicked in the home page
def randomPage(request):
    markConverter = Markdown()
    page = util.list_entries()
    # secretly choice an entry by its title
    anyPage = secrets.choice(page)
    # Takes the title of the secretly chosen entry,
    # and displays it content.
    content = util.get_entry(anyPage)

    return render(request, "encyclopedia/exist.html", {
        "content": markConverter.convert(content),
        "try": anyPage,
        "random": True
    })
