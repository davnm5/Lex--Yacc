from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Frame, Label, Entry
from lex import validar
from io import StringIO
import io
import sys
import re
r = {}
aux="import numpy as np\n"
class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        problema1 = "Crear un arreglo de numpy basado en una lista"
        problema2= "Comparar si el primer elemento de una lista es mayor que el segundo\n elemento(imprimir el elemento mayor)"
        problema3 = "Genere un arreglo de 9 elementos con números pares mayores a 10"
        problema4 = "Dado el arreglo de numpy del ejercicio anterior utilice una función \nde numpy para hacer posible la multiplicación con su matriz identidad"
        problema5 = "Dado el arreglo de numpy con las notas de algunos alumnos de matemáticas\n, determine el promedio de las notas"
        problema6 = "Dados dos arreglos de estudiantes y sus notas, concatene el arreglo e imprima las\nnotas y el nombre del alumno"
        problema7 = "Dada la matriz de notas y estudiantes obtenga el promedio por estudiante y guarde \nlos promedios en un arreglo"
        problema8 = "Dado el arreglo anterior determine el mejor promedio e indique si este promedio\nsupera la nota de 9.5"
        problema9 = "Dado el arreglo de Strings con los nombre de las materias de un curso concatenarlo\ncon otro arreglo de notas para que forme una matriz de 2x10, guarde el resultado en una variable de nombre ClaseA."
        problema10 ="Dado la matriz del ejercicio anterior y la matriz Clase B que representa las notas de\nel paralelo b. Compare los resultados de las 3 materias principales : Lenguaje,Matemáticas y Ciencias, si el promedio de la clase A supera al de la clase B, guarde\nTrue en un arreglo de numpy, de lo contrario guarde False, finalmente indique en cuántas de las 3 materias el paralelo A es mejor que el B"
        listProblemas = [problema2,problema3,problema4,problema5,problema6,problema7,problema8, problema9,problema10]
        global contProblemas
        contProblemas = 1
        self.parent.title("Numpy If-else problems")
        self.pack(fill=BOTH, expand=True)
        global value
        value = 0
        global expr
        expr = StringVar()
        global res
        res = StringVar()
        randomIterator = iter(listProblemas)

        def cambio(event):

            label.configure(text=next(randomIterator))
            label.update()

        def validate():
            count=0
            if expr.get() == '':
                str = entry1.get("1.0","end-1c")
                lista =str.split("\n")
                lista_code=str.split("\n")
                for x in lista:
                    y=re.sub("\t","",x)
                    lista[count]=y
                    count=count+1
    
                l_exec=[aux]
                for i in lista_code:
                    validar(i)
                    l_exec.append(i+'\n')
                    
                ''''a=''.join(l_exec)
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()
                exec(a)
                sys.stdout = old_stdout
                result.configure(text=redirected_output.getvalue())
                result.update()'''
                    




            else:
                print(entry1.get("1.0",END))
                #result = validate(expr.get())
                #file = open('res', 'r')
                #last_line = file.read().splitlines()[-1]
                #res.set(last_line)



        frame0 = Frame(self)
        frame0.pack(fill=X)
        label = Label(frame0, text=problema1, justify=CENTER)
        label.pack(side=TOP,padx=50, pady=20)
        frame1 = Frame(self)
        frame1.pack(fill=X)
        btn = Button(frame0,text="Siguiente problema")
        btn.bind("<Button-1>", cambio)
        btn.pack(pady=10)




        lbl1 = Label(frame1, text="Your code :", width=18)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        entry1 = Text(frame1,width=10, height=20)
        entry1.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        btnplus = Button(frame3, text="Run", width=8, command=validate)
        btnplus.pack(side=LEFT, anchor=N, padx=5, pady=5)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        lbl3 = Label(frame4, text="Result :", width=10)
        lbl3.pack(side=LEFT, padx=5, pady=5)

        result = Label(frame4,text=r)
        result.pack(fill=X, padx=5, expand=True)

    def errorMsg(self,msg):
        if msg == 'error':
            tkinter.messagebox.showerror('Error!', 'Enter your expression')



def main():
    
    root = Tk()
    root.geometry("800x600")
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
