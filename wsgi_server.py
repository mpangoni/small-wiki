
import re
import cgi


import content

from string import Template
from wsgiref.simple_server import make_server

def send_template(template_name, values):
    template = open(template_name).read()
    content = Template(template).substitute(values)
    response = [content.encode()]

    return "text/html", len(content), response

def parse_environ(environ):
    post_env = environ.copy()
    post_env['QUERY_STRING'] = ''

    context = cgi.FieldStorage(fp=environ['wsgi.input'], environ=post_env, keep_blank_values=True)
    context.path = environ.get('PATH_INFO','') 

    if re.match(r'.*\/$', context.path):
        context.path = context.path + "index.html"

    return context


def small_wiki_app(environ, start_response):

    context = parse_environ(environ)
    
    matched_call = re.match(r'.*\/(.+)\.wsgi', context.path )
    
    #requested resource is a functionality    
    if matched_call:
        method = getattr(content, matched_call.group(1))
        code, headers, response = method( context )
        
    #requested resource is a file ?
    elif content.is_content(context):
        code, headers, response = content.send_content(context)                

    #default create content page   
    else:
        code, headers, response = content.new_content( context )        
    
    start_response(code, headers)
    return response
    
if __name__ == '__main__':
                         
    httpd = make_server('', 8000, small_wiki_app)
    print("Serving on port 8000...")

    # Serve until process is killed
    httpd.serve_forever()
