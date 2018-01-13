try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from math import log10
from WordFilter import WordFilter
from EvaluateText import evaluateWord
from EvaluateText import guessEmotion


class Evaluator():
    def __init__(self):
        main = tk.Tk()
        tk.Label(main, text="Input text:", font=(None, 15)).grid(row=0, sticky="nsew", pady=5)
        tk.Label(main, text="Predicted:", font=(None, 15)).grid(row=1)

        self.v = tk.StringVar()
        self.inputStr = tk.Entry(main, font=(None, 15), width=50)
        self.output = tk.Label(main, textvariable=self.v, font=(None, 15))

        self.inputStr.grid(row=0, column=1, sticky="nsew", pady=10, padx=(0, 10))
        self.output.grid(row=1, column=1, sticky="W")

        tk.Button(main,
                  text='Clear',
                  command=self.clearButton,
                  font=(None, 10)).grid(row=2, column=0, stick="nsew", pady=(8, 2), padx=10)
        tk.Button(main,
                  text='Quit',
                  command=main.destroy,
                  font=(None, 10)).grid(row=3, column=0, sticky="nsew", pady=(2, 8), padx=10)
        tk.Button(main,
                  text='Predict',
                  command=self.predButton,
                  font=(None, 15)).grid(row=2, column=1, rowspan=2, sticky="nsew", pady=9, padx=20)

        main.title("Emotion Recognition: GUI")
        main.grid_rowconfigure(0, weight=1, minsize=60)
        main.grid_columnconfigure(0, weight=2, minsize=150)
        main.grid_columnconfigure(1, weight=2, minsize=400)
        main.grid_rowconfigure(1, weight=1, minsize=30)
        main.grid_rowconfigure(2, weight=1, minsize=40)
        main.grid_rowconfigure(3, weight=1, minsize=40)

        tk.mainloop()

    def predButton(self):
        with open("./data/Priors.csv", "r") as priorFile:
            priors = priorFile.readline().strip().split(',')[1:]
            priors = [log10(float(x)) for x in priors]
        predValues = []
        unfound = []

        wf = WordFilter()
        words = self.inputStr.get()
        print "Input:", words
        words = wf.filterWords(words)

        print "Tokens:", words
        for word in words:
            try:
                values = evaluateWord(word)
            except IOError:
                print "WordMap not found. Please train system first.\n"
                raise
            if values is not None:
                predValues.append(values)
            else:
                unfound.append(word)

        predValues = map(sum, zip(*predValues))
        predProb = map(sum, zip(priors, predValues))
        predEmotion = guessEmotion(predProb)
        self.v.set(predEmotion)
        print "Unfound:", unfound
        print "Prob:", ','.join([('%.2f ') % x for x in predProb])
        print

    def clearButton(self):
        self.v.set("")
        self.inputStr.delete(0, 'end')
