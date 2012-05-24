
import os

import mimetypes
import posixpath

import markme

from string import Template
from datetime import datetime
from wsgiref.util import FileWrapper

_CONTENT_ROOT = "./contents{0}"

_ROOT = ".{0}"

if not mimetypes.inited:
    mimetypes.init() # try to read system mime.types

def guess_mimetype(path):
    base, ext = posixpath.splitext(path)

    types_map = getattr(mimetypes, 'types_map')
    
    if ext in types_map:
        return types_map[ext]

    ext = ext.lower()
    if ext in types_map:
        return types_map[ext]
    else:
        return types_map['']


def apply_template(name, values):
    
    template = open( './templates/{0}.pst'.format(name) ).read()
    return Template(template).substitute(values)

def is_content(context):
    return os.path.isfile(_CONTENT_ROOT.format(context.path)) or os.path.isfile(_ROOT.format(context.path))

def default_response(content, mimetype='text/html; charset=utf-8'):
    response = [content.encode()]
    return "200 OK", [("Content-type", mimetype),("Content-length", str(response))], response

def send_content(context):


    path = _CONTENT_ROOT.format(context.path)    

    if not os.path.isfile(path):
        path = _ROOT.format(context.path)
    
    size = os.path.getsize(path)
    mimetype = guess_mimetype(path)

    if mimetype == 'text/html':
        mimetype += '; charset=utf-8'

    return "200 OK" , [("Content-type", mimetype),("Content-length", str(size))], FileWrapper(open(path, mode='rb'))
 
def new_content(context):
    
    content = apply_template('content_editor', dict({'resource':context.path, 'content':''}))
    return default_response(content)

def store_content(context):
    
    path = _CONTENT_ROOT.format(context.getvalue("resource"))
    directory = os.path.dirname(path)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(path,  mode='wb') as html_resource, open(path + '.txt', mode='wb') as txt_resource:
        content = context.getvalue('content')
        
        if content and len(content) > 0:
            html_content = apply_template('content_viwer', dict({'resource':context.getvalue("resource"), 'content':markme.mark_me(content), 'timestamp':datetime.now().isoformat(' ')}))
            html_resource.write(html_content.encode())
            txt_resource.write(content.encode())            

        html_resource.close()
        txt_resource.close()
        
    return '301 Moved Permanently', [('Location', context.getvalue("resource")) ], [] 

def update_content(context):
    
    path = _CONTENT_ROOT.format(context.getvalue("resource"))
    
    content = apply_template('content_editor', dict({'resource':context.getvalue("resource"), 'content':open(path + '.txt', encoding='utf-8' ,mode='r').read()}))
    print(len(content));
    return default_response(content)    
