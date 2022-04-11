from django.shortcuts import render


# Create your views here.

def index(request):
    map_loc = [51.505, -0.09]
    test = '123'
    popup_html = '''
    <html>
    <head>
        <style type="text/css" abt="234"></style>
    </head>
    <body style="background-color:powderblue">
    <h1>{{ test }}</h1>
    </body>
    </html>'''
    context = {
        'map_loc': map_loc,
        'test': test,
        'popup_html': popup_html
    }
    return render(request, 'test/index.html', context)


def iframe(request, uid=0):
    test = request.POST['add_method_selected']
    context = {
        'test': test,
    }
    return render(request, 'test/iframe.html', context)
