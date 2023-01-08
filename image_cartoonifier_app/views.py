from django.shortcuts import render
import cv2
import sys
import matplotlib.pyplot as plt
from .models import UserUpload


def index(request):
    return render(request,"index.html",{"name":"None"})

def cartoonify(request):
    img = request.FILES['image']
    id = UserUpload.objects.create(image=img)
    name = cartoonify_helper(id.id)
    name = "image_cartoonifier_app/media/images/"+str(name)
    print(name)
    return render(request,"index.html",{"name":name})


def cartoonify_helper(ImagePath):
    # read the image
    ImagePath = "image_cartoonifier_app/media/"+str(UserUpload.objects.get(id=ImagePath).image)
    from PIL import Image
    img = Image.open(ImagePath)
  
    # get width and height
    width = img.width
    height = img.height
    originalmage = cv2.imread(ImagePath,cv2.IMREAD_COLOR)
   
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers

    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    ReSized1 = cv2.resize(originalmage, (width, height))
    #plt.imshow(ReSized1, cmap='gray')


    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (width, height))
    #plt.imshow(ReSized2, cmap='gray')


    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (width, height))
    #plt.imshow(ReSized3, cmap='gray')

    #retrieving the edges for cartoon effect
    #by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (width, height))
    #plt.imshow(ReSized4, cmap='gray')

    #applying bilateral filter to remove noise 
    #and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    ReSized5 = cv2.resize(colorImage, (width, height))
    #plt.imshow(ReSized5, cmap='gray')


    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    ReSized6 = cv2.resize(cartoonImage, (width, height))
    #plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    # plt.show()
    return save(ReSized6,ImagePath)
    
    
def save(ReSized6, ImagePath):
    import os,random,string
    #saving an image using imwrite()
    newName=''.join(random.choices(string.ascii_lowercase +string.digits, k=15))
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    name = newName+extension
    return name