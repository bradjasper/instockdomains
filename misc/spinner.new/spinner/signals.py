import django.dispatch

spinner_results = django.dispatch.Signal(providing_args=["data"])
