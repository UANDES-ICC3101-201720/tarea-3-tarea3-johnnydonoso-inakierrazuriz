import socket
import json
import os

 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("[TRACKER]\n")
 
host = socket.gethostname()
port = 12345

s.bind((host,port))

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname,'generated.json')

with open (filepath,'r+') as file:
    datos = json.load(file)

cont=0
s.listen(10) 
while True:
    connection, address = s.accept()
    print ('[Tracker]Got connection from', address)
    data = connection.recv(1024)
    
    archivos_a_enviar = ""
    data_as_str = data.decode()
    data1 = data_as_str.split(",")
    if (data1[0]=='1'):
        print("[Tracker]data recibida desde host = "+ str(data1[0])+","+str(data1[1]))
        for dato in datos['data']:
            if (data1[1] in dato.get('nombre')):
                if(dato.get('disp')== "true" ):
                    cont = 1
                    archivos_a_enviar = archivos_a_enviar+dato.get('nombre')+","+dato.get('ip')+"|"
                    print("[Tracker]",dato.get('ip'))
                else:
                    continue
        if(cont==0):
             connection.send('[Tracker] Archivo lamentablemente no encontrado en nuestras redes'.encode())
    
        envio = archivos_a_enviar.encode()
        connection.send(envio)
    if (data1[0]=='2'):
        print("[Tracker]data recibida desde host = "+ str(data1[0])+","+str(data1[1]))
        print("[Tracker] subir archivos")
        datos['data'].append({
            'nombre': str(data1[1]),
            'ip': str(address[0]),
            'port': 1234,
            'disp': 'true'})
        with open(filepath,'w') as file:
            json.dump(datos,file)
        connection.send("[Tracker] Archivo subido correctamente".encode())
    if (data1[0]=='adios'):
        exit()
        

    

