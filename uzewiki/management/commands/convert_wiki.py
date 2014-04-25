"""
Convert content from other wiki formats to uzewiki 
"""
import codecs
import csv
import io
import os
import re

from django.core.management.base import BaseCommand

from uzewiki import settings
from uzewiki import utils


DOKUWIKI = 'dokuwiki'

def copycaps(to, orig):
    "Copy capitalisation from orig onto to"
    capped = []
    for i, char in enumerate(to):
        if i > len(orig):
            break
        capped.append(
            to[i].upper() if orig[i].upper() == orig[i]
            else to[i].lower()
        )
    return ''.join(capped)
    

class Converter(object):
    def __init__(self, path, **options):
        self.path = path
        self.options = options
        
        # Check path conforms to requirements
        self.path_pages = os.path.join(path, 'pages')
        self.path_assets = os.path.join(path, 'assets')
        if not os.path.isdir(self.path):
            raise ValueError('Path is not a directory')
        if not os.path.isdir(self.path_pages):
            raise ValueError('No pages directory found')
        if not os.path.isdir(self.path_assets):
            raise ValueError('No assets directory found')
    
    def convert(self):
        raise NotImplementedError
    
    
class DokuwikiConverter(Converter):
    """
    Convert a dokuwiki
    """
    #
    # Regexps for converting dokuwiki markup into pretext
    #
    
    # Inlines
    re_monospaced   = re.compile(ur"''(.+?)''", re.M)
    re_code_inline  = re.compile(
        ur'(\S[ \t]*)<(code|file)(?:[ \t]+.+?)?>[ \t]*(.+?)[ \t]*</\2>',
        re.M
    )
    re_page         = re.compile(ur'\[\[(?!https?://)(.+?)(#.*?)?(\|.+?)?\]\]', re.M)
    re_header       = re.compile(ur'^(==+)(.+?)\1$', re.M)
    re_assets       = re.compile(ur'\{\{wiki:(.+?)\}\}', re.M)
    re_images       = re.compile(ur'\{\{(.+?)\}\}', re.M)
    
    # Blocks
    re_ul           = re.compile(ur'^ {2}(\s*\*)', re.M)
    re_ol           = re.compile(ur'^ {2}(\s*)-', re.M)
    
    # Table
    re_table        = re.compile(
        ur'^(\^.*?\^[ \t]*$\n)?((?:^\|.*?\|[ \t]*$\n?)+)',
        re.M
    )
    re_row_strip    = re.compile(ur'(^\^\s*|^\|\s*|\^\s*$|\|\s*$)', re.M)
    
    # Code and file blocks
    re_code         = re.compile(
        ur'^[ \t]*?<(code|file)(?:[ \t]+(\S+?)[ \t]*)?>\s*(.+?)\s*</\1>[ \t]*?$',
        re.M | re.DOTALL
    )
    
    
    def __init__(self, *args, **kwargs):
        super(DokuwikiConverter, self).__init__(*args, **kwargs)
        
        # Build a mapping of old slugs and namespaces to new
        self.link_map = {}
        self.old_namespace = {}
        
    def convert(self):
        # Change /start.txt to index
        print "Restructuring pages..."
        self.mv_page(self.path_pages, 'start.txt', settings.FRONT_SLUG)
        self.link_map['start'] = settings.FRONT_SLUG
        self.process_pages(self.path_pages)
        
        # ++ process assets
        
        print "Converting pages..."
        self.convert_pages(self.path_pages)
    
    def slugify_path(self, path):
        """
        Convert the path into a relative slug
        """
        parts = path[len(self.path_pages):].split(os.pathsep)
        joined = '/'.join([
            utils.wikislugify(part.replace('_', ' ')) for part in parts
        ])
        return joined.strip('/')
    
    def process_pages(self, path):
        """
        Change page filenames for uzewiki
        """
        # Change /ns/start.txt to /ns.txt
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath):
                slugpath = self.slugify_path(filepath)
                startpath = self.mv_page(
                    path, 
                    os.path.join(filename, 'start.txt'),
                    filename,
                )
                if startpath:
                    self.old_namespace[startpath] = slugpath
                
                # Add to link_map
                doku_slug = ':'.join(
                    filepath[len(self.path_pages)+1:].split(os.pathsep)
                ) + ':start'
                self.link_map[doku_slug] = slugpath
                
                # Recurse through the dir
                self.process_pages(filepath)
            
            # Rename for slugs
            root, ext = os.path.splitext(filename)
            slugified = utils.wikislugify(root.replace('_', ' '))
            if root != slugified:
                newpath = os.path.join(path, slugified + ext)
                print "* Slugifying %s\n    to %s" % (filepath, newpath)
                os.rename(filepath, newpath)
                doku_slug = ':'.join(
                    filepath[len(self.path_pages)+1:].split(os.pathsep)
                )
                self.link_map[doku_slug] = self.slugify_path(filepath)
            
        
    def mv_page(self, path, filename, slug):
        """
        Try to move a page from the file to the specified slug, maintaining
        file extension.
        
        If slug already exists as .txt or .pt (or file's extension), no action
        is taken, and a warning is printed
        """
        root, ext = os.path.splitext(filename)
        filepath = os.path.join(path, filename)
        slugpath = os.path.join(path, slug)
        if not os.path.exists(filepath):
            # File doesn't exist
            return
            
        elif not os.path.isfile(filepath):
            print "Warning: cannot rename %s to %s - it is not a file" % (
                filename, slug,
            )
            
        elif (os.path.exists(slugpath + '.txt')
            or os.path.exists(slugpath + '.pt')
            or os.path.exists(slugpath + ext)
        ):
            print "Warning: %s could not be renamed - %s already exists" % (
                filename, slug,
            )
            
        else:
            # Rename
            newpath = os.path.join(slugpath + ext)
            print "* Moving %s\n    to %s" % (filepath, newpath)
            os.rename(filepath, newpath)
            return newpath
            
    
    #
    # Markup conversion
    #

    def convert_pages(self, path):
        """
        Convert pages in dokuwiki format to markuple
        This uses regexps, so some things may need fixing by hand
        """
        namespace = self.slugify_path(path)
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath):
                self.convert_pages(filepath)
            else:
                self.convert_page(
                    filepath,
                    self.old_namespace.get(filepath, namespace),
                )
    
    def convert_page(self, path, namespace):
        print "* Converting [%s] %s" % (namespace, path)
        with codecs.open(path, 'r', 'utf-8') as file:
            content = file.read()
        
        content = self.convert_content(content, namespace)
        
        with codecs.open(path, 'w', 'utf-8') as file:
            file.write(content)
    
    def convert_content(self, content, namespace):
        # Fix newlines
        content = u'\n'.join(content.splitlines())
        
        # Simple inlines ok - bold, italic, underline, link
        # Change monospaced
        content = self.re_monospaced.sub(ur'``\1``', content)
        
        # Dokuwiki <code> can appear in the middle of a line
        content = self.re_code_inline.sub(ur'\1``\3``', content)
        
        # First do pages, leaving us free to define inline blocks
        content = self.re_page.sub(
            lambda mo: u'[[%s%s%s]]' % (
                self.convert_link(mo.group(1), namespace),
                mo.group(2) or '',
                mo.group(3) or '',
            ), content
        )
        
        # Headers flip; H1 ====== to ==, H5 == to ======
        content = self.re_header.sub(
            lambda mo: u'%(chars)s%(title)s%(chars)s' % {
                'title': mo.group(2),
                'chars': u'=' * (8 - len(mo.group(1))),
            }, content
        )
        
        # Assets
        # ++ Need to match name against asset
        content = self.re_assets.sub(ur'<<asset:\1>>', content)
        
        # Images
        content = self.re_images.sub(ur'<<img:\1>>', content)
        
        # De-indent lists, and switch OL from - to #
        content = self.re_ul.sub(ur'\1', content)
        content = self.re_ol.sub(ur'\1#', content)
        
        # Convert tables
        content = self.re_table.sub(self.convert_table, content)
        
        # Explicit code and file blocks (implicit code fine)
        # ++ Not smart enough to handle a multi-line block which doesn't start
        # ++ at the start of a line
        content = self.re_code.sub(
            lambda mo: u'<<code%s\n%s\n>>' % (
                ':' + mo.group(2) if mo.group(2) else '',
                mo.group(3)
            ), content
        )
        
        # Add back newline that splitlines() will have stripped
        return content + '\n'
    
    def convert_link(self, link, namespace):
        "Updates links using self.link_map"
        # Standardise link to match link_map
        link = link.replace('_', ' ')
        lower = link.lower()
        
        if namespace and ':' not in link:
            link = namespace + ':' + link
            lower = namespace + ':' + lower
        
        if link.startswith(':'):
            link = link[1:]
            lower = lower[1:]
        
        if lower in self.link_map:
            return copycaps(self.link_map[lower], link)
            
        # Otherwise namespaces are dirs now
        return link.replace(':', '/')
    
    def convert_table(self, mo):
        "Convert a table"
        header = mo.group(1).replace('^', '|') + '\n' if mo.group(1) else ''
        stripped = self.re_row_strip.sub('', u'%s%s' % (header, mo.group(2)))
        
        output = io.BytesIO()
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(
            [
                [cell.strip() for cell in row.split('|')]
                for row in stripped.encode("utf-8").splitlines()
            ]
        )
        return u'<<table\n%s>>\n' % output.getvalue().decode("utf-8")
        
        
class Command(BaseCommand):
    """
    Convert content from other wiki formats to uzewiki
    
    Pass two arguments:
        type    Type of source wiki; one of:
                    docuwiki
        path    Path to dump of other wiki; should be a directory containing
                two directories, pages and assets. See documentation for how
                to create these dumps.
    """
    help = 'Convert content from other wiki formats to uzewiki'
    
    def handle(self, source_type, path, **options):
        # Hand off to wiki-specific handlers
        if source_type.lower() == DOKUWIKI:
            converter = DokuwikiConverter(path, **options)
        else:
            raise ValueError('Unknown source wiki type')
        
        converter.convert()
    
