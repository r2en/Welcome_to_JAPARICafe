#coding: utf-8
import cv2
import numpy as np
from PIL import Image

def resize_image(image, height, width):
    org_height, org_width = image.shape[:2]
    if float(height)/org_height > float(width)/org_width:
        ratio = float(height)/org_height
    else:
        ratio = float(width)/org_width
    resized = cv2.resize(image,(int(org_height*ratio),int(org_width*ratio)))
    return resized

def overlayOnPart(src_image,overlay_image,posX,posY):
    #get the size of the overlay_image
    ol_height,ol_width = overlay_image.shape[:2]

    #convert from BGRA to RGBA
    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGRA2RGBA)
    overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)

    src_image_PIL = Image.fromarray(src_image_RGBA)
    overlay_image_PIL = Image.fromarray(overlay_image_RGBA)

    #change PIL
    src_image_PIL = src_image_PIL.convert('RGBA')
    overlay_image_PIL = overlay_image_PIL.convert('RGBA')

    #prepare the opacity campus
    tmp = Image.new('RGBA',src_image_PIL.size,(255,255,255,0))
    tmp.paste(overlay_image_PIL,(posX,posY),overlay_image_PIL)
    result = Image.alpha_composite(src_image_PIL,tmp)
    return cv2.cvtColor(np.asarray(result),cv2.COLOR_RGBA2BGRA)

def main():
    image_path = "lena.png"
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    ol_image_path = "warai.png"
    ol_image = cv2.imread(ol_image_path,cv2.IMREAD_UNCHANGED)

    cascade_path = "/usr/local/opt/opencv/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
    cascade = cv2.CascadeClassifier(cascade_path)

    facerecog = cascade.detectMultiScale(image_gray,scaleFactor=1.1,minNeighbors=1,minSize=(1,1))

    if len(facerecog) > 0:
        for rect in facerecog:
            print("認識結果")
            print ("(x,y)=(" + str(rect[0]) + "," + str(rect[1])+ ")" + \
                "  高さ："+str(rect[2]) + \
                "  幅："+str(rect[3]))
            
            resized_ol_image = resize_image(ol_image,rect[2],rect[3])
            image = overlayOnPart(image,resized_ol_image,rect[0],rect[1])

    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()