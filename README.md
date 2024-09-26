# Red P2P en anillo con comunicación entre sus nodos con gRPC

El proyecto sigue los principios del protocolo Chord/DHT para la gestión distribuida de datos en redes P2P.
La red está diseñada para distribuir uniformemente las canciones y gestionar dinámicamente la adición y salida de nodos.

## Detalles del proyecto:

- **Materia:** Tópicos Especiales en Telemática - ST0263
- **Estudiantes:**
  - Alejandro Arango Mejía: aarangom1@eafit.edu.co
  - Thomas Rivera Fernández: triveraf@eafit.edu.co
- **Profesor:** Juan Carlos Montoya Mendoza: jcmontoy@eafit.edu.co

### 1. Descripcion:

Este proyecto consiste en el desarrollo de una red P2P en anillo utilizando gRPC. La red permite distribuir y buscar canciones a través de nodos conectados, gestionando responsabilidades mediante la implementación del protocolo Chord/DHT. Los nodos pueden unirse o salir de la red, transfiriendo de forma segura sus responsabilidades a otros nodos.

#### 1.1. Aspectos Logrados:
  - Creacion de red P2P en anillo.
  - Creación de nodos capaces de enviar, almacenar y buscar canciones.
  - Implementación de una función hash para identificar y distribuir las canciones de manera uniforme entre los nodos.
  - Los nodos pueden entrar y salir de la red dinámicamente, actualizando sus predecesores y sucesores.
  - Delegación de responsabilidades cuando un nodo sale de la red
  - Uso de gRPC para la comunicación eficiente entre nodos.
  - Uso de hilos para peticiones concurrentes.
  - Desarrollo y pruebas en localhost.
  
#### 1.2. Aspectos NO Logrados
  - No se ha integrado un mecanismo de recuperación ante fallos inesperados de nodos en la red.
  - Despliegue en AWS
  - Partición de canciones

### 2. Información general de diseño:
  - **Diseño**
    - El sistema es una red P2P distribuida basada en el protocolo Chord/DHT, donde los nodos actúan tanto como servidores como clientes.Cada nodo en la red tiene la capacidad de almacenar, localizar y transferir canciones a otros nodos. El sistema utiliza gRPC para facilitar la comunicación eficiente entre nodos, manejando la incorporación y salida de nodos dinámicamente, así como la distribución y búsqueda de canciones de manera eficiente.
    - Los nodos están organizados en un anillo lógico utilizando DHT (Distributed Hash Table) para garantizar una estructura escalable, que permite localizar canciones en otros nodos. Cada nodo es responsable de un rango de canciones en función de su identificación en el anillo.

  - **Arquitectura**
    - **Anillo P2P**: Los nodos están organizados en un anillo en el que cada nodo tiene un identificador único generado mediante un hash (por ejemplo, usando SHA-1). Cada nodo es responsable de un conjunto de claves (en este caso, las canciones), y mantiene referencias a su predecesor y sucesor inmediato.
    - **Cliente/Servidor**: Cada nodo actúa como cliente cuando necesita localizar o solicitar una canción desde otro nodo, y como servidor cuando recibe solicitudes de otros nodos. Esto con una comunicación gRPC entre los nodos.

  - **Procesos principales**
    - **Entrada y salida de nodos**: Un nodo puede unirse a la red contactando a cualquier otro nodo ya existente. El nodo es asignado a una posición en el anillo según su ID, y su responsabilidad de gestionar canciones se ajusta dinámicamente. Cuando un nodo se desconecta, su responsabilidad es transferida al nodo correspondiente.
    - **Distribución y busqueda de canciones**:  Las canciones se distribuyen en los nodos según sus identificadores hash, que determinan el nodo responsable de cada canción. Las búsquedas de canciones es permitida gracias a la DHT de cada nodo, el cual la recorrera y encontrará quien tiene la canción solicitada.


- **Mejores practicas utilizadas**
  - **gRPC para Comunicación**: Utilización de gRPC para implementar las interfaces cliente-servidor de manera eficiente, facilitando la comunicación entre nodos.
  - **Protobuf**: Para la serialización de datos en la comunicación entre nodos, lo que permite transferir estructuras complejas.
  - **Concurrencia**: Los nodos utilizan threading para manejar múltiples solicitudes al mismo tiempo.
  - **Resiliencia y Escalabilidad**: Los nodos se unen o se retiran sin generar interrupciones en el servicio

## Caracteristicas del proyecto:

- **Red distribuida en Anillo**: Los nodos se organizan en una red P2P en anillo, utilizando el protocolo Chord para la asignación y búsqueda de recursos (canciones) de manera eficiente.
- **Gestion de Nodos**: Los nodos pueden unirse y salir de la red dinámicamente, actualizando las referencias a sus sucesores y predecesores de acuerdo con el protocolo Chord.
- Se redistribuyen las canciones cuando un nodo se desconecta, asegurando que no se pierdan datos.
- **Distribución de canciones**: Cada nodo almacena canciones de manera distribuida en la red, utilizando un hash SHA-1 para identificar la canción y asignarla al nodo responsable.
- **Búsqueda de canciones**: Los nodos pueden buscar canciones en la red. Si el nodo actual no tiene la canción solicitada, reenvía la solicitud a su sucesor en el anillo, continuando la búsqueda de manera distribuida hasta encontrar la canción.
- **Comunicación a Través de gRPC**: La comunicación entre los nodos se realiza utilizando gRPC, lo que permite una transmisión eficiente de mensajes entre los nodos para almacenar y buscar canciones, así como para gestionar la entrada y salida de nodos.
- **Hashing Distribuido (SHA-1)**: El proyecto usa hashing SHA-1 para distribuir uniformemente las responsabilidades entre los nodos. Cada nodo es responsable de un rango específico en el espacio de claves, lo que asegura un almacenamiento balanceado de las canciones.
- **Operaciones Concurrentes**: Se utiliza multithreading para manejar múltiples operaciones al mismo tiempo, lo que permite que un nodo procese varias solicitudes simultáneamente sin bloquear la ejecución.
- **Cambios en la red**: Los nodos pueden entrar y salir de la red sin interrumpir las operaciones de búsqueda y almacenamiento de canciones, gracias a la actualización automática de las referencias entre nodos.


## Tecnologias usadas:

- **Python**: Lenguaje de programación.
- **gRPC**: Permite la comunicación entre nodos.
- **Protocol Buffers (Protobuf)**: Serializa datos estructurados.

## Estructura del proyecto

```bash
.
├── ANILLO CON DHT              
├── __pycache__                       
│   ├── node_pb2_grpc.cpython-311.pyc                
│   └── node_pb2.cpython-311.pyc                
├── node_pb2_grpc.py
├── node_pb2.py
├── node.proto
├── node.py
└── README.md                    
```

## Setup e Instalación
# Ambiente de Desarrollo:
  - **Lenguaje**: Python 3.9
  - **Librerías y Paquetes**:
    - **grpcio** (version 1.39.0)
    - **protobus** (version 3.17.3)
    - **hashlib**: Para el cálculo de hashes.
    - **threading**: Para la ejecución en paralelo de hilos.

### 1. Clonar el repositorio

```bash
git clone https://github.com/THOMAS-RIVERA-F/Red-P2P-en-Anillo.git
cd Red-P2P-en-Anillo
```

### 2. Instalar python y las dependecias
- Descargar **python** desde: [text](https://www.python.org/downloads/)
- **Dependencias**:
```bash
pip install grpcio grpcio-tools protobuf
```

### 3. Compilar archivos generados por **protobuf**

Estando en la ruta del proyecto desde la terminal, ejecutar:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. node.proto
```

### 4. Ejecutar un nodo con el comando:

```bash
python node.py
```
puerto --> `50051`.

### 5. Unir a la red otro nodo. (Hacer para cada nodo que se quiera agregar, pero en distintas terminales)

```bash
python node.py
```

Ingresa un puerto para el nuevo nodo (ejemplo: `50052`, `50053`, .... , `60000`).
Nota: Los nodos adicionales se conectan especificando el puerto de otro nodo ya existente en la red.

### 6. Subir o descargar canciones (Para cualquier nodo ya que actuan como Cliente/Servidor)

Al estar en cualquiera de los nodos creados, surgira el siguiente menu para subir o pedir una canción:
```
--------------------------------------------------
| 1: Subir una cancion a la red    (en Anillo)   |
| 2: Buscar una cancion en la red  (En Anillo)   |
| 3: Subir una cancion a la red    (Con DHT)     |
| 4: Buscar una cancion en la red  (Con DHT)     |
| 5: Salir de la red                             |
--------------------------------------------------
```
##  Guía para utilizar el software (EJEMPLO):

1. Añade el primer nodo a la red:

- Terminal 1
```bash
python node.py
# Ingresar puerto: 50051
```

2. Red en anillo con 4 nodos:

- Terminal 2
```bash
python node.py
# Ingresar puerto: 50052
# Ingresar nodo ya existente a la red: 50051
```

- Terminal 3
```bash
python node.py
# Ingresar puerto: 50053
# Ingresar nodo ya existente a la red: (ejemplo: '50051' ó '50052')
```

- Terminal 4
```bash
python node.py
# Ingresar puerto: 50054
# Ingresar nodo ya existente a la red: (ejemplo: '50051' ó '50052' ó '50053')
```

3. Subir una cancion desde cualquiera de los nodos:
- Aparecerá este menú para cada nodo, ya que es Cliente/Servidor puede hacer cualquiera de estas opciones escribiendo en la consola cual quiere hacer. (opciones 1 y 3)

```
--------------------------------------------------
| 1: Subir una cancion a la red    (en Anillo)   |
| 2: Buscar una cancion en la red  (En Anillo)   |
| 3: Subir una cancion a la red    (Con DHT)     |
| 4: Buscar una cancion en la red  (Con DHT)     |
| 5: Salir de la red                             |
--------------------------------------------------
```

4. Descargar una canción desde un nodo:
- Para descargar una canción ya subida a la red, debera de oprimir las opciones 2 o 4.
```
--------------------------------------------------
| 1: Subir una cancion a la red    (en Anillo)   |
| 2: Buscar una cancion en la red  (En Anillo)   |
| 3: Subir una cancion a la red    (Con DHT)     |
| 4: Buscar una cancion en la red  (Con DHT)     |
| 5: Salir de la red                             |
--------------------------------------------------
```
Y asi sucesivamente se puede utilizar el software.

5. Salida de un nodo de la red:
- Oprimir la opción numero 5 para sacar a un nodo de la red, las responsabilidades de este serán transferidas al nodo correspondiente.
```
--------------------------------------------------
| 1: Subir una cancion a la red    (en Anillo)   |
| 2: Buscar una cancion en la red  (En Anillo)   |
| 3: Subir una cancion a la red    (Con DHT)     |
| 4: Buscar una cancion en la red  (Con DHT)     |
| 5: Salir de la red                             |
--------------------------------------------------
```
### Referencias
- Archivo compartido por el profesor: chord_sigcomm 
  - Titulo: Chord: A Scalable Peer-to-peer Lookup Service for Internet
Application de los autores: Ion Stoica , Robert Morris, David Karger, M. Frans Kaashoek, Hari Balakrishnan.
- [text](https://www.youtube.com/watch?v=1wTucsUm64s)
- Chatgpt
