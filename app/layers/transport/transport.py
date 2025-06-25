"""
Capa de transporte/comunicación con APIs externas.

Este módulo maneja todas las comunicaciones con la API de Pokémon
y proporciona funciones para obtener datos de Pokémon.
"""

import requests
from ...config import config
import concurrent.futures
from threading import Lock
from typing import List, Dict, Optional

# Constantes para configuración
MAX_WORKERS = 5
POKEMON_RANGE = (1, 152)  # Rango de IDs de Pokémon a obtener
REQUEST_TIMEOUT = 10

# Cache para evitar hacer múltiples requests
_cache = {}
_cache_lock = Lock()


def getAllImages() -> List[Dict]:
    """
    Obtiene todos los Pokémon de la API con cache.
    
    Returns:
        List[Dict]: Lista de diccionarios con datos de Pokémon
    """
    with _cache_lock:
        if _cache:
            print("[transport.py]: Usando cache de Pokémon")
            return list(_cache.values())
    
    print("[transport.py]: Obteniendo datos de la API...")
    json_collection = []
    
    # Usar ThreadPoolExecutor para hacer peticiones paralelas
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Crear futures para cada petición
        future_to_id = {
            executor.submit(fetch_single_pokemon, pokemon_id): pokemon_id 
            for pokemon_id in range(POKEMON_RANGE[0], POKEMON_RANGE[1])
        }
        
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


def fetch_single_pokemon(pokemon_id: int) -> Optional[Dict]:
    """
    Obtiene un solo Pokémon de la API.
    
    Args:
        pokemon_id: ID del Pokémon a obtener
        
    Returns:
        Dict: Datos del Pokémon o None si hay error
    """
    try:
        response = requests.get(
            config.STUDENTS_REST_API_URL + str(pokemon_id), 
            timeout=REQUEST_TIMEOUT
        )
        
        if not response.ok:
            print(f"[transport.py]: Error al obtener datos para el id {pokemon_id}")
            return None

        raw_data = response.json()

        if 'detail' in raw_data and raw_data['detail'] == 'Not found.':
            print(f"[transport.py]: Pokémon con id {pokemon_id} no encontrado.")
            return None

        return raw_data
        
    except requests.exceptions.Timeout:
        print(f"[transport.py]: Timeout para el id {pokemon_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[transport.py]: Error de red para el id {pokemon_id}: {e}")
        return None
    except Exception as e:
        print(f"[transport.py]: Error inesperado para el id {pokemon_id}: {e}")
        return None


def get_type_icon_url_by_id(type_id: int) -> str:
    """
    Obtiene la URL de la imagen correspondiente para un type_id específico.
    
    Args:
        type_id: ID del tipo de Pokémon
        
    Returns:
        str: URL de la imagen del tipo
    """
    base_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/'
    return f"{base_url}{type_id}.png"


def clear_cache() -> None:
    """
    Limpia el cache de Pokémon.
    
    Útil para forzar una nueva obtención de datos de la API.
    """
    with _cache_lock:
        _cache.clear()
    print("[transport.py]: Cache limpiado")


def get_cache_size() -> int:
    """
    Obtiene el tamaño actual del cache.
    
    Returns:
        int: Número de Pokémon en cache
    """
    with _cache_lock:
        return len(_cache)