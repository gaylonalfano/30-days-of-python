import typing as t

"""
NOTES:
    - Whenever you use a web app you're going to have an app
      that's going to actually handle that application...?
      This app is just a simple function or could be a Class that
      has a method in it to accept a REQUEST and return a RESPONSE.
    - Gunicorn is our web server gateway interface (WSGI). Gunicorn
      will handle the request for us and it'll look for our function (app)
      that will handle the requests. Think of gunicorn as the middleman
      between the server and the Python app.
    - Gunicorn passes two variables to our app:
        def app(environ, start_response).
    - start_response is a method you can call to have some sort of response
      going/running. It takes in these args: status_code, headers, content
      length (bytes), and we need to return an iterable (list) of the
      response object.
    - Start the server using 'gunicorn server:app --reload'
    - Routing is totally ignored with a barebones app. We can handle other
      routes by adjusting the 'environ' argument that Gunicorn passes to
      our app (function). 'environ' is a Dict object. Gunicorn calls it
      'environ' but other servers may call it something else.
    - Exploring the 'environ' Dict, we see QUERY_STRING, PATH_INFO,
      HTTP_ACCEPT, etc.
    - The PATH_INFO (/hello) doesn't change when adding a query string
      (?query=hi there). The RAW_URI does update.
    - Can use F-strings like {path=} which prints: path='/hello-world'
    - ?? Where does 'index.html' come from? **When I default path="/"
      my render_template() function returned f"<h1>Hello {path=}</h1>"].
      So why doesn't 404 render when path='/abc/howdy/' ?
      **SOLVED: It's because I'm handling all paths the same way! If I
      render the template_name then I see the '404.html' displayed for all
      paths excluding the root path!
    - The 'data' variable can point to HTML files/templates, open/read the
      contents, and store the HTML. Then data is encoded to byte string
      and our app (function) returns an iterable of a list with data inside
      i.e., iter([data])  <list_iterator object at 0x10f9f1340>
    - Rendering different templates is fine. However, if we want to render
      the path if it's valid, then we use 'context' Dict in render_template()
      If we added a '{path}' inside 404.html then say we have a kwarg in
      context Dict of "path": "abc", then "abc" would render inside 404.html.
      This is because we render the HTML to a STRING and replace any context
      value (path="howdy") inside the HTML STRING using .format(**context)
    - To handle more routes, ideally we write some helper functions that
      handle multiple routes (instead of our current two: "/" or all other).
      Can have a homepage(environ) helper function (route handler).
    - You can deploy this to a host and then it's live to the public. Could use
      ngrok to create some live links for others to see.

CHALLENGE:
    - Could leverage CSV storage (instead of a full DB) and then
      try to render things to these different routes.



ENVIRON.items() shows details of REQUEST object:
    REQUEST_METHOD GET
QUERY_STRING
RAW_URI /
SERVER_PROTOCOL HTTP/1.1
HTTP_HOST localhost:8000
HTTP_CONNECTION keep-alive
HTTP_CACHE_CONTROL max-age=0
HTTP_UPGRADE_INSECURE_REQUESTS 1
HTTP_USER_AGENT Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/84.0.4147.105 Safari/537.36
HTTP_ACCEPT text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,appli
cation/signed-exchange;v=b3;q=0.9
HTTP_SEC_FETCH_SITE none
HTTP_SEC_FETCH_MODE navigate
HTTP_SEC_FETCH_USER ?1
HTTP_SEC_FETCH_DEST document
HTTP_ACCEPT_ENCODING gzip, deflate, br
HTTP_ACCEPT_LANGUAGE en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
HTTP_COOKIE _ga=GA1.1.87577474.1573965214
wsgi.url_scheme http
REMOTE_ADDR 127.0.0.1
REMOTE_PORT 53331
SERVER_NAME 127.0.0.1
SERVER_PORT 8000
PATH_INFO /
SCRIPT_NAME
wsgi.errors <gunicorn.http.wsgi.WSGIErrorsWrapper object at 0x10f9e5670>
wsgi.version (1, 0)
wsgi.multithread False
wsgi.multiprocess False
wsgi.run_once False
wsgi.file_wrapper <class 'gunicorn.http.wsgi.FileWrapper'>
wsgi.input_terminated True
SERVER_SOFTWARE gunicorn/20.0.4
wsgi.input <gunicorn.http.body.Body object at 0x10f9f0070>
gunicorn.socket <socket.socket fd=9, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0
, laddr=('127.0.0.1', 8000), raddr=('127.0.0.1', 53333)>
REQUEST_METHOD GET
QUERY_STRING
RAW_URI /
SERVER_PROTOCOL HTTP/1.1
HTTP_HOST localhost:8000
HTTP_CONNECTION keep-alive
HTTP_USER_AGENT Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/84.0.4147.105 Safari/537.36
HTTP_ACCEPT */*
HTTP_SEC_FETCH_SITE none
HTTP_SEC_FETCH_MODE cors
HTTP_SEC_FETCH_DEST empty
HTTP_ACCEPT_ENCODING gzip, deflate, br
HTTP_ACCEPT_LANGUAGE en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
HTTP_COOKIE _ga=GA1.1.87577474.1573965214
wsgi.url_scheme http
REMOTE_ADDR 127.0.0.1
REMOTE_PORT 53333
SERVER_NAME 127.0.0.1
SERVER_PORT 8000
PATH_INFO /
SCRIPT_NAME
"""

# ====== Advanced: Handling MULTIPLE routes with helper functions
# gunicorn
def render_template(
    template_name: str = "index.html", context: t.Dict[str, str] = {}
):
    """
    Render HTML instead of plain text. This will now
    be the 'data/payload' that we send.

    We read the template_name file's HTML and return that HTML.
    """
    html_str: str
    with open(template_name, "r") as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str
    # return f"<h1>Hello {path=}</h1>\n{template_name=}"


# Create some route handler functions
def home(environ):
    """
    This is a route handler/function!

    Helper function to handle the homepage route by returning
    the 'index.html' template.

    We don't need to pass anything to context for the index/root
    page.

    Params:
        environ = The actual request object
    """
    return render_template(template_name="index.html", context={})


def contact_us(environ):
    """
    This is a route handler/function!

    Params:
        environ = The actual request object
    """
    return render_template(
        template_name="contact.html", context={"path": environ.get("PATH_INFO")}
    )


def app(environ: t.Dict, start_response):
    """Expand app by adding routing by checking the path/route
    that is in the request (stored in 'environ') to render different
    things based on the specific routes."""
    # Print the request object details in environ.items()
    for k, v in environ.items():
        print(k, v)

    # Let's capture the request path
    path = environ.get("PATH_INFO")

    # Handle our different routes. Render different templates.
    # Allow user to add "/" or not to URL string
    # NOTE: Don't use elif statement! It skips 'data' assignment!
    if path.endswith("/"):
        path = path[:-1]  # remove the trailing "/"
    if path == "":  # the root / index
        data = home(environ)
    elif path == "/contact":
        data = contact_us(environ)
    else:
        data = render_template(template_name="404.html", context={"path": path})

    # Encode data to BYTE string
    data = data.encode("utf-8")

    # Gunicorn's start_response to get a response going
    start_response(
        f"200 OK",
        [("Content-Type", "text/html"), ("Content-Length", str(len(data)))],
        # You can remove these headers and the browser will still parse it.
        # Modern browsers are smart enough to infer how to parse the request
    )
    # Where does this print to? Server logs I bet... YES!
    # print(f"{data=}\n{iter([data])}")
    return iter([data])  # <list_iterator object at 0x10f9f1340>


# # ====== Basic w/o any routes
# def app(environ: t.Dict, start_response):
#     """The barebones app"""
#     # Have data var be a BYTE string
#     # data = "Hello World!"
#     data = render_template()
#     data = data.encode("utf-8")
#     start_response(
#         f"200 OK",
#         [("Content-Type", "text/html"), ("Content-Length", str(len(data)))],
#         # You can remove these headers and the browser will still parse it.
#         # Modern browsers are smart enough to infer how to parse the request
#     )
#     return iter([data])


# # ====== Intermediate: Handling TWO routes
# # gunicorn
# def render_template(
#     template_name: str = "index.html", context: t.Dict[str, str] = {}
# ):
#     """
#     Render HTML instead of plain text. This will now
#     be the 'data/payload' that we send.

#     We read the template_name file's HTML and return that HTML.
#     """
#     html_str: str
#     with open(template_name, "r") as f:
#         html_str = f.read()
#         html_str = html_str.format(**context)
#     return html_str
#     # return f"<h1>Hello {path=}</h1>\n{template_name=}"


# def home(environ):
#     """
#     Helper function to handle the homepage route by returning
#     the 'index.html' template.

#     We don't need to pass anything to context for the index/root
#     page.
#     """
#     return render_template(template_name="index.html", context={})


# def app(environ: t.Dict, start_response):
#     """Expand app by adding routing by checking the path/route
#     that is in the request (stored in 'environ') to render different
#     things based on the specific routes."""
#     # Print the request object details in environ.items()
#     for k, v in environ.items():
#         print(k, v)

#     # Let's capture the request path
#     path = environ.get("PATH_INFO")
#     if path == "/":  # the root / index
#         data = render_template(
#             template_name="index.html", context={"path": path}
#         )
#     else:
#         data = render_template(template_name="404.html", context={"path": path})

#     # Encode data to BYTE string
#     data = data.encode("utf-8")

#     # Gunicorn's start_response to get a response going
#     start_response(
#         f"200 OK",
#         [("Content-Type", "text/html"), ("Content-Length", str(len(data)))],
#         # You can remove these headers and the browser will still parse it.
#         # Modern browsers are smart enough to infer how to parse the request
#     )
#     # Where does this print to? Server logs I bet... YES!
#     # print(f"{data=}\n{iter([data])}")
#     return iter([data])  # <list_iterator object at 0x10f9f1340>

