# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def index_page(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validaciones
        errors = []
        
        # Verificar que todos los campos estén completos
        if not all([first_name, last_name, username, email, password, confirm_password]):
            errors.append("Todos los campos son obligatorios.")
        
        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            errors.append("Las contraseñas no coinciden.")
        
        # Verificar que la contraseña tenga al menos 8 caracteres
        if len(password) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres.")
        
        # Verificar que el email sea válido (validación básica)
        if '@' not in email or '.' not in email:
            errors.append("El email no es válido.")
        
        # Verificar que el nombre de usuario no exista
        if User.objects.filter(username=username).exists():
            errors.append("El nombre de usuario ya existe. Por favor, elige otro.")
        
        # Verificar que el email no esté en uso
        if User.objects.filter(email=email).exists():
            errors.append("El email ya está registrado. Por favor, usa otro email.")
        
        if errors:
            # Si hay errores, mostrar mensajes y volver al formulario
            for error in errors:
                messages.error(request, error)
            return render(request, 'registration/register.html')
        
        try:
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Autenticar y loguear al usuario
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido {user.first_name}! Tu cuenta ha sido creada exitosamente.")
                return redirect('home')
            else:
                messages.error(request, "Error al autenticar el usuario.")
                return render(request, 'registration/register.html')
                
        except Exception as e:
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            return render(request, 'registration/register.html')
    
    return render(request, 'registration/register.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages(request)
    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if name:
        images = services.filterByCharacter(name)
        favourite_list = services.getAllFavourites(request)
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    
    return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type_filter = request.POST.get('type', '')

    if type_filter:
        images = services.filterByType(type_filter) # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = services.getAllFavourites(request)
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    
    return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method == "POST":
        services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == "POST":
        services.deleteFavourite(request)
    return redirect('home')

@login_required
def exit(request):
    logout(request)
    return redirect('home')