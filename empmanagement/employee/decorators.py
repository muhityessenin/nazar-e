from django.shortcuts import redirect
from django.contrib import messages

def only_director(view_func):
    def wrapper(request, *args, **kwargs):
        director_id = "123123"

        if request.user.username != director_id:
            messages.error(request, "Access denied. Only the General Director can access this page.")
            return redirect("/ems/dashboard")

        return view_func(request, *args, **kwargs)
    return wrapper
