import numpy as np

class simplex:
    numero_varZ = (int(input("Digite el numero de variables en Z: ")))
    numero_inec = (int(input("Digite el numero de inecuaciones: ")))
    num_filas = numero_inec + 1
    num_colum = numero_inec + numero_varZ + 2
    restrictions = []
    matriz_2 = []
    lista = []
    respuestas = {}
    maxiRespuesta= (input("Digite min se desea minimizar o max si desea maximizar: "))
    maximize = True
    variables = []
    fila_pivot = 0
    salidaaux = 1
    elemento_pivote = 1
    objective = []
    colum_pivote = 0
    
    def crear_matriz(self, matriz):
        for i in range(self.num_filas):
            matriz.append([])
            for j in range(self.num_colum):
                matriz[i].append(None)
        return matriz

    #Encuentra la columna pivote
    def encontrar_columpiv(self, matriz, maximize):
        num_pivoteZ = 0
        
        if (maximize == True):
            for j in range(self.num_colum):
                if matriz[self.num_filas - 1][j] < 0 and matriz[self.num_filas - 1][j] < num_pivoteZ:
                    num_pivoteZ = matriz[self.num_filas - 1][j]
                    self.colum_pivote = j
        else:
            for j in range(self.num_colum):
                if matriz[self.num_filas - 1][j] > num_pivoteZ:
                    num_pivoteZ = matriz[self.num_filas - 1][j]
                    self.colum_pivote = j
                    
    #Encuentra el elemento pivote de la columna pivote
    def encontrar_elemento_pivote(self, matriz):
        num_menor = 1000
        for i in range(self.num_filas - 1):
            if matriz[i][self.colum_pivote]==0 or matriz[i][self.num_colum - 1] / matriz[i][self.colum_pivote] < 0:
                continue
            else:
                if i == 0:
                    num_menor = matriz[i][self.num_colum - 1] / matriz[i][self.colum_pivote]
                    self.fila_pivot = i
                    self.elemento_pivote = matriz[i][self.colum_pivote]
                elif matriz[i][self.num_colum - 1] / matriz[i][self.colum_pivote] < num_menor:
                    num_menor = matriz[i][self.num_colum - 1] / matriz[i][self.colum_pivote]
                    self.fila_pivot = i
                    self.elemento_pivote = matriz[i][self.colum_pivote]
        self.lista.append(self.fila_pivot)
        return self.elemento_pivote


    def fila_entrante(self, matriznueva,matrizvieja):
        for j in range(self.num_colum):
            matriznueva[self.fila_pivot][j] = matrizvieja[self.fila_pivot][j] / self.elemento_pivote


    def reorganizar_matriz(self, matriznueva):
        for i in range(self.num_filas):
            for j in range(self.num_colum):
                if i != self.fila_pivot:
                    self.matriz_2[i][j] = self.restrictions[i][j]-(self.restrictions[i][self.colum_pivote]*self.matriz_2[self.fila_pivot][j])

    def hay_negativos(self, matriznueva):
        negativo = None
        for j in range(self.num_colum-1):
            if matriznueva[self.num_filas-1][j] < 0:
                self.salidaaux = 1
                negativo = matriznueva[self.num_filas-1][j]
            elif negativo == None:
                self.salidaaux = 0
        return self.salidaaux

    def imprimir_matriz(self, matriz):
        for i in range(self.num_filas):
            tot= ""
            for j in range(self.num_colum):
                tot = tot + str(matriz[i][j]) + "   "
            print(tot)
        print()

    def limpiar_matriz(self, matriznueva, matrizvacia, num_filas, num_colum):
        for i in range(num_filas):
            for j in range(num_colum):
                matriznueva[i][j]=matrizvacia[i][j]
                
    #Metodo para pedir los parametros de simplex           
    def print_simplex(self):
        
        #Rellena variables con el nombre de las variables
        for i in range(self.num_filas):
            if i < self.num_filas-1:
                self.respuestas["S" + str(i+1)]= 0
                self.variables.append("S" + str(i+1))
            else:
                self.respuestas["Z"] = 0 
                self.variables.append("Z")
                
        #Se crean las matrices
        self.restrictions= self.crear_matriz(self.restrictions)
        self.matriz_2= self.crear_matriz(self.matriz_2)
        
        #Se rellena matriz restrictions
        for i in range(self.num_filas):
            for j in range(self.num_colum):
                if j == 0 and i != self.num_filas - 1:
                    self.restrictions[i][j] = 0
                elif j == 0 and i == self.num_filas - 1:
                    self.restrictions[i][j] = 1
                elif 0 < j <= self.numero_varZ and i != self.num_filas - 1:
                    self.restrictions[i][j] = int(
                        input("Digite el coeficiente de la variable " + str(j) + " de la ecuacion " + str(i + 1) + ": "))
                elif j == self.num_colum - 1 and i != self.num_filas - 1:
                    self.restrictions[i][j] = int(input("Digite el coeficiente al que esta igualado la ecuacion " + str(i + 1) + ": "))
                elif 0 < j <= self.numero_varZ and i == self.num_filas - 1:
                    self.restrictions[i][j] =int(input("Digite el coeficiente de la variable " + str(j) + " de la funcion Z: "))
                    self.restrictions[i][j] = self.restrictions[i][j]*(-1)
                    self.objective.append(self.restrictions[i][j])
                elif j == self.num_colum - 1 and i == self.num_filas - 1:
                    self.restrictions[i][j] = 0
                    self.objective.append(self.restrictions[i][j])
                elif  self.numero_varZ < j < self.num_colum-1:
                    if i== j - self.numero_varZ-1:
                        self.restrictions[i][j] = 1
                    else:
                        self.restrictions[i][j] = 0
                        
        if(self.maxiRespuesta.lower() != "max"):
            self.maximize = False
                        
        #se llama al metodo simplex
        self.metodo_simplex(self.objective, self.restrictions, self.variables, self.maximize)
        
                        
                    

    def metodo_simplex(self, objective, restrictions, variables, maximize):
        self.maximize = maximize
        
        for k in range(len(objective)):
            self.objective[k] = objective[k]
        
        for k in range(len(variables)):
            self.variables[k] = variables[k]
        
        for k in range(len(restrictions)):
            self.restrictions[k] = restrictions[k]
            for j in range(len(restrictions[k])):
                self.restrictions[k][j] = restrictions[k][j]
                                
        while self.salidaaux == 1:
            self.imprimir_matriz(self.restrictions)
            self.encontrar_columpiv(self.restrictions, self.maximize)
            self.elemento_pivote = self.encontrar_elemento_pivote(self.restrictions)
            self.fila_entrante(self.matriz_2, self.restrictions)
            self.reorganizar_matriz(self.matriz_2)
            self.salidaaux = self.hay_negativos(self.restrictions)
            print(str(self.salidaaux))
            print(self.elemento_pivote)
            for i in range(self.num_filas):
                if i == self.fila_pivot:
                    try:
                        self.respuestas["X" + str(i + 1)] = self.respuestas.pop("S" + str(i + 1))
                    except:
                        self.respuestas["X" + str(i + 1)] = self.matriz_2[i][self.num_colum - 1]
                elif i == self.num_filas - 1:
                    self.respuestas["Z"] = self.matriz_2[i][self.num_colum - 1]

            for i in range(self.num_filas):
                for j in range(len(self.lista)):
                    if i == self.lista[j]:
                        self.respuestas["X" + str(i + 1)] = self.matriz_2[i][self.num_colum - 1]

            for i in range(self.num_filas):
                for j in range(self.num_colum):
                    self.restrictions[i][j]=self.matriz_2[i][j]
            for i in range(self.num_filas):
                for j in range(self.num_colum):
                    self.matriz_2[i][j]= None

        print("Respuestas: ")
        for key, value in self.respuestas.items():
            print(key + " = ", value)
        
        
    def __init__(self):
        self.print_simplex()
        #self.metodo_simplex(2,2,2,2)

simplex1 = simplex()
        
        
    
        
    
    
