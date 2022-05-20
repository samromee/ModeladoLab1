import numpy as np

class simplex:
    variableZ = (int(input("Digite el numero de variables en Z: ")))
    inecuaciones = (int(input("Digite el numero de inecuaciones: ")))
    filas = inecuaciones + 1
    columnas = inecuaciones + variableZ + 2
    restrictions = []
    matriz_2 = []
    lista = []
    respuestas = {}
    maxiRespuesta= (input("Digite min se desea minimizar o max si desea maximizar: "))
    maximize = True
    variables = []
    filaPivote = 0
    bandera = 1
    elemento_pivote = 1
    objective = []
    columnaPivote = 0
    
    def __init__(self):
            self.print_simplex()
       
    def crear_matriz(self, matriz):
        for i in range(self.filas):
            matriz.append([])
            for j in range(self.columnas):
                matriz[i].append(None)
        return matriz

    #Encuentra la columna pivote
    def encontrar_columpiv(self, matriz, maximize):
        num_pivoteZ = 0
        
        if (maximize == True):
            for j in range(self.columnas):
                if matriz[self.filas - 1][j] < 0 and matriz[self.filas - 1][j] < num_pivoteZ:
                    num_pivoteZ = matriz[self.filas - 1][j]
                    self.columnaPivote = j
        else:
            for j in range(self.columnas):
                if matriz[self.filas - 1][j] > 0 and matriz[self.filas - 1][j] > num_pivoteZ:
                    num_pivoteZ = matriz[self.filas - 1][j]
                    self.columnaPivote = j
                    
    #Encuentra el elemento pivote de la columna pivote
    def encontrar_elemento_pivote(self, matriz):
        num_menor = 1000
        for i in range(self.filas - 1):
            if matriz[i][self.columnaPivote]==0 or matriz[i][self.columnas - 1] / matriz[i][self.columnaPivote] < 0:
                continue
            else:
                if i == 0:
                    num_menor = matriz[i][self.columnas - 1] / matriz[i][self.columnaPivote]
                    self.filaPivote = i
                    self.elemento_pivote = matriz[i][self.columnaPivote]
                elif matriz[i][self.columnas - 1] / matriz[i][self.columnaPivote] < num_menor:
                    num_menor = matriz[i][self.columnas - 1] / matriz[i][self.columnaPivote]
                    self.filaPivote = i
                    self.elemento_pivote = matriz[i][self.columnaPivote]
        self.lista.append(self.filaPivote)
        return self.elemento_pivote


    def encontrarFilaEntrante(self, matriznueva,matrizvieja):
        for j in range(self.columnas):
            matriznueva[self.filaPivote][j] = matrizvieja[self.filaPivote][j] / self.elemento_pivote


    def reorganizar_matriz(self, matriznueva):
        for i in range(self.filas):
            for j in range(self.columnas):
                if i != self.filaPivote:
                    self.matriz_2[i][j] = self.restrictions[i][j]-(self.restrictions[i][self.columnaPivote]*self.matriz_2[self.filaPivote][j])

    def encontrarNegativos(self, matriznueva):
        negativo = None
        for j in range(self.columnas-1):
            if matriznueva[self.filas-1][j] < 0:
                self.bandera = 1
                negativo = matriznueva[self.filas-1][j]
            elif negativo == None:
                self.bandera = 0
        return self.bandera

    def imprimir_matriz(self, matriz):
        for i in range(self.filas):
            tot= ""
            for j in range(self.columnas):
                tot = tot + str(matriz[i][j]) + "   "
            print(tot)
        print()

    def limpiar_matriz(self, matriznueva, matrizvacia, filas, columnas):
        for i in range(filas):
            for j in range(columnas):
                matriznueva[i][j]=matrizvacia[i][j]
                
    #Metodo para pedir los parametros de simplex           
    def print_simplex(self):
        
        #Rellena variables con el nombre de las variables
        for i in range(self.filas):
            if i < self.filas-1:
                self.respuestas["S" + str(i+1)]= 0
            else:
                self.respuestas["Z"] = 0 
                
        #Se crean las matrices
        self.restrictions= self.crear_matriz(self.restrictions)
        self.matriz_2= self.crear_matriz(self.matriz_2)              
        if(self.maxiRespuesta.lower() != "max"):
            self.maximize = False
                        
        #se llama al metodo simplex
        self.metodo_simplex(self.objective, self.restrictions, self.variables, self.maximize)
                           
    def rellena_matriz(self, objective, restrictions):
        
        for k in range(self.columnas-1):
            if(objective[k]>0):
                self.restrictions[self.filas][k] = objective[k]*(-1)
            else:
                 self.restrictions[self.filas][k] = objective[k]
                

    def metodo_simplex(self, objective, restrictions, variables, maximize): 
         
        self.columnas = len(objective)
        for i in range (len(variables)):
            if(variables[i].find('S')!=-1):   
                self.filas = self.filas+1
        
        self.maximize = maximize
        
        for k in range(len(objective)):
            self.objective[k] = objective[k]
        
        for k in range(len(variables)):
            self.variables[k] = variables[k]
        
        for k in range(len(restrictions)):
            self.restrictions[k] = restrictions[k]
            for j in range(len(restrictions[k])):
                self.restrictions[k][j] = restrictions[k][j]
                
        self.rellena_matriz
                                
        while self.bandera == 1:
            self.imprimir_matriz(self.restrictions)
            self.encontrar_columpiv(self.restrictions, self.maximize)
            self.elemento_pivote = self.encontrar_elemento_pivote(self.restrictions)
            self.encontrarFilaEntrante(self.matriz_2, self.restrictions)
            self.reorganizar_matriz(self.matriz_2)
            self.bandera = self.encontrarNegativos(self.restrictions)
            print(str(self.bandera))
            print(self.elemento_pivote)
            for i in range(self.filas):
                if i == self.filaPivote:
                    try:
                        self.respuestas["X" + str(i + 1)] = self.respuestas.pop("S" + str(i + 1))
                    except:
                        self.respuestas["X" + str(i + 1)] = self.matriz_2[i][self.columnas - 1]
                elif i == self.filas - 1:
                    self.respuestas["Z"] = self.matriz_2[i][self.columnas - 1]

            for i in range(self.filas):
                for j in range(len(self.lista)):
                    if i == self.lista[j]:
                        self.respuestas["X" + str(i + 1)] = self.matriz_2[i][self.columnas - 1]

            for i in range(self.filas):
                for j in range(self.columnas):
                    self.restrictions[i][j]=self.matriz_2[i][j]
            for i in range(self.filas):
                for j in range(self.columnas):
                    self.matriz_2[i][j]= None

        print("Respuestas: ")
        for key, value in self.respuestas.items():
            print(key + " = ", value)
            
simplex1 = simplex()
        
        
    
        
    
    
