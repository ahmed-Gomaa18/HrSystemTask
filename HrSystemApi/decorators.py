from rest_framework.response import Response


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'Notes': 'You are Already Authentication'})
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func



def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'employee':
            return Response({"Erorr" : "Your not Admin"})
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

