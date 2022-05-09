from dataclasses import replace
from turtle import up

def parse_equation(equation):
        equationSplit = equation.split()
        #print(equationSplit)
        vector = []
        flag = 1
        for x in range(len(equationSplit)):
            flag2 = equationSplit[x].split("x")
            var = str(flag2[0])
            if(var!="+"):
                if(var == ''):
                    var = "1"
                if(var.find(".")!=-1):
                    vector.append("'x"+str(flag)+"'"+" : "+var)
                    flag = flag+1
                else:
                    vector.append("'x"+str(flag)+"'"+" : "+var+".0")
                    flag = flag+1
        print(vector)
        return vector

def parse_restriction(restriction):
        upperBoundFlag = bool(0)
        find = ''
        dict = {}
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

        dict[0] = parse_equation(separateEquation) 
        dict[1] = float(restrictionValue)
        dict[2] = upperBoundFlag

        print (dict)

        return dict

class main:
    #Ejercicio 1
    print("Ingrese la ecuacion:")
    equation = input()

    #Llamado a la funcion
    parse_equation(equation)
    
    #Ejercicio 2
    print("Ingrese la restriccion:")
    restriction = input()

    #Llamado a la funcion
    parse_restriction(restriction)

    #Ejercicio 3
    #def parse_problem(objective, restrictions, maximize):

    #def metodo_simplex(self)

    #def metodo_simplex_solver(self)

