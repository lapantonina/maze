#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

# Create your views here.
import django.shortcuts
import math
import random
from django.http import HttpResponse, Http404
from django.views.generic.base import View
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template.defaulttags import register
import requests

def make_me_a_maze(request):
  return render_to_response('make_me_a_maze.html')


# количество клеток/ходов в высоту и ширину, задаются пользователем
w = 0
h = 0

# длина стороны квадратной комнаты и ширина стенки (длина=длине комнаты), также есть в стилях шаблона
room_width = 30
wall_width = 10
cell_width = room_width + wall_width

# тут может быть любой набор символов, но с такими лабиринт нагляден даже в качестве построчного вывода массива
space = ' '
full = '*'
line_hor = '_'
line_ver = '|'

maze = []
pure_path = [] #список всех ходов без учета выбирания из тупиков
keychain = [] #список всех ходов с учетом выбирания из тупиков (ходы, приводящие в тупики, убираются после выхода из тупика)

#проверка на тупик (отсутствие ходов из данной позиции)
def check_dead_end(maze, height, width, x, y):
  if (x == height-2 or maze[x+2][y] == space) and (y == width-2 or maze[x][y+2] == space) and (x == 1 or maze[x-2][y] == space) and (y == 1 or maze[x][y-2] == space):
    return 'yes'
  else:
    return 'no'


def maze(request):

  if 'h' in request.GET and 'w' in request.GET:
    h = int(request.GET['h'])
    w = int(request.GET['w'])
    if h > 0 and w > 0:

      
      # по два символа на клетку (три подряд клетки выглядят так: |_|_|_) плюс доп. клетка в высоту и ширину (от нее оставим только стенку)
      height = h * 2 + 1
      width = w * 2 + 1
      h_px = str(h * cell_width + wall_width)+'px'
      w_px = str(w * cell_width + wall_width)+'px'

      # строим непройденный дабиринт, есть стенки клетка состоит из заполнение + 3/6 стенок, + доп. стенки для замыкающих клеток
      maze = [[line_ver, full] * (w+1) for q in range(height)]
      walls = [[line_hor, line_hor] * (w+1) for q in range(height)]

      for q in range(0, height, 2):
        maze[q] = walls[q]

      for q in range(height):
        del maze[q][-1]
        maze[q][0] = maze[q][-1] = line_ver

      # задаем (любые нечетные) координаты начала построения. Из середины, т к так лабиринт будет сложнее (больше тупиковых ответвлений)
      x = 2 * int(h//2) +1
      y = 2 * int(w//2) +1
      o = []


      ##################### MAIN ############################
      while len(pure_path) < w*h-1:

        maze[x][y] = space # пройденная клетка отмечается как пустая

        if check_dead_end(maze, height, width, x, y) == 'no':
          key = random.randint(0, 3)
          if key == 0:
            if x < height-2 and maze[x+2][y] == full:
              maze[x+1][y] = space
              x = x+2
              keychain.append(key)
              pure_path.append(key)
          elif key == 1:
            if y < width-2 and maze[x][y+2] == full:
              maze[x][y+1] = space
              y = y+2
              keychain.append(key)
              pure_path.append(key)
          elif key == 2:
            if x > 1 and maze[x-2][y] == full:
              maze[x-1][y] = space
              x = x-2
              keychain.append(key)
              pure_path.append(key)
          elif key == 3:
            if y > 2 and maze[x][y-2] == full:
              maze[x][y-1] = space
              y = y-2
              keychain.append(key)
              pure_path.append(key)
          
        elif check_dead_end(maze, height, width, x, y) == 'yes':
          last_key = keychain[-1]
          if last_key == 0:
            x = x-2
          elif last_key == 1:
            y = y-2
          elif last_key == 2:
            x = x+2
          elif last_key == 3:
            y = y+2
          del keychain[-1]

      ##################### MAIN ############################


      safe_web_colors = ['FFFFCC', 'FFFF99', 'FFFF66', 'FFFF33', 'FFFF00', 'CCCC00', 'FFCC66', 'FFCC00', 'FFCC33', \
      'CC9900', 'CC9933', '996600', 'FF9900', 'FF9933', 'CC9966', 'CC6600', '996633', '663300', 'FFCC99', 'FF9966', \
      'FF6600', 'CC6633', '993300', '660000', 'FF6633', 'CC3300', 'FF3300', 'FF0000', 'CC0000', '990000', 'FFCCCC', \
      'FF9999', 'FF6666', 'FF3333', 'FF0033', 'CC0033', 'CC9999', 'CC6666', 'CC3333', '993333', '990033', '330000', \
      'FF6699', 'FF3366', 'FF0066', 'CC3366', '996666', '663333', 'FF99CC', 'FF3399', 'FF0099', 'CC0066', '993366', \
      '660033', 'FF66CC', 'FF00CC', 'FF33CC', 'CC6699', 'CC0099', '990066', 'FFCCFF', 'FF99FF', 'FF66FF', 'FF33FF', \
      'FF00FF', 'CC3399', 'CC99CC', 'CC66CC', 'CC00CC', 'CC33CC', '990099', '993399', 'CC66FF', 'CC33FF', 'CC00FF', \
      '9900CC', '996699', '660066', 'CC99FF', '9933CC', '9933FF', '9900FF', '660099', '663366', '9966CC', '9966FF', \
      '6600CC', '6633CC', '663399', '330033', 'CCCCFF', '9999FF', '6633FF', '6600FF', '330099', '330066', '9999CC', \
      '6666FF', '6666CC', '666699', '333399', '333366', '3333FF', '3300FF', '3300CC', '3333CC', '000099', '000066', \
      '6699FF', '3366FF', '0000FF', '0000CC', '0033CC', '000033', '0066FF', '0066CC', '3366CC', '0033FF', '003399', \
      '003366', '99CCFF', '3399FF', '0099FF', '6699CC', '336699', '006699', '66CCFF', '33CCFF', '00CCFF', '3399CC', \
      '0099CC', '003333', '99CCCC', '66CCCC', '339999', '669999', '006666', '336666', 'CCFFFF', '99FFFF', '66FFFF', \
      '33FFFF', '00FFFF', '00CCCC', '99FFCC', '66FFCC', '33FFCC', '00FFCC', '33CCCC', '009999', '66CC99', '33CC99', \
      '00CC99', '339966', '009966', '006633', '66FF99', '33FF99', '00FF99', '33CC66', '00CC66', '009933', '99FF99', \
      '66FF66', '33FF66', '00FF66', '339933', '006600', 'CCFFCC', '99CC99', '66CC66', '669966', '336633', '003300', \
      '33FF33', '00FF33', '00FF00', '00CC00', '33CC33', '00CC33', '66FF00', '66FF33', '33FF00', '33CC00', '339900', \
      '009900', 'CCFF99', '99FF66', '66CC00', '66CC33', '669933', '336600', '99FF00', '99FF33', '99CC66', '99CC00', \
      '99CC33', '669900', 'CCFF66', 'CCFF00', 'CCFF33', 'CCCC99', '666633', '333300', 'CCCC66', 'CCCC33', '999966', \
      '999933', '999900', '666600', 'FFFFFF', 'CCCCCC', '999999', '666666', '333333', '000000']

      background_color = safe_web_colors[random.randint(0, len(safe_web_colors))]

      # эта строка не в шаблоне, т к фигурные скобки конкурируют со скобками стиля
      o.append(str('  <div style="width:' + w_px + '; height:' + h_px + '; background:#' + background_color + '">'))


      for x in range(height):
        for y in range(width):
          if x == 1 and y == 0: #start_invisible_wall
            o.append('   <div id="wall_' + str(x//2+1) + '_' + str(y//2+1) + '", class="line_ver invsbl"></div>')
          elif maze[x][y] == line_ver:
            if x % 2 == 0:
              o.append('   <div class="corner"></div>')
            else:
              o.append('   <div id="wall_' + str(x//2+1) + '_' + str(y//2+1) + '", class="line_ver"></div>')
          elif maze[x][y] == line_hor:
            if x == 2*h and y == 2 * w - 1: #finish_invisible_wall
              o.append('   <div id="ceil_' + str(x//2+1) + '_' + str(y//2+1) + '", class="finish"></div>')
            elif y % 2 == 0:
              o.append('   <div class="corner"></div>')
            else:
              o.append('   <div id="ceil_' + str(x//2+1) + '_' + str(y//2+1) + '", class="line_hor"></div>')
          elif maze[x][y] == space or full:
            if x % 2 == 0:
              o.append('   <div class="space"></div>')
            elif y % 2 == 0:
              o.append('   <div class="high_space"></div>')
            else:
              o.append('   <div id="cell_' + str(x//2+1) + '_' + str(y//2+1) + '", class="runner invsbl"></div>')


      

      t = get_template('maze_templ.html')

      html = t.render(Context({'wdth': w_px, 'hght': h_px, 'height': h, 'width': w, 'runner': '\n'.join(o)}))

      del pure_path[:]
      
      return HttpResponse(html)