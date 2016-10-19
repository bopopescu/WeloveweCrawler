import HTMLParser

def parse_html(content):
    try:
        data = HTMLParser.HTMLParser().unescape(content)
    except Exception as e:
        data = ''

    return data
