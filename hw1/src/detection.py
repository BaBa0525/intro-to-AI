from fileinput import filename
import os
import cv2
from cv2 import WINDOW_NORMAL
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    '''
    first, we read the txt file, and get the coordinates of the face rectangle.
    Then, we read the photo twice, one is original RGB photo, the other one is grayscale
    for the same reason we have mentioned in dataset.py.
    Then we extract the area we need and transfer it to 19x19 because we our training datas
    are 19x19. And the reason I guess is to simplify calculation.
    Then, we use classifiers we have trained to judge if this rectangle contains face.
    if it does, we draw this rectangle with green line on the photo.
    Otherwise, draw it with red color.
    Last, we show the graph.
    '''
    # path[0] = the directory the txt file in, we need this path to access .jpg files.
    path = os.path.split(dataPath)
    green_color = (0, 255, 0)
    red_color = (0, 0, 255)

    try:
      #picture format: { file_name:[[the face coordinates], ...], ...}
      picture = {}
      filename = []
      with open (dataPath) as f:
        for lin in f:
          file, cnt = lin.split()
          picture[file] = []
          filename.append(file)
          cnt = int(cnt)
          for i in range(cnt):
            line = f.readline()
            loca1 = line.split()
            loca2 = [int(num) for num in loca1]
            picture[file].append(loca2)
      
      for name in filename:
        pic_path = os.path.join(path[0], name)
        img_gray = cv2.imread(pic_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(pic_path, cv2.IMREAD_UNCHANGED)

        for loca in picture[name]:
          x, y, width, height = loca[0], loca[1], loca[2], loca[3]
          # extract the specific area in images and change the graph to 19x19
          img_cut = img_gray[y:y+height, x:x+width]
          img_cut = cv2.resize(img_cut, (19, 19), interpolation=cv2.INTER_AREA)
          prediction = clf.classify(img_cut)
          if(prediction == 1):
            cv2.rectangle(img, (x, y), (x+width, y+height), green_color, 1, cv2.LINE_AA)
          else:
            cv2.rectangle(img, (x, y), (x+width, y+height), red_color, 1, cv2.LINE_AA)
        cv2.imshow('img', img)
        cv2.waitKey(0)
    except: 
      raise NotImplementedError("To be implemented")
    # End your code (Part 4)

