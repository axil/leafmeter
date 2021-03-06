# -*- coding: utf-8 -*-
## Add path to library (just for examples; you do not need this)
#import initExample

from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt

pg.setConfigOptions(imageAxisOrder='row-major')

## create GUI
app = QtGui.QApplication([])

Q = 100
rgb = plt.imread('7.jpg')[1000-Q:1000+Q,1500-Q:1500+Q,:]
lab = np.load('7.npz')['arr_0'][1000-Q:1000+Q,1500-Q:1500+Q,:]

arr = lab[:,:,0]

# This is the main graphics widget
w = pg.GraphicsLayoutWidget(show=True, size=(800,800), border=True)

# Top-left scene in the graphics widget
v = w.addViewBox(0,0)
v.invertY(True)  ## Images usually have their Y-axis pointing downward
v.setAspectLocked(True)
im1 = pg.ImageItem(rgb)   # Create image widget, add to scene and set position 
v.addItem(im1)
v.setRange(QtCore.QRectF(0, 0, 200, 120))

# Top-right scene in the graphics widget
v2 = w.addViewBox(0,1)
im3 = pg.ImageItem()
v2.addItem(im3)
v2.setRange(QtCore.QRectF(0, 0, 60, 60))
v2.invertY(True)
v2.setAspectLocked(True)
im3.setZValue(10)

# Bottom plot in the main graphics widget
pi1 = w.addPlot(1,0, colspan=2)
pi1.setXRange(-100, 100, padding=0)
pi1.setYRange(-100, 100, padding=0)
pi1.showGrid(x = True, y = True, alpha = 0.3)

# Create ROIs
def updateRoiPlot(roi, a=None, b=None):
    if a is None:
        a = roi.getArrayRegion(lab[:,:,1], img=im1)
        b = roi.getArrayRegion(lab[:,:,2], img=im1)
    if a is not None:
        roi.curve.setData({'x': a.flatten(), 'y': b.flatten()})#data.mean(axis=1))

_L, _a, _b = 0, 1, 2
#lastRoi = None
def updateRoi(roi):
    global im1, im3, arr#, lastRoi
    if roi is None:
        return
    print(roi.pos(), roi.size(), roi.getAffineSliceParams(im1.image, im1))
    
    a0, b0 = roi.pos()
    a1, b1 = roi.pos() + roi.size()
    #mask = (lab[:,:,_L] > ref[_L]-5) & (lab[:,:,_L] < ref[_L]+5) & \
    mask = (lab[:,:,_a] >= a0) & (lab[:,:,_a] <= a1) & \
           (lab[:,:,_b] >= b0) & (lab[:,:,_b] <= b1)
    
    rgbm = rgb.copy()
    rgbm[~mask] = [0,0,255]
    #lastRoi = roi
    #arr1 = roi.getArrayRegion(im1.image, img=im1)
    im3.setImage(rgbm)
  
rois = []
rois.append(pg.TestROI([0,  0], [20, 20], maxBounds=QtCore.QRectF(-100, -100, 230, 230), pen=(0,9)))

# Add each ROI to the scene and link its data to a plot curve with the same color
for r in rois:
    pi1.addItem(r)
    c = pi1.plot(x=[1,2,3], y=[1,4,9], pen=(0,0,0), symbol='o', symbolSize=5)
    r.curve = c
    r.sigRegionChanged.connect(updateRoi)

a = lab[:,:,1]
b = lab[:,:,2]
rois[0].curve.setData({'x': a.flatten(), 'y': b.flatten()})#data.mean(axis=1))

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
