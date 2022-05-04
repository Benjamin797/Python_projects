import tkinter as tk

def fenetre():

    root = tk.Tk()
    root.title("Window - Test")
    root.geometry("600x600")
    MyLabel = tk.Label(root, text='Enter your first name : ')#Creation d'un label
    MyLabel.pack()#Place label dans root de maniere aleatoire

    Textbox = tk.Entry(root, width=30)#Champs de saisie
    Textbox.pack()
    def hello():
        hello_label = tk.Label(root, text="Hello " + Textbox.get())
        hello_label.pack()



    Button = tk.Button(root, text='Enter', command=hello)#Button avec commande
    Button.pack()
    root.mainloop()



fenetre()










