from django.contrib import messages
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render as django_render

try:
    from simple_search import perform_search
except ImportError:
    perform_search = None

from uzewiki import archive
from uzewiki import constants
from uzewiki import forms
from uzewiki import models
from uzewiki import settings
from uzewiki.decorators import (
    get_wiki, permission_required, read_required, edit_required,
)
from uzewiki.utils import reverse_to_page, reverse_to_asset, title_from_slug
from uzewiki.markuplext import parser as markuple_parser

def render(request, template, dct, **kwargs):
    "Inject uzewiki settings into template render"
    dct['uzewiki_settings'] = {
        'add_jquery':   settings.ADD_JQUERY,
    }
    return django_render(request, template, dct, **kwargs)


@permission_required(settings.PERM_INDEX)
def index(request):
    """
    Index redirects to /index/
    """
    # Get all wikis that the user is allowed to read
    wikis = []
    for wiki in models.Wiki.objects.all():
        if wiki.can_read(request.user):
            wikis.append(wiki)
    
    return render(request, 'uzewiki/index.html', {
        'title':    'Available Wikis',
        'wikis':    wikis,
    })


@get_wiki
@read_required
def show(request, wiki, wiki_slug, page_slug=None):
    """
    Show a wiki page
    """
    # Enforce canonical slugs
    if page_slug and page_slug != page_slug.lower():
        return HttpResponseRedirect(
            reverse_to_page('uzewiki-show', wiki_slug, page_slug.lower())
        )
    
    # Hide the page slug
    if not page_slug:
        page_slug = settings.FRONT_SLUG
    
    # Look up page
    try:
        page = models.Page.objects.get(wiki=wiki, slug=page_slug)
        title = page.full_title()
    except models.Page.DoesNotExist:
        page = None
        title = 'New page: %s' % title_from_slug(page_slug)
        
    if wiki.can_edit(request.user):
        edit_url = reverse_to_page('uzewiki-edit', wiki_slug, page_slug)
            
    else:
        edit_url = None
    
    # Prepare page content
    return render(request, 'uzewiki/show.html', {
        'page':     page,
        'title':    title,
        'wiki_slug': wiki_slug,
        'breadcrumbs': wiki.gen_breadcrumbs(page_slug),
        'edit_url': edit_url,
        'mu_parser':    markuple_parser,
        'mu_context':   {
            'page': page,
            'wiki': wiki,
        },
    }, status=404 if not page else None,)
    

@get_wiki
@read_required
def search(request, wiki, wiki_slug):
    """
    Search a wiki
    """
    query = request.GET.get('q', '').strip()
    
    if perform_search is None:
        pages = []
    else:
        pages = perform_search(
            query,
            wiki.pages.all(),
            ['title', 'content'],
        )
    
    return render(request, 'uzewiki/search.html', {
        'title':    'Search' if perform_search is not None else 'Search unavailable',
        'wiki_slug': wiki_slug,
        'breadcrumbs': wiki.gen_breadcrumbs(settings.FRONT_SLUG) + [{
            'title':    'Search',
            'class':    '',
            'url':      '',
        }],
        'search_query': query,
        'pages': pages,
    })
    

@get_wiki
@edit_required
def edit(request, wiki, wiki_slug, page_slug):
    """
    Edit a wiki page
    """
    # Page slugs must always be lower case
    if page_slug != page_slug.lower():
        return HttpResponseRedirect(
            reverse_to_page('uzewiki-edit', wiki_slug, page_slug.lower())
        )
    
    # Look up page
    try:
        page = models.Page.objects.get(wiki=wiki, slug=page_slug)
    except models.Page.DoesNotExist:
        page = None
        
    # Save or display form
    if request.method == 'POST':
        if page:
            form = forms.PageForm(request.POST, instance=page)
        else:
            form = forms.PageForm(request.POST)
        
        if form.is_valid():
            # Check wiki hasn't been modified in the form
            if form.cleaned_data['wiki'] != wiki:
                # Don't worry about being helpful - this is a deliberate
                # attempt to subvert the authentication system
                messages.error(request, 'Trying to save to invalid wiki.')
            else:
                form.save()
                messages.success(request, 'Page saved.')
                return HttpResponseRedirect(
                    reverse_to_page('uzewiki-show', wiki_slug, page_slug)
                )
        else:
            messages.error(request, 'Error processing form.')
    
    else:
        if page:
            form = forms.PageForm(instance=page)
        else:
            form = forms.PageForm(initial={
                'wiki':     wiki,
                'title':    title_from_slug(page_slug),
                'slug':     page_slug,
            })
        
    return render(request, 'uzewiki/edit.html', {
        'form': form,
        'title': 'Edit page: %s' % page_slug,
        'breadcrumbs': wiki.gen_breadcrumbs(page_slug) + [{
            'title':    'Edit page',
        }],
        'show_url': reverse_to_page('uzewiki-show', wiki_slug, page_slug)
    })


@get_wiki
@edit_required
def wiki_import(request, wiki, wiki_slug):
    """
    Import a wiki
    """
    if request.method == 'POST':
        form = forms.ImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Wipe
            if form.cleaned_data['wipe']:
                wiki.pages.all().delete()
            
            # Import
            try:
                archive.import_zip(wiki, request.FILES['file'])
            except archive.ZipImportError, e:
                messages.error(request, 'Wiki could not be imported: %s' % e)
            else:
                messages.success(request, 'Wiki imported')
                return HttpResponseRedirect(
                    reverse_to_page('uzewiki-show', wiki_slug)
                )
    else:
        form = forms.ImportForm()
        
    return render(request, 'uzewiki/import.html', {
        'form': form,
        'title': 'Import wiki: %s' % wiki_slug,
        'show_url': reverse_to_page('uzewiki-show', wiki_slug)
    })


@get_wiki
@read_required
def asset_details(request, wiki, wiki_slug, asset_name):
    """
    Show asset details
    """
    # Asset slugs must always be lower case
    if asset_name != asset_name.lower():
        return HttpResponseRedirect(
            reverse_to_asset('uzewiki-asset', wiki_slug, asset_name.lower())
        )
    
    # Get asset
    asset = get_object_or_404(wiki.assets, name=asset_name)
    
    if wiki.can_edit(request.user):
        edit_url = reverse_to_asset('uzewiki-asset-edit', wiki_slug, asset_name)
    else:
        edit_url = None
    
    # Prepare page content
    return render(request, 'uzewiki/asset_details.html', {
        'wiki_slug': wiki_slug,
        'title':    'Asset: %s' % asset_name,
        'breadcrumbs': wiki.gen_breadcrumbs() + [{
            'title':    'Asset',
        }],
        'asset':    asset,
        'edit_url': edit_url,
        'edit_label': 'Edit asset',
    })
    

@get_wiki
@edit_required
def asset_edit(request, wiki, wiki_slug, asset_name):
    """
    Edit an asset
    """
    # Asset slugs must always be lower case
    if asset_name != asset_name.lower():
        return HttpResponseRedirect(
            reverse_to_asset('uzewiki-asset', wiki_slug, asset_name.lower())
        )
    
    # Look up asset
    initial = {}
    try:
        asset = models.Asset.objects.get(wiki=wiki, name=asset_name)
    except models.Asset.DoesNotExist:
        asset = None
        initial = {
            'wiki': wiki,
            'name': asset_name,
        }
        
    # Save or display form
    if request.method == 'POST':
        form = forms.AssetForm(request.POST, request.FILES, instance=asset)
        
        if form.is_valid():
            # Check wiki hasn't been modified in the form
            if form.cleaned_data['wiki'] != wiki:
                # Don't worry about being helpful - this is a deliberate
                # attempt to subvert the authentication system
                messages.error(request, 'Trying to save to invalid wiki.')
            else:
                asset = form.save()
                messages.success(request, 'Asset saved.')
                return HttpResponseRedirect(
                    reverse_to_asset('uzewiki-asset', wiki_slug, asset_name)
                )
        else:
            messages.error(request, 'Error processing form.')
    
    else:
        form = forms.AssetForm(initial=initial, instance=asset)
    
    breadcrumbs = wiki.gen_breadcrumbs()
    if asset:
        breadcrumbs += [{
            'title':    'Asset',
            'url':      asset.get_absolute_url(),
        }]
    breadcrumbs += [{
        'title':    'Edit asset',
    }]
    
    return render(request, 'uzewiki/asset_edit.html', {
        'form':     form,
        'title':    'Edit asset %s' % asset_name,
        'breadcrumbs': breadcrumbs,
    })