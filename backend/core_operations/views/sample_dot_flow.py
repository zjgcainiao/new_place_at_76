from django.http import HttpResponse
from graphviz import Digraph


def sample_dot_flow(request):
    dot = Digraph(format='svg')

    dot.attr(rankdir='LR')  # Global attribute to layout the graph from left to right
    # TB for top to bottom, LR for left to right, etc.).

    # Define nodes
    dot.node('Models', 'Models', shape='box', color='red')
    dot.node('Views', 'Views', shape='box')
    dot.node('Templates', 'Templates', shape='box')
    dot.node('Urls', 'URLs', shape='ellipse')
    dot.node('Forms', 'Forms', shape='box')

    # Define edges
    dot.edge('Urls', 'Views', label='resolve to', color='blue')
    dot.edge('Views', 'Models', label='interacts with', color='blue')
    dot.edge('Views', 'Templates', label='renders in', color='yellow')
    dot.edge('Forms', 'Views', label='posted to', color='blue')
    # Generate SVG
    svg = dot.pipe().decode('utf-8')  # This will generate the graph directly into memory in SVG format
    return HttpResponse(svg, content_type='image/svg+xml')
