import datetime
import pytz
import time
import platform

acciones_realizadas = {
    'Registrar Usuario': 0,
    'Ingresar Vehículo': 0,
    'Retirar Vehículo': 0,
    'Acceso Administrador': 0
}

def crear_log(nombre_usuario):
    sistema = platform.system()
    version = platform.version()
    arquitectura = platform.architecture()[0]
    plataforma_info = platform.platform()

    encabezado = (
        f"Usuario: {nombre_usuario}\n"
        f"Sistema Operativo: {sistema} - {version} - {arquitectura}\n"
        f"Plataforma: {plataforma_info}\n"
        f"{'Fecha y hora':<30}|{'Acción':<30}|{'Duración (s)':<15}\n"
        + "-"*85 + "\n"
    )

    with open("log_parqueadero.txt", "w") as archivo:
        archivo.write(encabezado)
    print(encabezado)


def registrar_log(accion, tiempo_inicio):
    tiempo_fin = time.time()
    duracion = round(tiempo_fin - tiempo_inicio, 5)
    fecha_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    linea = f"{fecha_hora:<30}|{accion:<30}|{duracion:<15}\n"

    with open("log_parqueadero.txt", "a") as archivo:
        archivo.write(linea)

    if accion in acciones_realizadas:
        acciones_realizadas[accion] += 1

def resumen_log():
    with open("log_parqueadero.txt", "a") as archivo:
        archivo.write("\nResumen de Acciones:\n")
        for accion, cantidad in acciones_realizadas.items():
            archivo.write(f"{accion}: {cantidad} veces\n")


usuarios = {}
vehiculos = {}
historial_retiros = []
ESPACIOS_TOTALES = 64
errores = []
NIT= "901234987-8"


def hora_actual_colombia():
    zona_colombia = pytz.timezone("America/Bogota")
    ahora = datetime.datetime.now(zona_colombia)
    return ahora.strftime("%H:%M:%S")

# Funciones de validación

def Registro_Nombre(nombre: str, errores):
    Nombre = str(nombre)
    if len(Nombre) > 2:
        palabras = Nombre.split()
        if all(palabra.isalpha() for palabra in palabras):
            return Nombre
        else:
                errores.append('error, los nombres solo debe contener letras')
                return False
    else:
        errores.append("Error, el nombre debe tener más de 2 letras.")
        return False

def Registro_Apellido(apellido: str, errores):
    Apellido = str(apellido)
    if len(Apellido) > 2:
        palabras = Apellido.split()
        if all(palabra.isalpha() for palabra in palabras):
            return Apellido
        else:
            errores.append("Error, el apellido solo debe contener letras.")
            return False
    else:
        errores.append("Error en el apellido, debe tener más de 2 letras.")
        return False

def Registro_Documento(documento: str, errores):
    if documento.isdigit():
        if 3 <= len(documento) <= 15:
            return documento
        else:
            errores.append("Error el documento debe tener entre 3 y 15 dígitos.")
            return False
    else:
        errores.append("Error en el documento solo debe contener números.")
        return False

def Registro_Placa(placa: str, errores):
    Placa = placa.upper()
    if len(Placa) == 6:
        letras = placa [:3]
        numeros = placa [3:]
        if letras.isalpha():
          if numeros.isnumeric():
            return placa
          else:
            mensaje = "la seccion de numero es incorrecta" # la seccion de numeros es incorrecta
            errores.append(mensaje)
            return False
        else:
          mensaje = 'la seccion de letras es incorrecta ' #la seccion de letras es incorrecta
          errores.append(mensaje)
          return False
    else:
      mensaje = ' error la longitud de la placa es 6'
      errores.append(mensaje)

      return False


# Funcion para el registro
def registrar_usuario():
    errores = []
    tiempo_inicio = time.time()

    nombre = Registro_Nombre(input("Ingrese nombre/s: "), errores)
    apellido = Registro_Apellido(input("Ingrese apellido/s: "), errores)
    documento = Registro_Documento(input("Ingrese el numero de documento: "), errores)
    placa = Registro_Placa(input("Ingrese la placa del vehiculo: "), errores)

    #Usuario repetido
    if documento in usuarios:
        print('El usuario ya se encuentra registrado')
        return

    # Si hay errores, se muestran
    if errores:
        print('Se encontraron los siguientes errores: ')
        for error in errores:
            print('-', error)
        return


    usuarios[documento] = {
        'Nombre': nombre,
        'Apellido': apellido,
        'Placa': placa
    }
    print('Usuario registrado exitosamente')
    registrar_log("Registrar Usuario", tiempo_inicio)


def ingresar_vehiculo():
  #se valida si el usuario existe por documento
  tiempo_inicio = time.time()
  if len(vehiculos)>= ESPACIOS_TOTALES:
        print("Estamos en capacidad maxima :(")
        return
  documento = input("Ingrese el documento del usuario: ")
  if documento in usuarios:
        hora = hora_actual_colombia()
        usuarios[documento]["hora_ingreso"] = hora
        placa = usuarios[documento]["Placa"]

        if placa in vehiculos:
            print("Este vehiculo ya ingreso al parquadero")
            return

        placa = usuarios[documento]["Placa"]      #Se utiliza para guardar en vehiculos={}
        vehiculos[placa] = {
            "documento": documento,
            "hora_ingreso": hora
        }



        nombre= usuarios[documento]["Nombre"]
        apellido = usuarios[documento]["Apellido"]
        print("\n")
        print('*'*43)
        print("PARQUEADERO LA CUEVA DEL AUTO".center(45))
        print(f"NIT:{NIT}".center(45))
        print("Dirección: CL.67 #53-108".center(45))
        print("Celular: 3148325322".center(45))
        print("Horario: 6:00 A.M - 12:00 P.M ".center(45))
        print("Factura Electronica de Registro".center(45))
        print("*"*43)
        print(f"Nombre: {nombre}")
        print(f"Apellido: {apellido}")
        print(f"Documento: {documento}")
        print(f'Placa: {usuarios[documento]["Placa"]}')
        print(f"Hora de ingreso: {hora}")
        print("Gracias por utilizar LA CUEVA DEL AUTO. ;) ")
        print('*'*43)
        print("\n")

  else:
        print("Usuario no registrado.")
        registrar_log("Registrar Usuario", tiempo_inicio)


def retirar_vehiculo():
    tiempo_inicio = time.time()
    documento = input("Ingrese el documento del usuario: ")

    if documento in usuarios and 'hora_ingreso' in usuarios[documento]:
        placa = usuarios[documento]["Placa"]
        hora_ingreso = usuarios[documento]['hora_ingreso']
        hora_actual = hora_actual_colombia()

        # Convertir strings a datetime
        formato = "%H:%M:%S"
        hora_ingreso_dt = datetime.datetime.strptime(hora_ingreso, formato)
        hora_actual_dt = datetime.datetime.strptime(hora_actual, formato)

        # Si el usuario sale al día siguiente
        if hora_actual_dt < hora_ingreso_dt:
            hora_actual_dt += datetime.timedelta(days=1)

        diferencia = hora_actual_dt - hora_ingreso_dt
        minutos_totales = diferencia.total_seconds() / 60

        horas = int(minutos_totales) // 60
        residuo = minutos_totales % 60
        cuarto_hora = 0
        minutos_restantes = int(residuo)
        while minutos_restantes > 0:
            cuarto_hora += 1
            minutos_restantes -= 15


        tarifa_hora = 7000
        tarifa_cuarto = 1500

        total = horas * tarifa_hora + cuarto_hora * tarifa_cuarto
        if total < tarifa_hora:
            total = tarifa_hora

        historial_retiros.append({
            "placa": placa,
            "documento": documento,
            "tiempo": minutos_totales,
            "monto": total
        })

        nombre = usuarios[documento]["Nombre"]
        apellido = usuarios[documento]["Apellido"]
        print("\n")
        print('*'*43)
        print("PARQUEADERO LA CUEVA DEL AUTO".center(45))
        print(f"NIT:{NIT}".center(45))
        print("Dirección: CL.67 #53-108".center(45))
        print("Celular: 3148325322".center(45))
        print("Horario: 6:00 A.M - 12:00 P.M ".center(45))
        print("Factura Electronica de SALIDA".center(45))
        print("*"*43)
        print(f"Nombre: {nombre}")
        print(f"Apellido: {apellido}")
        print(f"Documento: {documento}")
        print(f"Placa: {placa}")
        print(f"Hora de ingreso: {hora_ingreso}")
        print(f"Hora de salida: {hora_actual}")
        print(f"Tiempo total: {int(minutos_totales)} minutos")
        print(f"Total a pagar: ${total}")
        print("Gracias por utilizar LA CUEVA DEL AUTO".center(45))
        print("Vuelva pronto".center(45))
        print('*'*43)
        print("\n")

        del vehiculos[placa]
        del usuarios[documento]["hora_ingreso"]

        registrar_log("Retirar Vehículo", tiempo_inicio)
    else:
        print("Usuario no registrado o vehículo no ingresado.")

import getpass # Tapa la contraseña

def menu_administrador():

    print("\n*** ACCESO AL ADMINISTRADOR ***")
    usuario = input("Usuario: ")
    clave = getpass.getpass("Contraseña: ")
    administradores = {
            "adminmarlon": "batman3",
            "adminannie": "superman1",
            "admindaniel": "ironman2"
            }

    if usuario in administradores and administradores[usuario] == clave:
        acciones_realizadas["Acceso Administrador"] += 1
        while True:
            print("\n--- Menú del Administrador ---")
            print("1. Total de vehículos registrados")
            print("2. Total de vehículos retirados")
            print("3. Total de vehículos sin retirar")
            print("4. Total pagado por vehículos retirados")
            print("5. Tiempo promedio de estancia por vehiculo")
            print("6. Lista de usuarios")
            print("7. Vehículo con mayor y menor tiempo de parqueo")
            print("8. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                print(f"Total de vehículos registrados:\n ---> {len(vehiculos)}")
            elif opcion == "2":
                print(f"Total de vehículos retirados:\n ---> {len(historial_retiros)}")
            elif opcion == "3":
                activos = len(vehiculos) - len(historial_retiros)
                print(f"Total de vehículos sin retirar:\n ---> {activos}")
            elif opcion == "4":
                total_pagado = sum(ret['monto'] for ret in historial_retiros)
                print(f"Total pagado: ${total_pagado}")
            elif opcion == "5":
                if historial_retiros:
                    tiempos = [ret['tiempo'] for ret in historial_retiros]
                    promedio = sum(tiempos) / len(tiempos)
                    print(f"Tiempo promedio de estancia por vehiculo: {promedio:.2f} minutos")
                else:
                    print("No hay vehículos retirados aún.")
            elif opcion == "6":
                print("Usuarios registrados:")
                for doc, datos in usuarios.items():
                    print(f" {datos['Nombre']} {datos['Apellido']}\n(Documento: {doc})")
            elif opcion == "7":
                if historial_retiros:
                    maximo = max(historial_retiros, key=lambda x: x['tiempo'])
                    minimo = min(historial_retiros, key=lambda x: x['tiempo'])
                    print(f"Vehículo con mayor tiempo: {maximo['placa']} ({maximo['tiempo']} mins)")
                    print(f"Vehículo con menor tiempo: {minimo['placa']} ({minimo['tiempo']} mins)")
                else:
                    print("No hay vehículos retirados aún.")
            elif opcion == "8":
                break
            else:
                print("Opción inválida.")
    else:
        print(" Usuario o contraseña incorrecta.")


def menu_principal():
    crear_log(input("Ingrese su usuario: "))

    while True:
        print('*'*43)
        print("Bienvenido al parqueadero La cueva del auto")
        print('*'*43)
        print("1. Registrar usuario".center(50))
        print("2. Ingresar vehículo".center(50))
        print("3. Retirar vehículo".center(50))
        print("4. Administrador".center(45))
        print("5. Salir".center(53))
        opcion = input("Ingresar opción: \n ---> ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
          ingresar_vehiculo()
        elif opcion == "3":
           retirar_vehiculo()
        elif opcion == "4":
            menu_administrador()
        elif opcion == "5":
            resumen_log()
            print("Gracias por usar el sistema ")
            break
        else:
            print("Opción inválida.")

menu_principal()
