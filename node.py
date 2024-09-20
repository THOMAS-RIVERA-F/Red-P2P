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
        

    # ========== SERVIDOR ==========
    
    def SendMessage(self, request, context):
        """Método para manejar la recepción de canciones y decidir si guardarlas o reenviarlas."""
        cancion_hash = self.do_hash(request.cancion)
        
        if self.id == self.successor.id:
            print('')
            print(f"Guardando canción '{cancion}' en el nodo con ID {self.id}")
            self.dic_mis_canciones[cancion_hash] = request.cancion
        elif (self.id < cancion_hash < self.successor.id) or (self.id > self.successor.id and cancion_hash > self.id):
            print('')
            print(f"Guardando canción '{request.cancion}' en el nodo con ID {self.id}")
            self.dic_mis_canciones[cancion_hash] = request.cancion
        else:
            # Reenviar al sucesor
            with grpc.insecure_channel(self.successor.address) as channel:
                stub = node_pb2_grpc.NodeServiceStub(channel)
                print(f"Reenviando canción '{request.cancion}' al sucesor con ID {self.successor.id}")
                stub.SendMessage(node_pb2.CancionRequest(cancion=request.cancion, tamano_cancion=request.tamano_cancion))
        return node_pb2.MessageResponse(reply=f"Cancion '{request.cancion}' recibida")


    def serve(self):
        """Método para iniciar el servidor gRPC (Servidor)"""
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_pb2_grpc.add_NodeServiceServicer_to_server(self, server)  # Registrar esta instancia del Nodo como servicio
        server.add_insecure_port(f'[::]:{self.port}')  # Usar el puerto ya definido en la instancia
        server.start()
        print(f"Node server started on port {self.port}")
        server.wait_for_termination()
    
    def FindSuccessor(self, request, context):
        """Método que encuentra el sucesor adecuado para un nodo nuevo que quiere unirse."""
        print(f"Buscando sucesor para el nodo con ID {request.id}")
        
        
        # Caso 2: El ID del sucesor es menor que el ID del nodo actual y el ID del solicitante es mayor que el ID del nodo actual
        if self.id > self.successor.id and self.id < request.id:
            print(f"El nodo actual ({self.id}) es el sucesor adecuado (rango cruzando el límite superior).")
            return node_pb2.SuccessorResponse(successor_address=self.successor.address, predecessor_address=self.address)
        elif self.id < request.id <= self.successor.id or self.successor.id == self.id:
            print(f"El nodo actual ({self.id}) es el sucesor adecuado.")
            return node_pb2.SuccessorResponse(successor_address=self.successor.address, predecessor_address=self.address)
        else:
            with grpc.insecure_channel(self.successor.address) as channel:
                print("redirijiendo")
                stub = node_pb2_grpc.NodeServiceStub(channel)
                response = stub.FindSuccessor(request)
                #print(f"Enviando respuesta de sucesor: {response.successor}")
                return response
    
    def BuscarResponsabilidades(self, request, context):
        id_solicitante = request.id
        
        # Filtrar items del diccionario que tengan clave mayor al id del solicitante
        items_responsables = {k: v for k, v in self.dic_mis_canciones.items() if k > id_solicitante}
    
        # Eliminar del diccionario original las claves que se han asignado a otro nodo
        for key in items_responsables.keys():
            del self.dic_mis_canciones[key]
        
        # Crear la respuesta con los items filtrados
        return node_pb2.ResponsabilidadesResponse(items=items_responsables)
    

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


    # ========== CLIENTE ==========
    
    def send_cancion(self, cancion, tamano_cancion):
        cancion_hash = self.do_hash(cancion)
        print(f"Hash de la canción '{cancion}': {cancion_hash}")
        
        # Si el nodo actual es responsable del hash de la canción
        if self.id == self.successor.id:
            print('')
            print(f"Guardando canción '{cancion}' en el nodo con ID {self.id}")
            self.dic_mis_canciones[cancion_hash] = cancion
        elif (self.id < cancion_hash < self.successor.id) or (self.id > self.successor.id and cancion_hash > self.id):
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
    
    def buscar_mis_responsabilidades(self, predecessor_address):
        
        with grpc.insecure_channel(f'localhost:{predecessor_address}') as channel:
            stub = node_pb2_grpc.NodeServiceStub(channel)
            # Crear el request con mi ID
            request = node_pb2.ResponsabilidadesRequest(id=self.id)
        
            # Hacer la solicitud al predecesor
            response = stub.BuscarResponsabilidades(request)
            # Retornar los items recibidos como un diccionario
            return dict(response.items)

    
    def search_cancion(self, cancion_buscar):
        pass
            
            
    def client_loop(self):
        """Bucle del cliente para enviar mensajes o solicitar el ID de otro nodo (Cliente)"""
        while True:
            option = input("Escoge una opcion (1: Subir una cancion a la red, 2: Buscar una cancion en la red): ")
            print('')
            
            if option == "1":
                cancion = input("Ingresa la cancion a subir: ")
                t_cancion = input("Ingrese el tamaño del archivo (ej: 12 MB): ")
                tamano_cancion = int(t_cancion.split(' ')[0])
                self.send_cancion(cancion, tamano_cancion)
            elif option == "2":
                cancion_buscar = input("Ingresa la cancion a buscar: ")
                self.search_cancion(cancion_buscar)
    
    def join_network(self, bootstrap_node=None):
        """Método para unirse a la red."""
        if bootstrap_node is None:
            # El primer nodo de la red es su propio sucesor y predecesor
            self.successor = self
            self.predecessor = self
            print('')
            print(f"Soy el primer nodo en la red con ID: {self.id}")
        else:
            # Si hay un bootstrap node, unirse a la red a través de él
            self.join_existing_network(bootstrap_node)
        

    def join_existing_network(self, bootstrap_node_address):
        """Método para unirse a una red existente usando un nodo bootstrap."""
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
            
            #buscar responsabilidades que debe tener el nodo que eran de mi predecesor
            dic_mis_responsabilidades = self.buscar_mis_responsabilidades(int(response.predecessor_address.split(":")[-1]))
            self.dic_mis_canciones = dic_mis_responsabilidades | self.dic_mis_canciones
            print(f"Responsabilidades del nodo actual: {self.dic_mis_canciones}")
            
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

        print('')
        print("Solicitando información del nodo...")
        # Determinar si este es el primer nodo o si se unirá a una red existente
        is_first_node = input("¿Es este el primer nodo en la red? (s/n): ").lower()

        if is_first_node == 's':
            # Si es el primer nodo, no hay bootstrap node
            self.join_network()
        else:
            # Si no es el primer nodo, solicitar la dirección del nodo bootstrap
            bootstrap_port = input("Ingrese el puerto de algun nodo de la red a unirse (ej. 50051): ")
            bootstrap_address = f'localhost:{bootstrap_port}'
            self.join_network(bootstrap_node=bootstrap_address)
            
        print('')
        print("El nodo se ha unido a la red. Listo para subir o buscar canciones...")

        # Ejecutar el cliente en el hilo principal
        self.client_loop()



if __name__ == '__main__':
    port = input('Ingrese el puerto para este nodo: ')
    node = Node(port)
    node.run()

