from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from . import app_settings, archive, forms, models
from .decorators import edit_required, get_wiki, permission_required, read_required
from .utils import reverse_to_asset, reverse_to_page, title_from_path


@permission_required(app_settings.PERM_INDEX)
def index(request):
    """
    Index redirects to /index/
    """
    # Get all wikis that the user is allowed to read
    wikis = []
    for wiki in models.Wiki.objects.all():
        if wiki.can_read(request.user):
            wikis.append(wiki)

    return render(
        request,
        "powerwiki/index.html",
        {"title": "Available Wikis", "wikis": wikis, "body_class": "powerwiki_index"},
    )


@get_wiki
@read_required
def page(request, wiki, wiki_slug, page_path=None):
    """
    Show a wiki page
    """
    # Enforce canonical paths
    if page_path and page_path != page_path.lower():
        return HttpResponseRedirect(
            reverse_to_page("powerwiki:page", wiki_slug, page_path.lower())
        )

    # Hide the page path
    if not page_path:
        page_path = app_settings.FRONT_PATH

    # Look up page
    try:
        page = models.Page.objects.get(wiki=wiki, path=page_path)
        title = page.full_title()
    except models.Page.DoesNotExist:
        page = None
        title = "New page: %s" % title_from_path(page_path)

    if wiki.can_edit(request.user):
        edit_url = reverse_to_page("powerwiki:page-edit", wiki_slug, page_path)

    else:
        edit_url = None

    # Prepare page content
    return render(
        request,
        "powerwiki/show.html",
        {
            "page": page,
            "title": title,
            "wiki_slug": wiki_slug,
            "breadcrumbs": wiki.gen_breadcrumbs(page_path),
            "edit_url": edit_url,
            "body_class": "powerwiki_show",
        },
        status=404 if not page else None,
    )


@get_wiki
@read_required
def search(request, wiki, wiki_slug):
    """
    Search a wiki
    """
    query = request.GET.get("q", "").strip()
    pages = wiki.search(query)

    return render(
        request,
        "powerwiki/search.html",
        {
            "title": "Search",
            "wiki_slug": wiki_slug,
            "breadcrumbs": wiki.gen_breadcrumbs(app_settings.FRONT_PATH)
            + [{"title": "Search", "class": "", "url": ""}],
            "search_query": query,
            "pages": pages,
            "body_class": "powerwiki_search",
        },
    )


@get_wiki
@edit_required
def page_edit(request, wiki, wiki_slug, page_path):
    """
    Edit a wiki page
    """
    # Page paths must always be lower case
    if page_path != page_path.lower():
        return HttpResponseRedirect(
            reverse_to_page("powerwiki:page-edit", wiki_slug, page_path.lower())
        )

    # Look up page
    try:
        page = models.Page.objects.get(wiki=wiki, path=page_path)
    except models.Page.DoesNotExist:
        page = None

    # Save or display form
    if request.method == "POST":
        if page:
            form = forms.PageForm(request.POST, instance=page)
        else:
            form = forms.PageForm(request.POST)

        if form.is_valid():
            # Check wiki hasn't been modified in the form
            if form.cleaned_data["wiki"] != wiki:
                # Don't worry about being helpful - this is a deliberate
                # attempt to subvert the authentication system
                messages.error(request, "Trying to save to invalid wiki.")
            elif not form.cleaned_data["content"].strip():
                page.delete()
                messages.success(request, "Page deleted.")
                return HttpResponseRedirect(
                    reverse_to_page("powerwiki:page", wiki_slug)
                )
            else:
                form.save()
                messages.success(request, "Page saved.")
                return HttpResponseRedirect(
                    reverse_to_page("powerwiki:page", wiki_slug, page_path)
                )
        else:
            messages.error(request, "Error processing form.")

    else:
        if page:
            form = forms.PageForm(instance=page)
        else:
            form = forms.PageForm(
                initial={
                    "wiki": wiki,
                    "title": title_from_path(page_path),
                    "path": page_path,
                }
            )

    return render(
        request,
        "powerwiki/edit.html",
        {
            "form": form,
            "title": "Edit page: %s" % page_path,
            "breadcrumbs": wiki.gen_breadcrumbs(page_path) + [{"title": "Edit page"}],
            "show_url": reverse_to_page("powerwiki:page", wiki_slug, page_path),
            "body_class": "powerwiki_edit",
        },
    )


@get_wiki
@edit_required
def wiki_import(request, wiki, wiki_slug):
    """
    Import a wiki
    """
    if request.method == "POST":
        form = forms.ImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Wipe
            if form.cleaned_data["wipe"]:
                wiki.pages.all().delete()

            # Import
            try:
                archive.import_zip(wiki, request.FILES["file"])
            except archive.ZipImportError as e:
                messages.error(request, "Wiki could not be imported: %s" % e)
            else:
                messages.success(request, "Wiki imported")
                return HttpResponseRedirect(
                    reverse_to_page("powerwiki:page", wiki_slug)
                )
    else:
        form = forms.ImportForm()

    return render(
        request,
        "powerwiki/import.html",
        {
            "form": form,
            "title": "Import wiki: %s" % wiki_slug,
            "show_url": reverse_to_page("powerwiki:page", wiki_slug),
            "body_class": "powerwiki_import",
        },
    )


@get_wiki
@read_required
def asset(request, wiki, wiki_slug, asset_name):
    """
    Show asset details
    """
    # Asset slugs must always be lower case
    if asset_name != asset_name.lower():
        return HttpResponseRedirect(
            reverse_to_asset("powerwiki:asset", wiki_slug, asset_name.lower())
        )

    # Get asset
    asset = get_object_or_404(wiki.assets, name=asset_name)

    return redirect(asset.get_media_url())


@get_wiki
@edit_required
def asset_edit(request, wiki, wiki_slug, asset_name):
    """
    Edit an asset
    """
    # Asset slugs must always be lower case
    if asset_name != asset_name.lower():
        return HttpResponseRedirect(
            reverse_to_asset("powerwiki:asset", wiki_slug, asset_name.lower())
        )

    # Look up asset
    initial = {}
    try:
        asset = models.Asset.objects.get(wiki=wiki, name=asset_name)
    except models.Asset.DoesNotExist:
        asset = None
        initial = {
            "wiki": wiki,
            "name": asset_name,
        }

    # Save or display form
    if request.method == "POST":
        form = forms.AssetForm(request.POST, request.FILES, instance=asset)

        if form.is_valid():
            # Check wiki hasn't been modified in the form
            if form.cleaned_data["wiki"] != wiki:
                # Don't worry about being helpful - this is a deliberate
                # attempt to subvert the authentication system
                messages.error(request, "Trying to save to invalid wiki.")
            else:
                asset = form.save()
                messages.success(request, "Asset saved.")
                return HttpResponseRedirect(
                    reverse_to_asset("powerwiki:asset", wiki_slug, asset_name)
                )
        else:
            messages.error(request, "Error processing form.")

    else:
        form = forms.AssetForm(initial=initial, instance=asset)

    breadcrumbs = wiki.gen_breadcrumbs()
    if asset:
        breadcrumbs += [{"title": "Asset", "url": asset.get_absolute_url()}]
    breadcrumbs += [{"title": "Edit asset"}]

    return render(
        request,
        "powerwiki/asset_edit.html",
        {
            "form": form,
            "title": "Edit asset %s" % asset_name,
            "breadcrumbs": breadcrumbs,
            "body_class": "powerwiki_asset_edit",
        },
    )
