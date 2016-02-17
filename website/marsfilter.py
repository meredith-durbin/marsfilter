import numpy as np
from itertools import product
from scipy.interpolate import interp1d
from scipy.ndimage import interpolation

def marsfilter(img_array):
    img = img_array
    # img = mpimg.imread(imfile)
    mask = np.ones_like(img).astype('float64')
    mask[:,:,1]*= 0.465
    mask[:,:,2]*= 0.25
    marsimg = img*mask 
    x = np.arange(marsimg.shape[0]).reshape(-1,1)
    y = np.arange(marsimg.shape[1]).reshape(-1,1)   
    xy = np.array(list(product(x,y))).reshape(-1,2)
    center = np.mean(xy, axis=0)
    xc, yc = (xy - center).T
    # Polar coordinates
    r = np.sqrt(xc**2 + yc**2)
    theta = np.arctan2(yc, xc)
    a = 0.00022219029946345079
    b = 422.33975030901962
    k = a/(b - (np.max([img.shape[0], img.shape[1]])))
    d = np.linspace(np.min(r) +k*np.min(r)**3, np.max(r)+k*np.max(r)**3, 10000)
    u = d + k*(d**3)
    f = interp1d(u, d, bounds_error=False)
    s = f(r)
    newx = (np.round(s*np.cos(theta))).astype(int).reshape(len(x), len(y)) + int(center[0])
    newy = (np.round(s*np.sin(theta))).astype(int).reshape(len(x), len(y)) + int(center[1])
    one_image = interpolation.map_coordinates(marsimg[:,:,0], coordinates=[newx.flatten(), newy.flatten()]).reshape(marsimg.shape[0],marsimg.shape[1], 1)
    two_image = interpolation.map_coordinates(marsimg[:,:,1], coordinates=[newx.flatten(), newy.flatten()]).reshape(marsimg.shape[0],marsimg.shape[1], 1)
    three_image = interpolation.map_coordinates(marsimg[:,:,2], coordinates=[newx.flatten(), newy.flatten()]).reshape(marsimg.shape[0],marsimg.shape[1], 1)
    new_image = np.append(one_image, np.append(two_image, three_image, axis=2), axis=2)
    return new_image.astype('uint8')
    # imsavefile = 'marsfiter_'+imfile
    # return mpimg.imsave(imsavefile, new_image, dpi=100)