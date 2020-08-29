"""
Wiki archive management
"""
import os
import zipfile

from django.core.files.uploadedfile import InMemoryUploadedFile

from . import models
from .utils import title_from_path


TITLE_PREFIX = "TITLE: "


class ZipImportError(Exception):
    pass


def import_zip(wiki, file):
    """
    Import a zip into a wiki
    Zip should contain two directories:
        pages
            page.txt            # path: page
            page
                subpage.txt     # path: page/subpage
        assets
            internal_id.jpg

    Page extensions must be .txt or .md - both are treated as pretext format
    Asset extensions should indicate filetype.

    Page titles are expected on the first line, with the prefix "TITLE: "; if
    the first line does not match this format, it will be considered to be part
    of the content, and the title will be based on the path.

    These can optionally be held inside a directory whose name matches the zip,
    for example:

        mywiki.zip
            mywiki
                pages
                assets
    """
    # Test filename
    zipname, ext = os.path.splitext(file.name)
    if (
        not isinstance(file, InMemoryUploadedFile)
        and not zipfile.is_zipfile(file.temporary_file_path)
    ) or ext.lower() != ".zip":
        raise ZipImportError("File is not a zip file")

    # Open the zip file
    try:
        zf = zipfile.ZipFile(file)
    except zipfile.BadZipFile as e:
        raise ZipImportError("Bad zip file: %s" % e)
    except zipfile.LargeZipFile:
        raise ZipImportError("Bad zip file: ZIP64 not enabled")
    filenames = [info.filename for info in zf.infolist()]

    # Check the zip for optional root container
    path_con = zipname + "/"
    path_pages = "pages/"
    path_assets = "assets/"
    if path_con in filenames:
        path_pages = path_con + path_pages
        path_assets = path_con + path_assets

    # Check the structure of the zip
    if path_pages not in filenames:
        raise ZipImportError("Pages directory not found")
    if path_assets not in filenames:
        raise ZipImportError("Assets directory not found")

    # Import the pages
    pages = [filename for filename in filenames if filename.startswith(path_pages)]
    for filename in pages:
        # Find page path and read content
        page_path, ext = os.path.splitext(filename[len(path_pages) :])
        if ext.lower() not in [".txt", ".pt"]:
            continue
        content = zf.read(filename)

        # Get or create Page
        try:
            page = models.Page.objects.get(wiki=wiki, path=page_path)
        except models.Page.DoesNotExist:
            page = models.Page(wiki=wiki, path=page_path)

        # Set title and content
        lines = content.splitlines()
        if lines and lines[0].startswith(TITLE_PREFIX):
            page.title = lines.pop(0)[TITLE_PREFIX:].strip()
        else:
            page.title = title_from_path(page_path)
        page.content = "\n".join(lines)
        page.save()


def export_zip(wiki):
    """
    Export a wiki into a zip, returning the file object
    """
    raise NotImplementedError()
