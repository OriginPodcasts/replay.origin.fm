from django.urls import reverse


def theme(request):
    def item(urlname, text):
        url = reverse(urlname)
        if url == '/':
            active = request.path == '/'
        else:
            active = request.path.startswith(url)

        return {
            'url': url,
            'active': active,
            'text': text
        }

    return {
        'main_menu': [
            item('index', 'Home'),
            item('about', 'About')
        ]
    }
