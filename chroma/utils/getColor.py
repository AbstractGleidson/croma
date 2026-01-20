import cv2 as openCV
import numpy

class GetColor:
    
    def __init__(self):
        self._x_start = None
        self._y_start = None 
        self._x_end = None
        self._y_end = None
        self._drawing = None 
        self._endDrawing = None 
        self.rectangles = [] # local onde vao ser as posicoes dos retangulos
        
        self._points = [] # pontos para getColorByPoint
        self._drawingP = None
        self._xp = None
        self._yp = None
    
    # Escuta os eventos 
    def _click_and_crop(self, event, x, y, flags, param):    
        
        if event == openCV.EVENT_LBUTTONDOWN: # Mouse foi pressionado para baixo
            self._x_start, self._y_start, self._x_end, self._y_end = x, y, x, y
            self._drawing = True # Indica que comecou um desenho 
            self._endDrawing = False # Inidca que comecou um novo desenho
            
        elif event == openCV.EVENT_MOUSEMOVE: # Mouse em movimento
            if self._drawing == True:
                self._x_end, self._y_end = x, y # define o final do desenho
                    
        elif event == openCV.EVENT_LBUTTONUP: # Mouse terminou o movimento
            self._x_end, self._y_end = x, y
            self._drawing = False
            self._endDrawing = True
            
            if self._x_start != self._x_end and self._y_start != self._y_end:
                self.rectangles.append({"start": (self._x_start, self._y_start), "end": (self._x_end, self._y_end)})
                
    def _click(self, event, x, y, flags, param):
        if event == openCV.EVENT_LBUTTONDBLCLK:
            self._xp, self._yp = x, y
            self._points.append((x, y))
            self._drawingP = True

    def getColorByRect(self, imagePath):
        
        image = openCV.imread(imagePath)
        
        if image is not None:
            self._x_start, self._y_start, self._x_end, self._y_end = 0, 0, 0, 0
            self._drawing = False
            self._endDrawing = False
            
            drawingImage = image.copy()
            
            # Cria uma janle
            openCV.namedWindow("Selecione a cor do plano de fundo")
            openCV.setMouseCallback("Selecione a cor do plano de fundo", self._click_and_crop)

            while True:
                i = drawingImage.copy()
                
                if not self._drawing and not self._endDrawing:
                    openCV.imshow("Selecione a cor do plano de fundo", drawingImage)
                    
                elif self._drawing and not self._endDrawing:
                    openCV.rectangle(i, (self._x_start, self._y_start), (self._x_end, self._y_end), (0, 255, 0), 2)
                    openCV.imshow("Selecione a cor do plano de fundo", i)
                    
                elif not self._drawing and self._endDrawing:
                    openCV.rectangle(drawingImage, (self._x_start, self._y_start), (self._x_end, self._y_end), (0, 255, 0), 2)
                    openCV.imshow("Selecione a cor do plano de fundo", drawingImage)
                    
                key = openCV.waitKey(1) & 0xFF     
                
                if key == ord("s"): # cor selecionada
                    self._endDrawing = False 
                    break    
                
                elif key == ord("r"): # reseta os desnhos da imagem
                    drawingImage = image.copy()
                    self.rectangles = []
                    self._drawing = False
                    self._endDrawing = False
                
                elif key == ord("q"):
                    break
            
            if len(self.rectangles) >= 1:
                openCV.destroyAllWindows() # destroi todas as janelas
                imageHsv = openCV.cvtColor(image, openCV.COLOR_BGR2HSV)
                
                maxC = []
                minC = []
                
                print()
                print(self.rectangles)
                print()
                
                for i, rect in enumerate(self.rectangles):
                    
                    if rect["start"] != rect["end"]: # Verifica se realmente é um retangulo
                        imageCut = imageHsv[rect["start"][1]:rect["end"][1], rect["start"][0]:rect["end"][0]]
                        
                        if i == 0:
                            maxC = [imageCut[:,:,0].max(), imageCut[:,:,1].max(), imageCut[:,:,2].max()]
                            minC = [imageCut[:,:,0].min(), imageCut[:,:,1].min(), imageCut[:,:,2].min()]
                        
                        else:
                            maxC = [max(imageCut[:,:,0].max(), maxC[0]), max(imageCut[:,:,1].max(), maxC[1]), max(imageCut[:,:,2].max(), maxC[2])]
                            minC = [min(imageCut[:,:,0].min(), minC[0]), min(imageCut[:,:,1].min(), minC[1]), min(imageCut[:,:,2].min(), minC[2])]
                            
                return {"min": minC, "max": maxC}
            
            else:
                return None
    
    def getColorByPoint(self, imagePath):
        
        image = openCV.imread(imagePath)
        
        if image is not None:
            self._drawingP = False
            drawingImage = image.copy()
            
            # Cria uma janle
            openCV.namedWindow("Selecione a cor do plano de fundo")
            openCV.setMouseCallback("Selecione a cor do plano de fundo", self._click)

            while True:
               
                if not self._drawingP:
                    drawingImage[self._xp, self._yp] = numpy.array([0, 255, 0]).astype("uint8")
                    self._drawingP = False 
                
                openCV.imshow("Selecione a cor do plano de fundo", drawingImage)
                    
                key = openCV.waitKey(1) & 0xFF     
                
                if key == ord("s"): # cor selecionada 
                    break    
                
                elif key == ord("r"): # reseta os desnhos da imagem
                    drawingImage = image.copy()
                    self._points = []
                    self._drawingP = False
                
                elif key == ord("q"):
                    break
            
            if len(self._points) >= 2:
                openCV.destroyAllWindows() # destroi todas as janelas
                imageHsv = openCV.cvtColor(image, openCV.COLOR_BGR2HSV)

                h, s, v = [], [], []
                
                for point in enumerate(self._points):
                    
                    imageCut = imageHsv[point[0], point[1]]
                    h.append(imageCut[:,:,0])
                    s.append(imageCut[:,:,1])
                    v.append(imageCut[:,:,2])
                            
                
                return {
                    "min": [min(h), min(s), min(v)],
                    "max": [max(h), max(s), max(v)]
                    }
            
            else:
                return None