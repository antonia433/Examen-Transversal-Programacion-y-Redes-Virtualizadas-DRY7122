#!/usr/bin/env python3
# Script para calcular distancia entre ciudades de Chile y Perú

import math

# Diccionario con coordenadas aproximadas de ciudades (lat, lon)
ciudades = {
    # Chile
    'santiago': (-33.4489, -70.6693),
    'valparaiso': (-33.0458, -71.6197),
    'concepcion': (-36.8267, -73.0617),
    'arica': (-18.4783, -70.3126),
    # Perú
    'lima': (-12.0464, -77.0428),
    'arequipa': (-16.4090, -71.5375),
    'cuzco': (-13.5319, -71.9675),
    'trujillo': (-8.1091, -79.0215)
}

# Velocidades promedio en km/h
velocidades = {
    'auto': 90,
    'bus': 70,
    'avion': 800,
    'bicicleta': 20
}

def calcular_distancia(ciudad1, ciudad2):
    """Calcula la distancia entre dos ciudades usando la fórmula del haversine"""
    lat1, lon1 = ciudad1
    lat2, lon2 = ciudad2
    
    # Radio de la Tierra en km
    R = 6371.0
    
    # Convertir grados a radianes
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Diferencias de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula del haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distancia_km = R * c
    return distancia_km

def mostrar_menu_ciudades(pais):
    """Muestra las ciudades disponibles para un país"""
    print(f"\nCiudades de {pais} disponibles:")
    for ciudad in ciudades:
        if pais.lower() == 'chile' and ciudad in ['santiago', 'valparaiso', 'concepcion', 'arica']:
            print(f"- {ciudad.capitalize()}")
        elif pais.lower() == 'perú' and ciudad in ['lima', 'arequipa', 'cuzco', 'trujillo']:
            print(f"- {ciudad.capitalize()}")

def obtener_ciudad(pais):
    """Solicita al usuario una ciudad válida"""
    while True:
        mostrar_menu_ciudades(pais)
        ciudad = input(f"\nIngrese ciudad de {pais} (o 's' para salir): ").lower()
        
        if ciudad == 's':
            return None
        
        if ciudad in ciudades and (
            (pais.lower() == 'chile' and ciudad in ['santiago', 'valparaiso', 'concepcion', 'arica']) or
            (pais.lower() == 'perú' and ciudad in ['lima', 'arequipa', 'cuzco', 'trujillo'])
        ):
            return ciudad
        else:
            print("¡Ciudad no válida! Intente nuevamente.")

def obtener_transporte():
    """Solicita al usuario el medio de transporte"""
    print("\nMedios de transporte disponibles:")
    for transporte in velocidades:
        print(f"- {transporte.capitalize()}")
    
    while True:
        transporte = input("\nElija medio de transporte (o 's' para salir): ").lower()
        
        if transporte == 's':
            return None
        
        if transporte in velocidades:
            return transporte
        else:
            print("¡Transporte no válido! Intente nuevamente.")

def narrar_viaje(origen, destino, transporte):
    """Genera una narrativa del viaje"""
    narrativas = {
        'auto': f"Un emocionante viaje por carretera desde {origen} hasta {destino}.",
        'bus': f"Un viaje en bus disfrutando del paisaje entre {origen} y {destino}.",
        'avion': f"Un rápido vuelo desde {origen} a {destino} con hermosas vistas desde arriba.",
        'bicicleta': f"Una aventura en bicicleta desde {origen} hasta {destino} para los más valientes."
    }
    return narrativas.get(transporte, f"Viaje desde {origen} hasta {destino}.")

def main():
    print("\n=== Calculador de Viajes Chile-Perú ===")
    print("Ingrese 's' en cualquier momento para salir\n")
    
    while True:
        # Obtener ciudades
        origen = obtener_ciudad('Chile')
        if origen is None:
            break
            
        destino = obtener_ciudad('Perú')
        if destino is None:
            break
        
        # Obtener transporte
        transporte = obtener_transporte()
        if transporte is None:
            break
        
        # Calcular distancia y duración
        distancia_km = calcular_distancia(ciudades[origen], ciudades[destino])
        distancia_millas = distancia_km * 0.621371
        
        horas_viaje = distancia_km / velocidades[transporte]
        dias_viaje = int(horas_viaje // 24)
        horas_restantes = horas_viaje % 24
        
        # Mostrar resultados
        print("\n=== Resultados del Viaje ===")
        print(f"Ruta: {origen.capitalize()} (Chile) -> {destino.capitalize()} (Perú)")
        print(f"Distancia: {distancia_km:.2f} km / {distancia_millas:.2f} millas")
        
        if dias_viaje > 0:
            print(f"Duración: {dias_viaje} días y {horas_restantes:.1f} horas (en {transporte})")
        else:
            print(f"Duración: {horas_viaje:.1f} horas (en {transporte})")
        
        print("\nNarrativa del viaje:")
        print(narrar_viaje(origen.capitalize(), destino.capitalize(), transporte))
        
        input("\nPresione Enter para realizar otro cálculo o Ctrl+C para salir...")

if __name__ == "__main__":
    main()
