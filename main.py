#Laboratorio1
#Samantha Romero
#Paula Monge
from dataclasses import replace
from turtle import up
import numpy as np
#import simplex as simplex

def parse_equation(equation):
        #Quita las "" que traiga
        for x in range(len(equation)):
            equation = equation.replace('"',"")

        equationSplit = equation.split()
        vector = {}
        flag = 1
        for x in range(len(equationSplit)):
            flag2 = equationSplit[x].split("x")
            var = str(flag2[0])
            if(var!="+"):
                if(var == ''):
                    var = "1"
                if(var.find(".")!=-1):
                    vector["x"+str(flag)] = var
                    flag = flag+1
                else:
                    vector["x"+str(flag)] = var+".0"
                    flag = flag+1

        #print(vector)
        return vector

def parse_restriction(restriction):
        upperBoundFlag = bool(0)
        find = ''
        restrictionSplit = restriction.split()

        for value in restrictionSplit:
            if value == '<=':
                upperBoundFlag = bool(1)
                find = restriction.find(value)
            elif value == '>=':
                upperBoundFlag = bool(0)
                find = restriction.find(value)

        separateEquation = restriction[0:find]
        restrictionValue = restriction[find+3:len(restriction)]
        f = float(restrictionValue)

        #print(parse_equation(separateEquation), float(restrictionValue), upperBoundFlag)
        return parse_equation(separateEquation), f, upperBoundFlag

def splitIndex(value):
    index = value.split('x')
    coeficient = 1
    subindex = index[1]

    if index[0] != '':
        coeficient = index[0]
        if index[0] == '-':
            coeficient = -1
    return float(coeficient), int(subindex)

def parse_problem(objective, restrictions, maximize):
        Mvar = 100000.0
        contTrue = 0
        contFalse = 0
        matrix = []
        filaZ = []
        filaVar = []
        filaMat = []
        parseRestrictions = []
        contX = objective.count('x')

        restrictions = str(restrictions)
        contRestriction = restrictions.count(',')

        #Eliminar caracteres de las restricciones
        for xDelete in range(len(restrictions)):
            restrictions = restrictions.replace('[',"")
            restrictions = restrictions.replace(']',"")
            restrictions = restrictions.replace('"',"")
            restrictions = restrictions.replace("'","")

        #Se envia a evaluar la funcion objetivo
        parseEquation = parse_equation(objective)

        #Se envian a evaluar las restricciones
        restrictionsSplit = restrictions.split(",")
        for xEvaluate in range(len(restrictionsSplit)):
            xEvaluate = parse_restriction(restrictionsSplit[xEvaluate])
            parseRestrictions.append(xEvaluate)

        #Agregar variables de slack
        for xEvaluate in range(len(parseRestrictions)):
            if  parseRestrictions[xEvaluate][2] == True:
                #Holgura
                contTrue = len(parseRestrictions)
            elif parseRestrictions[xEvaluate][2] == False:
                #Superavit
                contFalse+=1
       
        #Matriz
        #Fila z
        for key in parseEquation:
            filaZ.append(parseEquation[key])
            #agrega las variables
            filaVar.append(key)
        for x in range(contRestriction+1):
            filaVar.append('s' + str(x+1))
        for y in range(contFalse):
            filaVar.append('a' + str(y+1))

        if contTrue > 0 and contFalse == 0:
            for x in range(contTrue):
                filaZ.append(0)  
        elif contTrue > 0 and contFalse > 0:
            for x in range(contTrue):
                filaZ.append(0) 
            for y in range(contFalse):
                if maximize == False:
                    filaZ.append(Mvar) 
                elif maximize == True:
                    filaZ.append(-Mvar)
        elif contTrue == 0 and contFalse > 0:
            for x in range(contFalse):
                filaZ.append(0) 
            for y in range(contFalse):
                if maximize == False:
                    filaZ.append(Mvar) 
                elif maximize == True:
                    filaZ.append(-Mvar)


        matrix.append(filaZ)

        #Matriz de valores
        cont = len(parseEquation)
        contA = len(filaVar) - len(parseEquation) - (contRestriction+1)

        for r in parseRestrictions:
            #hace una matriz de 0's
            row = np.zeros(len(filaVar) + 1, dtype=np.float64)
            
            #Pone los valores de x
            for key, value in r[0].items():
                var = splitIndex(key)[1]
                row[var-1] = float(value)
            #Pone variables de slack
            for slack in range(len(parseEquation), (len(filaVar)-contA)):
                if slack == cont:
                    if r[2] == True:
                        row[slack] = 1.0
                    else:
                        row[slack] = -1.0
                        slack += 1
            if r[2] == False and contA > 1:
                row[slack+1] = 1.0
            elif r[2] == False:
                row[slack] = 1.0

            row[len(filaVar)] = r[1]
            filaMat.append(row)
            
            cont += 1

        matrix.append(filaMat)
        matrix.append(filaVar)
        matrix.append(maximize)

        #print(matrix)
        return matrix

def simplex_solver(objective, restrictions, maximize):
    matrix = []
    objectiveP = []
    restrictionsP = []
    variables = []

    matrix = parse_problem(objective, restrictions, maximize)

    #Se divide el retorno de parse_problem
    objectiveP = matrix[0]
    restrictionsP = matrix[1]
    variables = matrix[2]
    maximizeP = matrix[3]

    print(matrix)

class main:
    #Ejercicio 5
    #Llamado a la funcion
    simplex_solver("0.65x1 + 0.45x2", ["2x1 + 3x2 <= 400", "3x1 + 1.5x2 <= 300", "x1 <= 90"], True)
    simplex_solver("30x1 + 100x2", ["x1 + x2 <= 7", "4x1 + 10x2 <= 40", "10x1 >= 30"], True)
    simplex_solver("3x1 + 8x2", ["5x1 + 4x2 >= 3.5" , "x1 + 2x2 >= 2.5"], False)
    simplex_solver("x1 + 4x2", ["-10x1 + 20x2 <= 22" , "5x1 + 10x2 <= 49", "x1 <= 5"], True)


