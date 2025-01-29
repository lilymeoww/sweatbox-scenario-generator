from fasthtml.common import *

app,rt = fast_app()

@rt("/")
def get(): return Div(P("goodbye world :("), hx_get="/change")

@rt("/change")
def get(): return P("Nice to be here!")

serve()