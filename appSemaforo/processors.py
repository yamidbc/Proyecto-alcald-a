def usuario_logeado(request):
    return {'usuario_logeado':request.user.username}