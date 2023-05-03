import pandas as pd
import re
import html
import random

csv = pd.read_csv("history.csv")
# print(csv["response"][0])

"""
NAME
CODENAME
ROLE
BIOGRAPHY
RELATIONSHIPS
"""

def give_text():

    raw_text = csv["response"][random.randint(0, 25)]

    # Define the set of headers to be formatted as <h3>
    header_set = {'Name', 'Codename', 'Role', 'Appearance', 'Biography', 'Personality', 'Abilities', 'Relationships'}

    # Function to format specific headers as <h3> headings
    def format_header(match):
        header = match.group(1)
        if header in header_set:
            return '<h4> /// ' + header.upper() + '</h4>'
        else:
            return header + ':'

    # Format the raw text into HTML
    html_text = html.escape(raw_text)
    html_text = html_text.replace('\n', '<br>')
    html_text = re.sub(r'(\w+):', format_header, html_text)

    # Wrap the HTML text in <p> tags
    # html_text = '<p>' + html_text + '</p>'

    # print(html_text)
    return html_text

def proc_text(raw_text):
    # Define the set of headers to be formatted as <h3>
    header_set = {'Name', 'Codename', 'Role', 'Appearance', 'Biography', 'Personality', 'Abilities', 'Relationships'}

    # Function to format specific headers as <h3> headings
    def format_header(match):
        header = match.group(1)
        if header in header_set:
            return '<h4> /// ' + header.upper() + '</h4>'
        else:
            return header + ':'

    # Format the raw text into HTML
    html_text = html.escape(raw_text)
    html_text = html_text.replace('\n', '<br>')
    html_text = re.sub(r'(\w+):', format_header, html_text)

    # Wrap the HTML text in <p> tags
    # html_text = '<p>' + html_text + '</p>'

    # print(html_text)
    return html_text