import numpy as np
from scipy.optimize import minimize

'''
sample_pixel takes a labelPixelCoordinate and returns coordinates of its 14 neighbors
'''
def sample_pixels(labelPixelCoordinate):
    neighboringPixelCoordinates = []
    for i in range(labelPixelCoordinate[0]-2, labelPixelCoordinate[0]+3):
        for j in range(labelPixelCoordinate[1]-2, labelPixelCoordinate[1]+3):
            neighboringPixelCoordinates.append([i,j])
    return neighboringPixelCoordinates


'''
find_maximum_distance finds a color in palette that has the maximum distance from neighboring pixel coordinates, which are 
sampled from background_image
'''
def find_maximum_distance(background_image, neighboringPixelCoordinates, palette):
    distances = []
    # derive RGB values of neighboring pixels from background_image
    neighboringPixelValues = [background_image[coord[0], coord[1], :] for coord in neighboringPixelCoordinates]

    # iterate through the palette and calculate each color's distance from neighboring pixel values
    for i in range(len(palette)):
        distanceSum = 0
        for j in range(len(neighboringPixelCoordinates)):
            distanceSum += np.linalg.norm(palette[i]-background_image[neighboringPixelCoordinates[j][0], neighboringPixelCoordinates[j][1],:])
        distances.append(distanceSum)
    
    # Derive the index of the color in the palette that has the maximum distance value 
    maxDistanceColorIdx = np.argmax(distances)

    # Return the color whose index was found in the previous step
    return palette[maxDistanceColorIdx]


'''
palette-generator generates a palette given numColors
THIS FUNCTION NEEDS TO BE REVISED SO THAT IT RETURNS AN ARRAY WITH VALUES BETWEEN 0 and 255
'''
def palette_generator(numColors):
    palette =[]
    startingColor = np.random.rand(3)*255
    secondColor = np.asarray([255-startingColor[0], 255-startingColor[1], 255-startingColor[2]])

    palette.append(startingColor)
    palette.append(secondColor)

    for i in range(2,numColors):
        # get the two previous colors of the current color in the palette
        prevColors = [palette[i-2], palette[i-1]]
        # find a point that has the largest distance from prevColors
        newColor = minimize(lambda point: -1*(np.linalg.norm(prevColors[0] - point) + np.linalg.norm(prevColors[1] - point)), 
                            x0=np.asarray([0,0,0])).x
        palette.append(newColor)
    return palette

'''
References: 
http://www.realtimerendering.com/blog/low-discrepancy-color-sequences/
http://www.realtimerendering.com/blog/low-discrepancy-color-sequences-part-deux/
https://stackoverflow.com/questions/52974075/maximize-objective-function-using-scipy-optimize
'''
