def imgmask(frame,thre = 150):
    img = frame.copy()
    img[img[:,:,0]>thre,2]=0
    img[img[:,:,1]>thre,2]=0
    img[img[:,:,0]>thre,0]=0
    img[img[:,:,0]>thre,1]=0
    img[img[:,:,1]>thre,0]=0
    img[img[:,:,1]>thre,1]=0
    return img
