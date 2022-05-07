from dataclasses import replace


class main:
    #Ejercicio 1
    print("Ingrese la ecuacion")
    equation = input()
    def parse_equation(equation):
        txt2 = equation.split()
        print(txt2)
        vector = []
        bandera = 1
        for x in range(len(txt2)):
            flag = txt2[x].split("x")
            var = str(flag[0])
            if(var!="+"):
                if(var == ''):
                    var = "1"
                if(var.find(".")!=-1):
                    vector.append("'x"+str(bandera)+"'"+" : "+var)
                    bandera = bandera+1
                else:
                    vector.append("'x"+str(bandera)+"'"+" : "+var+".0")
                    bandera = bandera+1
        print(vector)
        
    parse_equation(equation)



    
    #def parse_restriction(self)

    #def parse_problem(self)

    # def metodo_simplex(self)

    #def metodo_simplex_solver(self)
