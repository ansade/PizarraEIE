########################################################################
# 			Software Pizarra Interactiva EIE
#
# Realizado por Andres Sanchez Delgado B05832
# I-2016
########################################################################





########################################################################
#					IMPORTS 
########################################################################
from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.graphics import Color, Line
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
import os
from kivy.graphics import (
    Canvas, Translate, Fbo, ClearColor, ClearBuffers, Scale)

########################################################################
##							CLASE CANVAS WIDGET
# Crea las funciones que posteriormente se usaran en el APP pizarra
########################################################################

class CanvasWidget(Widget):
    line_width = 2 

    def on_touch_down(self, touch):
        if Widget.on_touch_down(self, touch):
            return

        with self.canvas:
            touch.ud['current_line'] = Line(
                points=(touch.x, touch.y),
                width=self.line_width)

    def on_touch_move(self, touch):
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points += (touch.x, touch.y)


	# Define el color 
    def set_color(self, new_color):
        self.last_color = new_color
        self.canvas.add(Color(*new_color))


	#Define el grosor
    def set_line_width(self, line_width='Medio'):
        self.line_width = {
            'Fino': 2, 'Medio': 4, 'Grueso': 8
        }[line_width]
	
	#Borra el contenido de la pizarra 
    def clear_canvas(self):
        saved = self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)
        self.set_color(self.last_color)

    
    def export_to_png(self, filename, *args):
      

        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=self.size, with_stencilbuffer=True)

        with fbo:
            ClearColor(1, 1, 1, 1)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()
        fbo.texture.save(filename, flipped=False)
        fbo.remove(self.canvas)

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

        return True
    
	
    def guardar(self):
        global itername # variable que incrementa el numero de 
        saved = self.children[:]
         
        self.clear_widgets()
    
        self.export_to_png('IMG'+str(itername)+'.png')
        
        
        itername = itername + 1
        print itername
        for widget in saved:
            self.add_widget(widget)
        self.set_color(self.last_color)
    
    def export(self):
		c = canvas.Canvas('./PDFs/EJEMPLO.pdf')
		c.drawImage('./prueba.png', 0, 0, 22*cm, 22*cm) #HAcer un for que itere sobre todas las imagenes creadas
		c.showPage()
		c.save() # Desplegar mensaje de creacion satisfactoria
    
    	
		
	 
       
        
	
        
########################################################################
##							CLASE RADIO BUTTON
# Crea la funcion de boton presionado 
########################################################################
        
        
class RadioButton(ToggleButton):
    def _do_press(self):
        if self.state == 'normal':
            ToggleButtonBehavior._do_press(self)        

########################################################################
##							CLASE PIZARRAAPP
# Crea la aplicacion instanciando Canvas_widget 
########################################################################            


class PizarraEIEApp(App):
    def build(self):
        EventLoop.ensure_window()

        self.canvas_widget = CanvasWidget() # Crea el widget 
        
        self.canvas_widget.set_color(  # Pone color al trazo 
        get_color_from_hex('#190707'))
        
        
       # c = canvas.Canvas('EJEMPLO.pdf')
	
	
	#c.showPage()
	#c.save()	
        #a=Button(text='GUARDAR')
        #self.canvas_widget.add_widget(a)
        #self.canvas_widget.export_to_png('a.png')
        #get_color_from_hex('#000000'))
           
        return self.canvas_widget

########################################################################
##							MAIN
# Programa principal que llama PizarraAPP para correrla 
########################################################################

if __name__ == '__main__':
    
    global itername
    itername = 1
    
    Config.set('graphics', 'width', '1300')
    Config.set('graphics', 'height', '720')  # 16:9
   
    from kivy.core.window import Window
    Window.clearcolor = get_color_from_hex('#FFFFFF') # Pone el fondo de la ventana en blanco 
   
    
    PizarraEIEApp().run()
