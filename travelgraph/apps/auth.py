from flask import session, redirect

def login_required(f):
    
    def wrap(request,*args,**kwargs):

        user_logged_in = session.get('user_id',False)
        
        if user_logged_in:
            return f(request, *args, **kwargs)
        else:
            return redirect('/')

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap