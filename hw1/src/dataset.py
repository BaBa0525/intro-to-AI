import os
import cv2
import matplotlib.pyplot as plt

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    '''
    At first, we read go to the data/train directory, and we find there are 3 directories.
    They are .DS_Store(useless), face and nonface.
    Next, we read the photos in the face and nonface in GRAYSCALE.
    That is because we want to simplify works, decreasing dimensions to 2 per image.
    '''
    try:
      dataset = []
      # dir is the directory in the datapath directory
      for dir in os.listdir(dataPath):
        if(dir == ".DS_Store"):
          continue
        classification = 1 if dir == 'face' else 0
        path = os.path.join(dataPath, dir)
        for file in os.listdir(path):
          # GRAYSCALE because we want to simplify works, decreasing dimensions to 2 per image
          img = cv2.imread(os.path.join(path, file), cv2.IMREAD_GRAYSCALE)
          dataset.append((img, classification))

      return dataset
    # if program explode here 
    except:
      raise NotImplementedError("To be implemented")
    # End your code (Part 1)
