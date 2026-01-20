import cv2 as openCV

class GetColor:
    
    def __init__(self):
        self._x_start = None
        self._y_start = None 
        self._x_end = None
        self._y_end = None
        self._drawing = None 
        self._endDrawing = None 
    
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

    def getColor(self, imagePath):
        
        image = openCV.imread(imagePath)
        
        if image is not None:
            self._x_start, self._y_start, self._x_end, self._y_end = 0, 0, 0, 0
            self._drawing = False
            self._endDrawing = False
            
            rectangles = [] # local onde vao ser as posicoes dos retangulos
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
                    rectangles = []
                    self._drawing = False
                    self._endDrawing = False
                
                elif key == ord("q"):
                    break

            # tenho que guarda todos os retangulos
            rectangles = [(self._x_start, self._y_start), (self._x_end, self._y_end)]
            
            if len(rectangles) == 2:
                roi = image[rectangles[0][1]:rectangles[1][1], rectangles[0][0]:rectangles[1][0]]
                hsvRoi = openCV.cvtColor(roi, openCV.COLOR_BGR2HSV)
                openCV.destroyAllWindows()
                
                color = {
                    "min": [
                        hsvRoi[:,:,0].min(),
                        hsvRoi[:,:,1].min(),
                        hsvRoi[:,:,2].min(),
                    ],
                    "max": [
                        hsvRoi[:,:,0].max(),
                        hsvRoi[:,:,1].max(),
                        hsvRoi[:,:,2].max()
                    ],
                }
                
                return color
            
        else:
            return None