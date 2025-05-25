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

def obtener_reporte_general_data():
    """
    Prepara los datos para el reporte general.
    """
    reporte = []
    for registro in datos_participantes:
        reporte.append({
            "nombre": registro["nombre"],
            "puntaje_final": registro["puntaje_final"],
            "estado": registro["estado"]
        })
    return reporte

def calcular_puntaje_promedio_grupo():
    """
    Calcula el puntaje promedio final de todos los participantes.
    """
    if not datos_participantes:
        return 0
    total_puntajes = sum(r["puntaje_final"] for r in datos_participantes)
    return round(total_puntajes / len(datos_participantes))

def contar_clasificados():
    """
    cuenta cauntos participantes clasificaron y cuantos no.
    cada registro se considera una entrada individual en el conteo.
    si se desea contar solo una vez por participante(por ejemplo, su ultima participacion)
    habia que ajustar la logica para evitar duplicados"""

    clasificadosd = 0
    no_clasificados = 0
    for registro in datos_participantes:
        if registro["estado"] == "Clasificó":
            clasificados += 1
        else:
            no_clasificados += 1
        return{"clasificó": clasificados, "no clasificó": no_clasificados}
    
if __name__ == '__main__':

    reg1 = registrar_participante("Ana Peres", {"resistencia": 85, "fuerza": 70, "velocidad": 90})
    if reg1: print(f"Registrado: {reg1['nombre']}, Puntaje final: {reg1['puntaje_final']}, Estado: {reg1['estado']}")

    reg2 = registrar_participante("Luis Gómez", {"resistencia": 60, "fuerza": 65, "velocidad": 50})
    ir reg2: print(f"Registrado: {reg2['nombre']}, Puntaje Final: {reg2['puntaje_final']}, Estado: {reg2['estado']}")

    reg3 = registrar_participante("Ana Pérez", {"resistencia": 90, "fuerza": 80, "velocidad": 85})
    ir reg3: print(f"Registrado: {reg3['nombre']}, Puntaje Final: {reg3['puntaje_final']}, Estado: {reg3['estado']}")

    print("\n--- Reporte General (Datos Base) ---")
    for item in obtener_reporte_general_data():
        print(item)

    print("\n--- Datos Participante 'Ana Pérez' ---")
    for item in obtener_datos_participante("Ana Pérez"):
        print(f"  Puntaje Final: {item['puntaje_final']}, Estado: {item['estado']}")
        for prueba, detalles in item['detalle_pruebas'].items():
            print(f"    {PRUEBAS[prueba]}: Puntaje {detalles['puntaje']}, Dificultad {detalles['dificultad']}")

    print(f"\nPuntaje promedio del grupo" {calcular_puntaje_promedio_grupo()}")
    print(f"Clasificacion (por registro): {contar_clasificados()}")