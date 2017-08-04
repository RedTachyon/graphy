#!/bin/python3

from graph import Graph
from tkinter import *
from math import pi, sin, cos

class GrApp:
    def __init__(self, root, graph, width=400, height=400, color='#DDDDDD'):
        self.root = root
        self.width = self.W = width
        self.height = self.H = height
        self.canvas = self._add_canvas(color)
        self.graph = graph
        quit = self._add_quit_button()
        
        self.draw_nodes(self.canvas)
        self.draw_edges(self.canvas)
        
        
    def _add_canvas(self, color):
        canvas = Canvas(self.root,
                        width=self.width,
                        height=self.height,
                        bg=color)
        
        canvas.pack()
        return canvas
    
    def _add_quit_button(self):
        button = Button(self.root,
                        text='QUIT',
                        fg='red',
                        command=self.root.destroy)
        button.pack()
        return button
        
    def _draw_circle(self, canvas, x, y, r, color='black'):
        canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)
        
    def draw_nodes(self, canvas):
        N = self.graph.N
        R = (7/16) * min(self.H, self.W)
        r = pi*R/(4*N)        
        self.coords = {}
        for i in range(N):
            x, y = self.W/2 + R*sin(2*pi*i/N), self.H/2 - R*cos(2*pi*i/N)
            self.coords[i] = (x,y)
            self._draw_circle(canvas, x, y, r)
            
    def draw_edges(self, canvas):
        edges = self.graph.edges
        
        for (i, j) in edges:
            x1, y1 = self.coords[i]
            x2, y2 = self.coords[j]
            canvas.create_line(x1, y1, x2, y2, width=3)
            
def show(graph, width=800, height=800):
    root = Tk()
    app = GrApp(root, graph=graph, width=width, height=height)
    root.mainloop()
    
    
if __name__ == '__main__':
    graph = Graph(20, 6)
    graph.WS_model(0.5)

    root = Tk()

    app = GrApp(root, graph=graph, width=800, height=800)

    root.mainloop()
