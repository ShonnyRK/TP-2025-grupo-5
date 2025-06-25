# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config
import concurrent.futures
from threading import Lock

# Cache para evitar hacer múltiples requests
_cache = {}
_cache_lock = Lock()

def getAllImages():
    with _cache_lock:
        if _cache:
            print("[transport.py]: Usando cache de Pokémon")
            return list(_cache.values())
    
    print("[transport.py]: Obteniendo datos de la API...")
    json_collection = []
    
    # Usar ThreadPoolExecutor para hacer peticiones paralelas
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Crear futures para cada petición
        future_to_id = {executor.submit(fetch_single_pokemon, id): id for id in range(1, 30)}
        
        for future in concurrent.futures.as_completed(future_to_id):
            pokemon_id = future_to_id[future]
            try:
                pokemon_data = future.result()
                if pokemon_data:
                    json_collection.append(pokemon_data)
            except Exception as exc:
                print(f"[transport.py]: Error al obtener Pokémon {pokemon_id}: {exc}")
    
    # Ordenar por ID para mantener consistencia
    json_collection.sort(key=lambda x: x.get('id', 0))
    
    # Guardar en cache
    with _cache_lock:
        for pokemon in json_collection:
            _cache[pokemon['id']] = pokemon
    
    print(f"[transport.py]: Obtenidos {len(json_collection)} Pokémon")
    return json_collection

def fetch_single_pokemon(pokemon_id):
    """Función auxiliar para obtener un solo Pokémon"""
    try:
        response = requests.get(config.STUDENTS_REST_API_URL + str(pokemon_id), timeout=10)
        
        if not response.ok:
            print(f"[transport.py]: error al obtener datos para el id {pokemon_id}")
            return None

        raw_data = response.json()

        if 'detail' in raw_data and raw_data['detail'] == 'Not found.':
            print(f"[transport.py]: Pokémon con id {pokemon_id} no encontrado.")
            return None

        return raw_data
    except requests.exceptions.Timeout:
        print(f"[transport.py]: Timeout para el id {pokemon_id}")
        return None
    except Exception as e:
        print(f"[transport.py]: Error inesperado para el id {pokemon_id}: {e}")
        return None

# obtiene la imagen correspodiente para un type_id especifico 
def get_type_icon_url_by_id(type_id):
    base_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/'
    return f"{base_url}{type_id}.png"