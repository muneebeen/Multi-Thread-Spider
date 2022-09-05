from urllib.parse import urlparse


def get_sub_domain(url):
    try:
        sub_domain = urlparse(url).netloc
    except:
        print('Could not get the URL')
        return ''
    return sub_domain


def get_domain(url):
    try:
        results = get_sub_domain(url).split('.')
    except:
        print('Could not get the URL')
    return results[-2] + '.' + results[-1]


