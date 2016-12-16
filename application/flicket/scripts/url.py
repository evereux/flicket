

def generate_url(base, end):
    """
    Depending on the applications config generating url for api can result in something like
    http://website.com//flicket-api/.
    This function will fix this and output http://website.come/flicketp-api/
    :param base:
    :param end:
    :return:
    """
    if base[-1] == '/' and end[0] == '/':
        base = base[:-1]

    return base+end