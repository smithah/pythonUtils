import cv2

blurry = 0

def variance_of_laplacian(image):
            # compute the Laplacian of the image and then return the focus
            # measure, which is simply the variance of the Laplacian
            return cv2.Laplacian(image, cv2.CV_64F).var()

def blurDetect(imagePath):
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        blurry = 0
                # if the focus measure is less than the supplied threshold,
                # then the image should be considered "blurry"
        if fm < 100.0:
            blurry = 1 
        return(blurry)   
