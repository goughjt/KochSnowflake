from Tkinter import * 
from PIL import Image, ImageTk 
import cv2
import numpy as np

width=650
height=650
alf=3
L=1
n=100
ori=1
root = Tk()
img=np.zeros((height,width,3), np.uint8)
cv2.circle(img, (width/2, height/2), (width/2), (255,0,0), thickness=1, lineType=8, shift=0)
imgTk=ImageTk.PhotoImage(Image.fromarray(img))

class Application(Frame):
	class snowflake:
		def __init__(self, panel):
			self.faces=np.array([[(2-3*pow(3,0.5))*width/4, 3*width/4], [width+(3*pow(3,0.5)-2)*width/4, 3*width/4]])
			x1=self.faces[0,0]
			y1=self.faces[0,1]
			x2=self.faces[1,0]
			y2=self.faces[1,1]
			#initial face must be 3*(sqrt(3)width/2) in width. Therefore has x coords given by
			#   -(3*sqrt(3)-2)width/4 and w+(3*sqrt(3)-2)width/4
			self.faces = np.array([[(2*x1+x2)/3,(2*y1+y2)/3], [0.5*(x1+x2+ori*pow(3,0.5)*(y2-y1)/3),0.5*(y1+y2-ori*pow(3,0.5)*(x2-x1)/3)], [(x1+2*x2)/3,(y1+2*y2)/3]])
			cv2.fillPoly(img, np.int32([self.faces]), 255)
			imgTk=ImageTk.PhotoImage(Image.fromarray(img))
			panel.configure(image=imgTk)
			panel.image = imgTk
			self.useful1=(alf+1.0)/pow(alf,2)
			self.useful2=1
			self.azero=pow(alf,0.5)*L*L/(alf+1.0)
			self.step=0
			self.atotal=alf
			self.ltotal=alf*L
			print np.array(["step", "atotal", "totArea", "totLength", "fractalDim"])
			print(self.step, self.atotal, 1.0*self.atotal*self.azero/alf, self.ltotal, 1.0*self.atotal/alf)
		def makeTriangleOnFace(self, i, panel):
			if(i==self.faces.shape[0]-1):
				j=0
			else:
				j=i+1
			x1=self.faces[i,0]
			y1=self.faces[i,1]
			x2=self.faces[j,0]
			y2=self.faces[j,1]
			#initial face must be 3*(sqrt(3)width/2) in width. Therefore has x coords given by
			#   -(3*sqrt(3)-2)width/4 and w+(3*sqrt(3)-2)width/4
			points = np.array([[(2*x1+x2)/3,(2*y1+y2)/3], [0.5*(x1+x2+ori*pow(3,0.5)*(y2-y1)/3),0.5*(y1+y2-ori*pow(3,0.5)*(x2-x1)/3)], [(x1+2*x2)/3,(y1+2*y2)/3]])
			self.faces=np.insert(self.faces, i+1, points[0], axis=0)
			self.faces=np.insert(self.faces, i+2, points[1], axis=0)
			self.faces=np.insert(self.faces, i+3, points[2], axis=0)
			cv2.fillPoly(img, np.int32([points]), 255)
			imgTk=ImageTk.PhotoImage(Image.fromarray(img))
			panel.configure(image=imgTk)
			panel.image = imgTk
		def reset(self):
			self.faces.clear()
			self.faces=np.array([[(2-3*pow(3,0.5))*width/4, 3*width/4], [width+(3*pow(3,0.5)-2)*width/4, 3*width/4]])
		
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.panel = Label(self, image = imgTk)
		self.panel.pack(side = "bottom", fill = "both", expand = "yes")
		self.sf=self.snowflake(self.panel)
		self.pack()
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		self.QUIT.pack({"side": "left"})
		self.nextStep = Button()
		self.nextStep["text"] = "nextStep"
		self.nextStep["command"] = self.incrementStep
		self.nextStep.pack({"side": "left"})

	def incrementStep(self):
		i=0
		lim=4*self.sf.faces.shape[0]
		while(i<lim):
			#comment out this line to neglect generating the image: comment out for fast calculation of length, area and fractal dimension.
			self.sf.makeTriangleOnFace(i, self.panel)
			i=i+4
		self.sf.ltotal=self.sf.ltotal*(alf+1.0)/alf
		self.sf.atotal+=self.sf.useful2
		self.sf.useful2=self.sf.useful2*self.sf.useful1
		self.sf.step=self.sf.step+1
		print(self.sf.step, self.sf.atotal, 1.0*self.sf.atotal*self.sf.azero/alf, self.sf.ltotal, 1.0*self.sf.atotal/alf)	
		
app = Application(master=root)
app.mainloop()
root.destroy()

