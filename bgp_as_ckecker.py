#!/usr/bin/env python3

def verificar_as(numero_as):
    try:
        as_num = int(numero_as)
        if 64512 <= as_num <= 65534 or as_num == 4200000000 or (65536 <= as_num <= 4294967294):
            return "privado"
        elif 1 <= as_num <= 64511 or as_num == 65535 or (131072 <= as_num <= 4199999999):
            return "público"
        else:
            return "fuera de rango conocido"
    except ValueError:
        return "no válido (debe ser un número)"

if __name__ == "__main__":
    print("=== Verificador de AS BGP ===")
    while True:
        as_input = input("Ingrese el número de AS (o 'salir' para terminar): ")
        
        if as_input.lower() == 'salir':
            break
            
        resultado = verificar_as(as_input)
        print(f"El AS {as_input} es {resultado}\n")
