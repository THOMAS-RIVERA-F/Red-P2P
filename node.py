import grpc
from concurrent import futures
import threading
import node_pb2_grpc
import node_pb2
import hashlib


class Node(node_pb2_grpc.NodeServiceServicer):

    def __init__(self, port):
        # Inicialización del nodo
        self.port = port
        self.address = f'localhost:{port}'  # Dirección con formato 'localhost:puerto'
        self.id = self.do_hash(self.address)  # Hash único basado en la dirección del nodo
        self.successor = None  # Nodo sucesor, se inicializa vacío
        self.predecessor = None  # Nodo predecesor, se inicializa vacío
        self.dic_mis_canciones = {} # Diccionario para guardar las cancionces de las que soy responsable
        self.DHT_nodos = {}
        

    # ========== SERVIDOR ==========
    

    def serve(self):
        """Método para iniciar el servidor gRPC (Servidor)"""
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_NodeServiceServicer_to_server(self, server)  # Registrar esta instancia del Nodo como servicio
        server.add_insecure_port(f'[::]:{self.port}')  # Usar el puerto ya definido en la instancia
        server.start()
        server.wait_for_termination()
    
    
    # =================== ACTUALIZAR SUCESOR Y PREDECESOR ========================

    # Método para actualizar el predecesor del nodo actual
    def UpdatePredecessor(self, request, context):
        self.predecessor = Node(request.new_predecessor_address.split(":")[-1])
        self.predecessor.address = request.new_predecessor_address
        return node_pb2.EmptyResponse()

    # Método para actualizar el sucesor del nodo actual
    def UpdateSuccessor(self, request, context):
        self.successor = Node(request.new_successor_address.split(":")[-1])
        self.successor.address = request.new_successor_address
        return node_pb2.EmptyResponse()


    # =================== SALIR DE LA RED ========================
    
    def salir_de_la_red(self):
        
        self.enviar_diccionario()
        
        del self.DHT_nodos[self.id]
        self.actualizar_todas_las_dht()
        
        # Actualizar sucesor del nodo predecesor
        with grpc.insecure_channel(self.predecessor.address) as channel_pred:
            stub_pred = node_pb2_grpc.NodeServiceStub(channel_pred)
            stub_pred.UpdateSuccessor(node_pb2.UpdateRequest(new_successor_address=self.successor.address, new_predecessor_address=""))
        
        # Actualizar predecesor del nodo sucesor
        with grpc.insecure_channel(self.successor.address) as channel_succ:
            stub_succ = node_pb2_grpc.NodeServiceStub(channel_succ)
            stub_succ.UpdatePredecessor(node_pb2.UpdateRequest(new_predecessor_address=self.predecessor.address, new_successor_address=""))
        
        print(f"Me he retirado de la red.")
    
    #================== BUSCAR RESPONSABILIDADES ========================
    
    def buscar_mis_responsabilidades(self, predecessor_port):
        
        with grpc.insecure_channel(f'localhost:{predecessor_port}') as channel:
            print("Conectando con el predecesor...", predecessor_port)
            stub = node_pb2_grpc.NodeServiceStub(channel)
            # Crear el request con mi ID
            request = node_pb2.ResponsabilidadesRequest(id=self.id)
        
            # Hacer la solicitud al predecesor
            response = stub.BuscarResponsabilidades(request)
            # Retornar los items recibidos como un diccionario
            return dict(response.items)
    
    def BuscarResponsabilidades(self, request, context):
        id_solicitante = request.id
        
        items_responsables1 = {}
        items_responsables2 = {}
        
        # Filtrar items del diccionario que tengan clave mayor al id del solicitante
        items_responsables1 = {k: v for k, v in self.dic_mis_canciones.items() if k > id_solicitante}
        
        #filtrar items del diccionario que tengan clave menor a mi id (caso 0)
        items_responsables2 = {k: v for k, v in self.dic_mis_canciones.items() if k < self.id}

        # Unir los items filtrados
        items_responsables = items_responsables1|items_responsables2
        
        # Eliminar del diccionario original las claves que se han asignado a otro nodo
        for key in items_responsables.keys():
            del self.dic_mis_canciones[key]
        
        print(f"Responsabilidades del nodo actual: {self.dic_mis_canciones}")
        
        # Crear la respuesta con los items filtrados
        return node_pb2.ResponsabilidadesResponse(items=items_responsables)

    def enviar_diccionario(self):
        # Enviar el diccionario al nodo destino
        with grpc.insecure_channel(self.predecessor.address) as channel:
            print(f'print{self.predecessor.address}')
            stub = node_pb2_grpc.NodeServiceStub(channel)
            response = stub.UpdateDiccionario(node_pb2.DiccionarioRequest(diccionario=self.dic_mis_canciones))
            print(response.reply)
    
    def UpdateDiccionario(self, request, context):
        # Recibir el diccionario y actualizar el diccionario actual
        self.dic_mis_canciones = self.dic_mis_canciones | dict(request.diccionario)
        print("Diccionario actualizado.")
        print(f"Responsabilidades del nodo actual: {self.dic_mis_canciones}")
        return node_pb2.MessageResponse(reply="Diccionario recibido con éxito.")
    
    #================== BUSCAR CANCIONES ========================
    
    def buscar_cancion(self, cancion_buscada):
        requester_id = self.id
        hash_cancion = self.do_hash(cancion_buscada)
        
        print(f"Buscando la canción '{cancion_buscada}' con hash: {hash_cancion}")
        
        if hash_cancion in self.dic_mis_canciones.keys():
            print(f"La canción '{cancion_buscada}' se encuentra en el nodo con ID: {self.id}")
            
        else:
            print(f"Reenviando la solicitud de búsqueda al sucesor con ID {self.successor.id}")
            # Si no es responsable, reenviar la solicitud al sucesor
            with grpc.insecure_channel(self.successor.address) as channel:
                
                stub = node_pb2_grpc.NodeServiceStub(channel)
                #request = node_pb2.BuscarCancionRequest(cancion = cancion_buscada, requester_id = requester_id)
                
                response = stub.BuscarCancion(node_pb2.BuscarCancionRequest(cancion=cancion_buscada, requester_id=requester_id))
                
                if response.id_nodo == -1:
                    print(f"La canción '{cancion_buscada}' no se encontró en toda la red.")
                else:
                    print(f"La canción '{cancion_buscada}' se encuentra en el nodo con ID: {response.id_nodo}")
                    
                
                    
    def BuscarCancion(self, request, context):
        hash_cancion = self.do_hash(request.cancion)
        id_solicitante = request.requester_id
        
        if hash_cancion in self.dic_mis_canciones.keys():
            # Si la canción está en este nodo
            print(f'Yo nodo {self.id} tengo la cancion {request.cancion}')
            print(f"Se la enviare a {id_solicitante}")
            return node_pb2.BuscarCancionResponse(cancion=request.cancion, id_nodo=self.id)
        else:
            # Si no es la canción de este nodo y aún no se ha cerrado el ciclo
            if id_solicitante != self.id:
                print(f"La canción '{request.cancion}' no es responsabilidad de: {self.id}, reenviando al sucesor.")
                with grpc.insecure_channel(self.successor.address) as channel:
                    stub = node_pb2_grpc.NodeServiceStub(channel)
                    return stub.BuscarCancion(request)
            else:
                # Si ha dado toda la vuelta y no se encontró
                print(f"La canción '{request.cancion}' no se encontró en toda la red.")
                return node_pb2.CancionResponse(cancion='', id_nodo=-1)

    
    def buscar_cancion_dht(self, cancion_buscada):
        hash_cancion = self.do_hash(cancion_buscada)
        claves_ordenadas = sorted(self.DHT_nodos.keys())
        
        ultimo_nodo = claves_ordenadas[-1]
        primer_nodo = claves_ordenadas[0]
        
        if hash_cancion > ultimo_nodo or hash_cancion < primer_nodo:
            succ_address = self.DHT_nodos[ultimo_nodo]
        else:
            nodo_correspondiente = max([k for k in claves_ordenadas if k <= hash_cancion])
            succ_address = self.DHT_nodos[nodo_correspondiente]
        
        with grpc.insecure_channel(succ_address) as channel:
            stub = node_pb2_grpc.NodeServiceStub(channel)
            response = stub.BuscarCancion(node_pb2.BuscarCancionRequest(cancion=cancion_buscada, requester_id=self.id))
            if response.id_nodo == -1:
                print(f"La canción '{cancion_buscada}' no se encontró en toda la red.")
            else:
                print(f"La canción '{cancion_buscada}' se encuentra en el nodo con ID: {response.id_nodo}")
                
    # ====================== DHT =========================== 
    
    def actualizar_todas_las_dht(self):
        for id, address in self.DHT_nodos.items():
            if id != self.id:
                with grpc.insecure_channel(address) as channel:
                    stub = node_pb2_grpc.NodeServiceStub(channel)
                    response = stub.ActualizarDhts(node_pb2.NewDht(diccionario_new_dht=self.DHT_nodos))
                    
    
    
    def ActualizarDhts(self, request, context):
        self.DHT_nodos = dict(request.diccionario_new_dht)
        self.imprimir_diccionario()
        return node_pb2.MessageResponse(reply=f"DHT actualizada con éxito.")
    
    
    def PedirDHT(self, request, context):
        print(f"Enviando la DHT al nodo con ID {request.id}, que se ha unido a la red.")
        return node_pb2.DhtResponse(diccionario_dht=self.DHT_nodos)
    
    # ====================== SUBIR CANCIONES A LA RED =========================
    
    def send_cancion(self, cancion, tamano_cancion):
        cancion_hash = self.do_hash(cancion)
        print(f"Hash de la canción '{cancion}': {cancion_hash}")
        
        # Si el nodo actual es responsable del hash de la canción
        if self.id == self.successor.id:
            print('')
            print(f"Guardando canción '{cancion}' en el nodo con ID {self.id}")
            self.dic_mis_canciones[cancion_hash] = cancion
        elif (self.id < cancion_hash < self.successor.id) or (self.id > self.successor.id and cancion_hash > self.id) or (self.id > self.successor.id and cancion_hash < self.successor.id):
            print('')
            print(f"Guardando canción '{cancion}' en el nodo con ID {self.id}")
            self.dic_mis_canciones[cancion_hash] = cancion
        else:
            # Si no es el nodo responsable, reenviar la canción al sucesor
            with grpc.insecure_channel(self.successor.address) as channel:
                stub = node_pb2_grpc.NodeServiceStub(channel)
                print('')
                print(f"Reenviando canción '{cancion}' al sucesor con ID {self.successor.id}")
                stub.SendMessage(node_pb2.CancionRequest(cancion=cancion, tamano_cancion=tamano_cancion))
                
    
    def enviar_cancion_dht(self, cancion1):
        hash_cancion = self.do_hash(cancion1)
        claves_ordenadas = sorted(self.DHT_nodos.keys())
        
        ultimo_nodo = claves_ordenadas[-1]
        primer_nodo = claves_ordenadas[0]
        
        if hash_cancion > ultimo_nodo or hash_cancion < primer_nodo:
            succ_address = self.DHT_nodos[ultimo_nodo]
        else:
            nodo_correspondiente = max([k for k in claves_ordenadas if k <= hash_cancion])
            succ_address = self.DHT_nodos[nodo_correspondiente]
        
        print(f"Enviando la canción '{cancion1}' al nodo con direccion {succ_address}")
        
        with grpc.insecure_channel(succ_address) as channel:
            stub = node_pb2_grpc.NodeServiceStub(channel)
            response = stub.SendMessage(node_pb2.CancionRequest(cancion=cancion1, tamano_cancion=0))
            print(response.reply)
    
    
    def SendMessage(self, request, context):
        """Método para manejar la recepción de canciones y decidir si guardarlas o reenviarlas."""
        cancion_hash = self.do_hash(request.cancion)
        
        if self.id == self.successor.id:
            print('')
            print(f"Guardando canción '{cancion}' en el nodo con ID {self.id}")
            self.dic_mis_canciones[cancion_hash] = request.cancion
        elif (self.id < cancion_hash < self.successor.id) or (self.id > self.successor.id and cancion_hash > self.id) or (self.id > self.successor.id and cancion_hash < self.successor.id):
            print('')
            print(f"Guardando canción '{request.cancion}' en el nodo con ID {self.id}")
            self.dic_mis_canciones[cancion_hash] = request.cancion
        else:
            # Reenviar al sucesor
            with grpc.insecure_channel(self.successor.address) as channel:
                stub = node_pb2_grpc.NodeServiceStub(channel)
                print(f"Reenviando canción '{request.cancion}' al sucesor con ID {self.successor.id}")
                stub.SendMessage(node_pb2.CancionRequest(cancion=request.cancion, tamano_cancion=request.tamano_cancion))
        
        print(f"Responsabilidades del nodo actual: {self.dic_mis_canciones}")
        
        return node_pb2.MessageResponse(reply=f"Cancion '{request.cancion}' recibida")

    # ====================== UNIÓN A LA RED =========================

    def join_network(self, bootstrap_node=None):
        """Método para unirse a la red."""
        if bootstrap_node is None:
            # El primer nodo de la red es su propio sucesor y predecesor
            self.successor = self
            self.predecessor = self
            print('')
            print(f"Soy el primer nodo en la red con ID: {self.id}")
            self.DHT_nodos[self.id] = self.address
            self.imprimir_diccionario()
        else:
            # Si hay un bootstrap node, unirse a la red a través de él
            self.join_existing_network(bootstrap_node)
    
    def imprimir_diccionario(self):
        print("DHT actualizada: ")
        for key, value in self.DHT_nodos.items():
            print(f"| id: {key} -> address: {value}|")
        print('\n')
        

    def join_existing_network(self, bootstrap_node_address):
        """Método para unirse a una red existente usando un nodo bootstrap."""
        print(f'Soy el nodo con ID: {self.id}')
        with grpc.insecure_channel(bootstrap_node_address) as channel:
            stub = node_pb2_grpc.NodeServiceStub(channel)
            print("Intentando encontrar el sucesor...")
            response = stub.FindSuccessor(node_pb2.NodeIDRequest(id=self.id))
            print('')
            print(f"Sucesor encontrado: {response.successor_address}")

            # Asignar el sucesor y predecesor basados en la respuesta
            
            successor = Node(int(response.successor_address.split(":")[-1])) 
            predecessor = Node(int(response.predecessor_address.split(":")[-1])) 
            
            successor.address = response.successor_address
            predecessor.address = response.predecessor_address 
            
            self.successor = successor
            self.predecessor = predecessor
            
            
            print(f"Me uní a la red.")
            print()
            
            # Actualizar sucesor del nodo predecesor
            with grpc.insecure_channel(self.predecessor.address) as channel_pred:
                stub_pred = node_pb2_grpc.NodeServiceStub(channel_pred)
                
                stub_pred.UpdateSuccessor(node_pb2.UpdateRequest(new_successor_address=self.address, new_predecessor_address=""))
            
            # Actualizar predecesor del nodo sucesor
            with grpc.insecure_channel(self.successor.address) as channel_succ:
                stub_succ = node_pb2_grpc.NodeServiceStub(channel_succ)
                                
                stub_succ.UpdatePredecessor(node_pb2.UpdateRequest(new_predecessor_address=self.address, new_successor_address=""))

            print(f"Mi ID: {self.id}, Sucesor: {self.successor.id}, Predecesor: {self.predecessor.id}")
            
            #buscar responsabilidades que debe tener el nodo que eran de mi predecesor
            dic_mis_responsabilidades = self.buscar_mis_responsabilidades(self.predecessor.port)
            self.dic_mis_canciones = dic_mis_responsabilidades | self.dic_mis_canciones
            print(f"Responsabilidades del nodo actual: {self.dic_mis_canciones}")
            
            with grpc.insecure_channel(self.predecessor.address) as channel:
                stub_pred2 = node_pb2_grpc.NodeServiceStub(channel)
                response = stub_pred2.PedirDHT(node_pb2.DhtRequest(id = self.id))
                self.DHT_nodos = dict(response.diccionario_dht)
                self.DHT_nodos[self.id] = self.address
                self.imprimir_diccionario()
            
            self.actualizar_todas_las_dht()
        
    def FindSuccessor(self, request, context):
        """Método que encuentra el sucesor adecuado para un nodo nuevo que quiere unirse."""
        print(f"Buscando sucesor para el nodo con ID {request.id} \n")
        
        
        # Caso 2: El ID del sucesor es menor que el ID del nodo actual y el ID del solicitante es mayor que el ID del nodo actual
        if self.id > self.successor.id and self.id < request.id:
            return node_pb2.SuccessorResponse(successor_address=self.successor.address, predecessor_address=self.address)
        elif self.id < request.id <= self.successor.id or self.successor.id == self.id:
            return node_pb2.SuccessorResponse(successor_address=self.successor.address, predecessor_address=self.address)
        else:
            with grpc.insecure_channel(self.successor.address) as channel:
                print("redirijiendo \n")
                stub = node_pb2_grpc.NodeServiceStub(channel)
                response = stub.FindSuccessor(request)
                return response
     
    
    # ================== LOOP DEL CLIENTE =================
    
    def client_loop(self):
        """Bucle del cliente para enviar mensajes o solicitar el ID de otro nodo (Cliente)"""
        while True:
            print('--------------------------------------------------')
            print('| 1: Subir una cancion a la red    (en Anillo)   |')
            print('| 2: Buscar una cancion en la red  (En Anillo)   |')
            print('| 3: Subir una cancion a la red    (Con DHT)     |')
            print('| 4: Buscar una cancion en la red  (Con DHT)     |')
            print('| 5: Salir de la red                             |')
            print('--------------------------------------------------')
            option = input('Ingrese el número de la opción deseada: ')
            print('\n')
            
            
            if option == "1":
                cancion = input("Ingresa la cancion a subir: ")
                t_cancion = input("Ingrese el tamaño del archivo (ej: 12 MB): ")
                tamano_cancion = int(t_cancion.split(' ')[0])
                self.send_cancion(cancion, tamano_cancion)
            elif option == "2":
                cancion_buscar = input("Ingresa la cancion a buscar: ")
                self.buscar_cancion(cancion_buscar)
            elif option == "3":
                cancion1 = input("Ingresa la cancion a subir: ")
                t_cancion = input("Ingrese el tamaño del archivo (ej: 12 MB): ")
                tamano_cancion = int(t_cancion.split(' ')[0])
                self.enviar_cancion_dht(cancion1)
            elif option == "4":
                cancion_buscar = input("Ingresa la cancion a buscar: ")
                self.buscar_cancion_dht(cancion_buscar)
            elif option == "5":
                self.salir_de_la_red()
                break
                  
 
    # ========== UTILIDADES ==========
    def do_hash(self, string):
        """Generar un hash único basado en la dirección del nodo"""
        hash_object = hashlib.sha1(string.encode())
        hash_num = (int(hash_object.hexdigest(), 16)) % 100000  # Convertir a entero y limitar el tamaño del hash
        return hash_num

    # ========== EJECUCIÓN ==========

    def run(self):
        """Ejecutar servidor y cliente en paralelo"""

        # Crear y lanzar el hilo del servidor
        server_thread = threading.Thread(target=self.serve, daemon=True)
        server_thread.start()

        is_first_node = input("¿Es este el primer nodo en la red? (s/n): ").lower()

        if is_first_node == 's':
            # Si es el primer nodo, no hay bootstrap node
            self.join_network()
        else:
            # Si no es el primer nodo, solicitar la dirección del nodo bootstrap
            bootstrap_port = input("Ingrese el puerto de algun nodo de la red a unirse (ej. 50051): ")
            bootstrap_address = f'localhost:{bootstrap_port}'
            self.join_network(bootstrap_node=bootstrap_address)
            
        print(' ')
        print("El nodo se ha unido a la red. Listo para subir o buscar canciones...")

        # Ejecutar el cliente en el hilo principal
        self.client_loop()



if __name__ == '__main__':
    port = input('Ingrese el puerto para este nodo: ')
    node = Node(port)
    node.run()

