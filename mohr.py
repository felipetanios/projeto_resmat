import Tkinter
import tkMessageBox
import math
import sys
import os
import subprocess

class Informacoes:
    def __init__(self):
        self.tensao_x = 0
        self.tensao_y = 0
        self.tensao_cisalhamento = 0
        self.raio = 0
        self.tensao_principal_med = 0
        self.tensao_principal_max = 0
        self.tensao_principal_min = 0
        self.tensao_cisalhamento_max = 0
        self.teta_p = 0
        self.teta_s = 0

    def run(self, tensao_x, tensao_y, tensao_cisalhamento, teta=0):
        sin = math.sin
        cos = math.cos
        rad = math.radians
        self.tensao_x = tensao_x
        self.tensao_y = tensao_y
        self.tensao_cisalhamento = tensao_cisalhamento
        self.teta = teta
        self.raio = 0
        # Tensao media (tau_med)
        self.tensao_principal_med = (self.tensao_x + self.tensao_y)/2.

        # Tensao media de Cisalhamento (tau_med)
        self.tensao_media_cisalhamento = (self.tensao_x - self.tensao_y)/2.

        # Raio do Circulo (R)
        self.raio = ((self.tensao_media_cisalhamento)**2  + (self.tensao_cisalhamento)**2)**0.5

        # Equilibrio das forcas nas direcao do Teta_sigma_x (sigma_x')
        self.tensao_x_linha = (self.tensao_principal_med + self.tensao_media_cisalhamento*cos(rad(2.*teta)) +
                    self.tensao_cisalhamento*sin(rad(2*teta)))

        # Equilibrio das forcas na direcao Teta_sigma_y (sigma_y')
        self.tensao_y_linha = (self.tensao_principal_med - self.tensao_media_cisalhamento*cos(2.*rad(teta)) -
                    self.tensao_cisalhamento*sin(2.*rad(teta)))

        # Equilibrio das forcas na direcao de Teta_tau (tau')
        self.tensao_cisalhamento_linha = -self.tensao_media_cisalhamento*sin(2.*rad(teta))+self.tensao_cisalhamento*cos(2.*rad(teta))

        # Tensao principal maxima (sigma_max)
        self.tensao_principal_max = self.tensao_principal_med + (((self.tensao_media_cisalhamento)**2) + self.tensao_cisalhamento**2)**0.5

        # Tensao principal minima (sigma_min)
        self.tensao_principal_min = self.tensao_principal_med - (((self.tensao_media_cisalhamento)**2) + self.tensao_cisalhamento**2)**0.5

        # Tensao de cisalhamento maxima (tau_max)
        self.tensao_cisalhamento_max = ((self.tensao_media_cisalhamento**2) + self.tensao_cisalhamento**2)**0.5

        # Angulo entre os eixos sem rotacao ate o sigma minimo
        self.teta_p = ((math.degrees(math.atan((2.*self.tensao_cisalhamento) /
                                              (self.tensao_x-self.tensao_y))))/2.)
        # Angulo entre o eixo sem rotacao ate sigma_x'
        self.teta_s = ((math.degrees(math.atan(-(self.tensao_x-self.tensao_y) /
                                              (2.*self.tensao_cisalhamento))))/2.)

    def conversion(self, radius):
        self.save_plot = (self.tensao_principal_med*radius)/self.raio
        self.sx_plot = (self.tensao_x*radius)/self.raio
        self.sy_plot = (self.tensao_y*radius)/self.raio
        self.txy_plot = (self.tensao_cisalhamento*radius)/self.raio
        self.nsx_plot = (self.tensao_x_linha*radius)/self.raio
        self.nsy_plot = (self.tensao_y_linha*radius)/self.raio
        self.ntxy_plot = (self.tensao_cisalhamento_linha*radius)/self.raio


class Gui:
    def __init__(self, app):
        self.r_plot = 0
        app.title("Circulo de Mohr")
        app.geometry('900x500')
        self.calc = Informacoes()
        self.circle_diameter = 400
        self.xo_circle = 120
        self.yo_circle = 50
        self.x1_circle = self.xo_circle + self.circle_diameter
        self.y1_circle = self.yo_circle + self.circle_diameter

        self.frame = Tkinter.Frame(app)
        self.frame.pack(side='left', pady=10)
        self.frame1 = Tkinter.Frame(self.frame)
        self.frame1.pack()
        self.frame2 = Tkinter.Frame(self.frame)
        self.frame2.pack()
        self.frame3 = Tkinter.Frame(self.frame)
        self.frame3.pack()
        self.frame4 = Tkinter.Frame(self.frame)
        self.frame4.pack()
        self.frame5 = Tkinter.Frame(self.frame)
        self.frame5.pack()

        top_draw_frame = Tkinter.Frame(app)
        top_draw_frame.pack(expand=Tkinter.NO, fill=Tkinter.BOTH, side='left')

        label_text = Tkinter.StringVar()
        label_text.set(u"\u03C3x")
        label1 = Tkinter.Label(self.frame1, textvariable=label_text, height=2)
        label1.pack(side='left', padx=7)
        cust_name = Tkinter.StringVar(None)
        self.entry1 = Tkinter.Entry(self.frame1,
                                    textvariable=cust_name, width=15)
        self.entry1.pack(side='left')
        self.entry1.focus_force()

        label_text2 = Tkinter.StringVar()
        label_text2.set(u"\u03C3y \n")
        label2 = Tkinter.Label(self.frame2, textvariable=label_text2, height=2)
        label2.pack(side='left', padx=7)
        cust_name2 = Tkinter.StringVar(None)
        self.entry2 = Tkinter.Entry(self.frame2,
                                    textvariable=cust_name2, width=15)
        self.entry2.pack(side='left')

        label_text3 = Tkinter.StringVar()
        label_text3.set(u"\u03C4xy")
        label3 = Tkinter.Label(self.frame3, textvariable=label_text3, height=2)
        label3.pack(side='left', padx=5)
        cust_name3 = Tkinter.StringVar(None)
        self.entry3 = Tkinter.Entry(self.frame3,
                                    textvariable=cust_name3, width=15)
        self.entry3.pack(side='left')

        label_text4 = Tkinter.StringVar()
        label_text4.set(u"\u03B8")
        label4 = Tkinter.Label(self.frame4, textvariable=label_text4, height=2)
        label4.pack(side='left', padx=12)
        cust_name4 = Tkinter.StringVar(None)
        self.entry4 = Tkinter.Entry(self.frame4,
                                    textvariable=cust_name4, width=15)
        self.entry4.pack(side='left')
        self.var = Tkinter.IntVar()
        R1 = Tkinter.Radiobutton(self.frame5, text="Antihorario",
                                 variable=self.var, value=1)
        R1.pack(anchor='w')
        R2 = Tkinter.Radiobutton(self.frame5, text="Horario",
                                 variable=self.var, value=2)
        R2.pack(anchor='w')
        R1.select()

        button1 = Tkinter.Button(self.frame, text="OK", width=10,
                                 command=self.execute)
        button1.pack(padx=10, pady=10)

        button2 = Tkinter.Button(self.frame, text="Gerar Resultados", width=10,
                                 command=self.show_log)
        button2.pack(padx=10)

        menu_bar = Tkinter.Menu(app)
        file_menu = Tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_separator()
        about_menu = Tkinter.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="Sobre o aplitcativo", command=self.new_window)
        menu_bar.add_cascade(label="Sobre", menu=about_menu)
        app.config(menu=menu_bar)

        self.r_plot = self.circle_diameter/2
        rx = self.xo_circle + self.r_plot
        ry = self.yo_circle + self.r_plot
        # left mohr circle
        self.canvas0 = Tkinter.Canvas(top_draw_frame, width=1000,
                                      height=500, bg='white')
        self.canvas0.pack(side='left')
        self.canvas0.create_oval(self.xo_circle, self.yo_circle, self.x1_circle,
                                 self.y1_circle, width=2,
                                 fill='#ffffff', tag='circle')

        self.canvas0.create_line(0, int(ry), 1000, int(ry),
                                 width=1, fill='black', tag='origin_line')
        self.canvas0.create_line(int(rx), 0, int(rx),
                                 1000, width=1, fill='black', tag='origin_line')
        diameter = 3
        self.rx2 = rx + diameter
        self.ry2 = ry + diameter
        self.canvas0.create_oval(rx-2, ry-2, self.rx2, self.ry2, width=2,
                                 fill='black', tag='center-dot')
        # convension canvas
        self.canvas1 = Tkinter.Canvas(self.frame, width=200,
                                      height=400, bg='#f0f0f0')
        self.canvas1.pack(expand=Tkinter.YES, fill='both')
        self.canvas1.create_rectangle(60, 100, 140, 180,
                                      fill='#b4b4ff', width=1)
        # tensao_y arrow
        self.canvas1.create_line(100, 60, 100,
                                 100, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(100, 60, 95,
                                 70, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(100, 60, 105,
                                 70, width=1, fill='black', tag='origin_line')
        self.canvas1.create_text(100, 50, text=u"\u03C3y")
        # tensao_x arrow
        self.canvas1.create_line(60, 140, 20,
                                 140, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(20, 140, 30,
                                 145, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(20, 140, 30,
                                 135, width=1, fill='black', tag='origin_line')
        self.canvas1.create_text(30, 125, text=u"\u03C3x")
        # tensao_cisalhamento up
        self.canvas1.create_line(150, 100, 150,
                                 140, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(150, 100, 155,
                                 110, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(150, 100, 145,
                                 110, width=1, fill='black', tag='origin_line')
        self.canvas1.create_text(150, 80, text=u"\u03C4xy")
        # tensao_cisalhamento right
        self.canvas1.create_line(100, 90, 140,
                                 90, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(140, 90, 130,
                                 95, width=1, fill='black', tag='origin_line')
        self.canvas1.create_line(140, 90, 130,
                                 85, width=1, fill='black', tag='origin_line')

    def execute(self):
        try:
            string_input1 = self.entry1.get()
            string_input2 = self.entry2.get()
            string_input3 = self.entry3.get()
            string_input4 = self.entry4.get()
            tensao_x = float(string_input1)
            tensao_y = float(string_input2)
            tensao_cisalhamento = float(string_input3)
            teta = float(string_input4)
            if self.var.get() == 2:
                teta = -teta
            self.calc.run(tensao_x, tensao_y, tensao_cisalhamento, teta)
            self.build_canvas()
        except ValueError:
            self.wrong_value()

    def wrong_value(self):
        tkMessageBox.showinfo("Status",
                              "Insira apenas numeros")

    def new_window(self):
        top = Tkinter.Toplevel()
        top.title("Sobre")
        top.geometry('380x200')
        label_text = Tkinter.StringVar()
        label_text.set("Idealizado para materia de Resistencia dos Materiais por:\nLauro Cruz e Souza\nFelipe Tanios\nHenrique Noronha Facioli\nMateus Coelho\n Kairo Vinicius\n\n\n Design inspiriado em projeto de Estevao Fon ")
        label1 = Tkinter.Label(top, textvariable=label_text, height=10)
        label1.pack(side='top', padx=10, pady=15)
        top.mainloop()

    def x_not_created(self):
        top = Tkinter.Toplevel()
        top.title("Info")
        top.geometry('380x100')
        label_text = Tkinter.StringVar()
        label_text.set("Nao existe log ainda")
        label1 = Tkinter.Label(top, textvariable=label_text, height=2)
        label1.pack(side='top', padx=10, pady=15)
        top.mainloop()

    def build_canvas(self):
        self.canvas0.delete('line1')
        self.canvas0.delete('line2')
        self.canvas0.delete('origin_line')
        self.canvas0.delete('center-dot')
        self.calc.conversion(self.r_plot)
        rx = self.xo_circle + self.r_plot
        ry = self.yo_circle + self.r_plot
        yo = ry
        xo = rx - self.calc.save_plot
        tensao_x = xo + self.calc.sx_plot
        tensao_y = xo + self.calc.sy_plot
        tensao_x_linha = xo + self.calc.nsx_plot
        tensao_y_linha = xo + self.calc.nsy_plot
        tensao_cisalhamento = yo + self.calc.txy_plot
        txym = yo - self.calc.txy_plot
        tensao_cisalhamento_linha = yo + self.calc.ntxy_plot
        ntxym = yo - self.calc.ntxy_plot
        self.canvas0.create_line(int(rx), int(ry), int(tensao_x_linha),
                                 int(tensao_cisalhamento_linha), width=3, fill='red', tag='line2')
        self.canvas0.create_line(int(rx), int(ry), int(tensao_y_linha),
                                 int(ntxym), width=3, fill='red', tag='line2')
        self.canvas0.create_line(int(rx), int(ry), int(tensao_x),
                                 int(tensao_cisalhamento), width=3, fill='blue', tag='line1')
        self.canvas0.create_line(int(rx), int(ry), int(tensao_y),
                                 int(txym), width=3, fill='blue', tag='line1')
        self.canvas0.create_line(0, int(yo), 1000, int(yo),
                                 width=1, fill='black', tag='origin_line')
        self.canvas0.create_line(xo, 0, xo,
                                 1000, width=1, fill='black', tag='origin_line')
        self.canvas0.create_oval(rx-2, ry-2, self.rx2, self.ry2, width=2,
                                 fill='black', tag='center-dot')
        try:
            with open("resultados.html", 'w') as data:
                text = []
                text.append('<!DOCTYPE html><html><head><title> Resultados numericos </title>')
                text.append('<body><center><h1>Informacoes Circulo de Mohr</h1><b><h2>Resistencia de Materiais<br>EM423</h2>')
                text.append('</p><hr><p>Tensao x\':<br>%.2f' %self.calc.tensao_x_linha)
                text.append('</p><hr><p>Tensao y\':<br>%.2f' %self.calc.tensao_y_linha)
                text.append('</p><hr><p>Tensao xy\'<br>%.2f' %self.calc.tensao_cisalhamento_linha)
                text.append('</p><hr><p>Angulo &#952 p (Tensao principal maxima):<br>%.2f' %self.calc.teta_p)
                text.append('</p><hr><p>Angulo &#952 s:<br>%.2f' %self.calc.teta_s)
                text.append('</p><hr><p>Tensao principal maxima:<br>%.2f' %self.calc.tensao_principal_max)
                text.append('</p><hr><p>Tensao principal minimo:<br>%.2f' %self.calc.tensao_principal_min)
                text.append('</p><hr><p>Tensao de cisalhamento maxima:<br>%.2f' %self.calc.tensao_cisalhamento_max)
                text.append('</p><hr><p>Tensao principal media:<br>%.2f' %self.calc.tensao_principal_med)
                text.append('</p><hr><p>Raio do circulo:<br>%.2f' %self.calc.raio)
                text.append('</p><hr></center></body></html>')
                data.writelines(text)
                data.close()
        except:
            print "File erro"
            raise

    def show_log(self):
        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", "resultados.html"])
        else:
            os.startfile("resultados.html")

app = Tkinter.Tk()
Gui(app)
app.mainloop()
