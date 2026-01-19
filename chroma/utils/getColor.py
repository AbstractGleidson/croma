import cv2 as openCV

class GetColor:
    
    _x_start = None
    _y_start = None 
    _x_end = None
    _y_end = None
    _cropping = None 
    _getROI = None 
    
    @classmethod
    def _click_and_crop(cls, event, x, y, flags, param):    
        
        if event == openCV.EVENT_LBUTTONDOWN:
            cls._x_start, cls._y_start, cls._x_end, cls._y_end = x, y, x, y
            cls._cropping = True
            
        elif event == openCV.EVENT_MOUSEMOVE:
            if cls._cropping == True:
                cls._x_end, cls._y_end = x, y
                    
        elif event == openCV.EVENT_LBUTTONUP:        
            cls._x_end, cls._y_end = x, y
            cls._cropping = False
            cls._getROI = True

    @classmethod
    def getColor(cls, imagePath):
        
        image = openCV.imread(imagePath)
        
        if image is not None:
            cls._x_start, cls._y_start, cls._x_end, cls._y_end = 0, 0, 0, 0
            cls._cropping = False
            cls._getROI = False
            
            refPt = []

            clone = image.copy()
            
            openCV.namedWindow("image")
            openCV.setMouseCallback("image", GetColor._click_and_crop)

            while True:
                i = image.copy()
                
                if not cls._cropping and not cls._getROI:
                    openCV.imshow("image", image)
                    
                elif cls._cropping and not cls._getROI:
                    openCV.rectangle(i, (cls._x_start, cls._y_start), (cls._x_end, cls._y_end), (0, 255, 0), 2)
                    openCV.imshow("image", i)
                    
                elif not cls._cropping and cls._getROI:
                    openCV.rectangle(image, (cls._x_start, cls._y_start), (cls._x_end, cls._y_end), (0, 255, 0), 2)
                    openCV.imshow("image", image)
                    
                key = openCV.waitKey(1) & 0xFF     
                
                if key == ord("r"):
                    image = clone.copy()
                    cls._getROI = False 
                    break    
                
                elif key == ord("c"):
                    break

            refPt = [(cls._x_start, cls._y_start), (cls._x_end, cls._y_end)]
            
            if len(refPt) == 2:
                roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
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