#!/usr/bin/env python2
#-*- coding: UTF-8 -*-
#polynom.py

import matplotlib.pyplot as plt
import numpy as np
import pylab
import math


class Polynom:

    def __init__(self, a , b, c):
        assert a > 0
        self.a = a
        self.b = b
        self.c = c
        self.delta = self.get_delta()

    def get_delta(self):
        return self.b**2 - 4*self.a*self.c

    def eval(self, v):
      return self.a*v**2 + self.b*v + self.c

    def get_extremum(self):
        return [-self.b/(2*float(self.a)), -self.delta/(4*float(self.a))]

    def get_sym_axis(self):
        return -self.b/(2*float(self.a))

    def get_sol(self):
        sol = []
        if self.delta == 0:
          sol.append(-self.b/(2*self.a))
        elif self.delta > 0:
          sol.append((-self.b + math.sqrt(self.delta))/(2*float(self.a)))
          sol.append((-self.b - math.sqrt(self.delta))/(2*float(self.a)))
        sol.sort()
        return sol

    def plot(self, xwindow, ywindow, decoration=False):
        fig = plt.figure()
        title = "Graphe du polynome du second degre\n{}".format(str(self))
        fig.suptitle(title, fontsize=14, fontweight='bold')
        ax = pylab.gca()
        # center in (0,0) xaxis and yaxis
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data',0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data',0))
        # window
        pylab.xlim(xwindow[0], xwindow[1])
        pylab.ylim(ywindow[0], ywindow[1])
        # data
        x = np.linspace(xwindow[0], xwindow[1], 100)
        y = self.eval(x)
        if decoration:
            yy = np.linspace(ywindow[0], ywindow[1], 100)
            s = [self.get_sym_axis()]*len(yy)
            extremum = self.get_extremum()
        # plot
        ax.plot(x, y, 'r-')
        ax.text(xwindow[1]-0.5, 0.2, r'$x$', fontsize=15)
        ax.text(0.2, ywindow[1]-0.5, r'$y$', fontsize=15)
        if decoration:
            ax.plot(s, yy, 'k:')
            ax.plot(extremum[0], extremum[1], 'ok')
            px = r'$P \,:\, x \mapsto ax^2 + bx + c$'
            ax.text(xwindow[1]-7, ywindow[1]-2, px, fontsize=15)
            sol = self.get_sol()
            if len(sol) == 0:
                ax.text(xwindow[1]-7, ywindow[1]-3, r'$Aucune solution$', fontsize=15)
            elif len(sol) == 1:
                x_0 = r'$x_0 = {}$'.format(sol[0])
                ax.plot(sol[0], 0, 'ok')
                ax.text(xwindow[1]-7, ywindow[1]-3, x_0, fontsize=15)
            elif len(sol) == 2:
                x_1 = r'$x_1 = {}$'.format(sol[0])
                ax.plot(sol[0], 0, 'ok')
                x_2 = r'$x_2 = {}$'.format(sol[1])
                ax.plot(sol[1], 0, 'ok')
                ax.text(xwindow[1]-7, ywindow[1]-3, x_1, fontsize=15)
                ax.text(xwindow[1]-7, ywindow[1]-4, x_2,  fontsize=15)
        plt.show()

    def _op(self, x):
        s = ''
        if x < 0:
            s = '-'
        elif x > 0:
            s = '+'
        return s

    def __str__(self):
        a = '' if self.a in [-1, 1] else abs(self.a)
        b = '' if self.b in [-1, 1] else abs(self.b)
        c = abs(self.c)
        if self.b == 0 and self.c == 0:
          s = '{}X^2'.format(a)
        elif self.b == 0:
          op1 = self._op(self.c)
          s = '{}X^2 {} {}'.format(a, op1, c)
        else:
          op1 = self._op(self.b)
          op2 = self._op(self.c)
          s = '{}X^2 {} {}X {} {}'.format(a, op1, b, op2, c)
        return s

if __name__ == '__main__':
    p = Polynom(1, -1, -12)
    p.plot([-5,15],[-15,10], True)

