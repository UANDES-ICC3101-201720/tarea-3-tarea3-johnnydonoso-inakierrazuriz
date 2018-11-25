import socket               
         
host = socket.gethostname() 
port = 12345  

mis_Archivos = ["archivo1.txt","archivo2.txt","archivo3.txt"] #asumiremos que asi se pueden verificar los archivos en mi almacenamiento, ya que esto es un modelo

print("[CLIENTE]\n")

toServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
toServer.connect((host,port))

print("[Client] Bienvenido al descargador de archivos")


while True:
    opcion = input("[Client]Seleccione la acción a realizar:\n1.- Buscar Archivo y Descargar\n2.- Subir Archivo\n")
    
    if(opcion=='1'):
        while True:
            archivo = input("[Client]Ingrese el archivo que desea buscar en la red: \n")
            if(archivo != "" ):
                archivo_as_bytes = str.encode("1,"+archivo )
                toServer.send(archivo_as_bytes)
 
                response = toServer.recv(1024)
                response_as_str = response.decode()

                if(response_as_str == '[Tracker] Archivo lamentablemente no encontrado en nuestras redes'):
                    print(response_as_str)
                else:
                    palabras = response_as_str.split("|")
                    contador = 0
                    palabras.remove("")
                    nombre_archivos=[]
                    ip_archivos = []
                    print("Hosts Disponibles para descarga")
                    for palabra in palabras:
                        palabrita = palabra.split(",")
                        print(str(contador)+".-  Nombre: "+palabrita[0]+" Ip: "+palabrita[1])
                        nombre_archivos.append(palabrita[0])
                        ip_archivos.append(palabrita[1])
                        contador = contador + 1
                    opcion_host = ""
                    while True:
                        opcion_host = input("Ingrese el número asociado al host donde quiere descargar el archivo\n")
                        if(int(opcion_host) < 0 or int(opcion_host)>contador):
                            print("Opcion inválida, ingrésela nuevamente porfavor\n")
                            continue
                        break
                    ip_a_descargar = ip_archivos[int(opcion_host)]
                    archivo_a_descargar = nombre_archivos[int(opcion_host)]

                    break
            else:
                print("No ingresó nada, ingrese nuevamente\n")
                continue
            break

    if(opcion=='2'):
        print("[Client] Subir archivo\n")
        print("[Client] Seleccione el archivo que desea subir para tenerlo en las posibles descargas\n")
        contador1 = 0
        archivo_a_subir = ""
        for archivo in mis_Archivos:
            print(str(contador1)+".- "+archivo)
            contador1 = contador1 + 1
        opcionn = ""
        while True:
            opcionn = input()
            if(int(opcionn)<0 or int(opcionn)>contador1):
                print("Opción inválida, ingrésela nuevamente\n")
                continue
            break
        archivo_a_subir = mis_Archivos[int(opcionn)]
        archivo_as_bytes = str.encode("2,"+archivo_a_subir)
        toServer.send(archivo_as_bytes)

        response = toServer.recv(1024)
        response_as_str = response.decode()
        print(response_as_str)


        break
    else:
        print("[Client] Opción inválida, ingrésela nuevamente porfavor \n")
        continue
    break

toServer.close()
