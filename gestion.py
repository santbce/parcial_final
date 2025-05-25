import random
import math


datos_participantes = []

PRUEBAS = {
    "resistencia": "Resistencia",
    "fuerza": "Fuerza",
    "velocidad": "Velocidad"
}

def registrar_participante(nombre_participante, resultados_pruebas):
    """
    Registra el rendimiento de un participante.

    Args:
        nombre_participante (str): El nombre del participante.
        resultados_pruebas (dict): Un diccionario con los puntajes de cada prueba.
                                   Ej: {"resistencia": 80, "fuerza": 75, "velocidad": 90}

    Returns:
        dict: El registro del participante creado, incluyendo puntaje final y estado.
              Retorna None si hay un error en los puntajes.
    """
    detalle_pruebas = {}
    suma_puntaje_por_dificultad = 0
    suma_dificultades = 0

    for prueba_key, puntaje in resultados_pruebas.items():
        if not (0 <= puntaje <= 100):
            print(f"Error: El puntaje para {PRUEBAS.get(prueba_key, prueba_key)} debe estar entre 0 y 100.")
            return None

        dificultad = round(random.uniform(1.0, 1.3), 2)
        detalle_pruebas[prueba_key] = {
            "puntaje": puntaje,
            "dificultad": dificultad,
            "puntaje_ponderado_prueba": puntaje * dificultad
        }
        suma_puntaje_por_dificultad += puntaje * dificultad
        suma_dificultades += dificultad

    if suma_dificultades == 0:  
        puntaje_final_ponderado = 0
    else:
        puntaje_final_ponderado = suma_puntaje_por_dificultad / suma_dificultades
    
    puntaje_final_redondeado = round(puntaje_final_ponderado) 

    estado_clasificacion = "Clasificó" if puntaje_final_redondeado >= 70 else "No clasificó"

    registro = {
        "nombre": nombre_participante,
        "detalle_pruebas": detalle_pruebas,
        "puntaje_final": puntaje_final_redondeado,
        "estado": estado_clasificacion
    }
    datos_participantes.append(registro)
    return registro