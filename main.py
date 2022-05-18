from dataclasses import replace
from turtle import up
import numpy as np

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

        separateEquation = restriction[1:find]
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
        parseRestrictions = []
        contX = objective.count('x')
        contRestriction = restrictions.count(',')

        #Eliminar caracteres de las restricciones
        for xDelete in range(len(restrictions)):
            restrictions = restrictions.replace('[',"")
            restrictions = restrictions.replace(']',"")
            restrictions = restrictions.replace('"',"")

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

        if contTrue > 0 and contFalse == 0:
            cantVar = contX + len(parseRestrictions)
        else:
            cantVar = contX + len(parseRestrictions) + contFalse
       
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
                if maximize == "False" or maximize == "false":
                    filaZ.append(Mvar) 
                elif maximize == "True" or maximize == "true":
                    filaZ.append(-Mvar)

        matrix.append(filaZ)

        #Matriz de valores
        cont = len(parseEquation)
        for r in parseRestrictions:
            #hace una matriz de 0's
            row = np.zeros(len(filaVar) + 1, dtype=np.float64)
            
            for key, value in r[0].items():
                var = splitIndex(key)[1]
                row[var-1] = float(value)
            for slack in range(len(parseEquation), len(filaVar)):
                if slack == cont:
                    if r[2] == True:
                        row[slack] = 1.0
                    else:
                        row[slack] = -1.0
                        row[slack+1] = 1.0
                        slack += 1
                    break
            row[len(filaVar)] = r[1]
            matrix.append(row)
            cont += 1
        matrix.append(filaVar)

        #print(matrix)
        return matrix


class main:

    #Ejercicio 1
    #print("Ingrese la ecuacion:")
    #equation = input()

    #Llamado a la funcion
    #parse_equation(equation)
    
    #Ejercicio 2
    #print("Ingrese la restriccion:")
    #restriction = input()

    #Llamado a la funcion
    #parse_restriction(restriction)

    #Ejercicio 3
    print("Ingrese el objetivo:")
    objective = input()
    print("Ingrese la lista de restricciones:")
    restrictions = input()
    print("Se desea maximizar la funcion:")
    maximize = input()

    #Llamado a la funcion
    parse_problem(objective, restrictions, maximize)

    #Ejercicio 4
    #Llamado a la funcion
    #def metodo_simplex(objective, restrictions, variables, maximize)

    #Ejercicio 5
    #print("Ingrese el objetivo:")
    #objective = input()
    #print("Ingrese la lista de restricciones:")
    #restrictions = input()
    #print("Se desea maximizar la funcion:")
    #maximize = input()

    #Llamado a la funcion
    #def metodo_simplex_solver(objective, restrictions, maximize)


