import hashlib
import random
import re

import markdown


def hash_SHA3_str(input_string)->str:
    """
    This function takes an input string and returns its SHA3 hash as a hexadecimal string.
    """
    sha3_hash = hashlib.sha3_256()
    sha3_hash.update(input_string.encode('utf-8'))
    hashed_string = sha3_hash.hexdigest()
    return hashed_string

def linksToHTML_a(text):
    def replace_markdown_links(match):
        link_text = match.group(1)
        link_url = match.group(2)
        return f'<a href="{link_url}">{link_text}</a>'

    def replace_plain_links(match):
        return f'{match.group(0)}🔗'

    # Замена Markdown ссылок
    markdown_pattern = r'\[(.*?)\]\((.*?)\)'
    text = re.sub(markdown_pattern, replace_markdown_links, text)

    # Замена простых ссылок
    plain_link_pattern = r'https?://\S+'
    text = re.sub(plain_link_pattern, replace_plain_links, text)

    return text



# input_text = "this is a text with [link 1](http://example1.com) and [link2](http://example2.com) with markdown and also https://example3.com"
# output_text = linksToHTML_a(input_text)
# print(output_text)

def str_to_HTML(string):
    '''converts string to HTML tags WITH P-TAG!!!'''
    string = linksToHTML_a(string)
    string = markdown.markdown(string)
    return string
# print(str_to_HTML('''
# [лололо](http://clown.ai)
# трололо https://glitchdev.ru
# *лол*
# **лыл**
# ***лал***
# `аивап`
# ```python атмама```
# __иапа__
# ~~ffdfdfsg~~
# ## h2
# '''))
def genToken(segments:int, segment_length:int)->str:
    token = ''
    symbols = "abcdefjhijklmnopqrstuvwxyz0123456789ABCDEFGHJIKLMNOPQRSTUVWXYZ"
    for i in range(segments):
        token += ''.join([str(random.choice(symbols)) for _ in range(segment_length)])
        token+="-"
    token=token[:-1]
    return token