# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages(request=None):
    raw_images = transport.getAllImages()
    favourite_ids = []

    # Solo obtener favoritos si hay request y el usuario está autenticado
    if request and request.user.is_authenticated:
        favourites = getAllFavourites(request)
        favourite_ids = [str(card.id) for card in favourites]

    card_list = []

    for raw in raw_images:
        card = translator.fromRequestIntoCard(raw)
        card.is_favourite = str(card.id) in favourite_ids  # Marcar si ya es favorito
        card_list.append(card)

    return card_list

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    # Obtener todas las imágenes una sola vez
    all_cards = getAllImages()
    filtered_cards = []

    for card in all_cards:
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        if name.lower() in card.name.lower():            
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    # Obtener todas las imágenes una sola vez
    all_cards = getAllImages()
    filtered_cards = []

    for card in all_cards:
        # debe verificar si la casa de la card coincide con la recibida por parámetro. Si es así, se añade al listado de filtered_cards.
        if type_filter.lower() in [type.lower() for type in card.types]:
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request) # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav)

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    
    user = get_user(request)
    favourite_list = repositories.get_all_favourites(user) # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
    mapped_favourites = []

    for favourite in favourite_list:
        card = translator.fromRepositoryIntoCard(favourite) # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
        mapped_favourites.append(card)

    return mapped_favourites

def deleteFavourite(request):
    fav_id = request.POST.get('id')
    return repositories.delete_favourite(fav_id) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)