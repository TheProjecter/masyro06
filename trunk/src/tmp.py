                # Se comprueba si y es el vecino izquierdo de x.
                t, limite = x[1].isLeftNeighbour(y[1])
                if t and x[1].getLeftNeighbour() > 0:

                    # Actualización de vecinos.
                    x[1].setLeftNeighbour(x[1].getLeftNeighbour() - 1)
                    y[1].setRightNeighbour(y[1].getRightNeighbour() - 1)

                    path1 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(x[0]) + EXT)
                    path2 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(x[0]) + EXT)
                    im1 = Image.open(path1)
                    im2 = Image.open(path2)
                    # finalIbs es el valor final de la banda de interpolación.
                    finalIbs = min(x[1].getIbs(), y[1].getIbs())
                    # Limitex representa el trozo a interpolar de x.
                    limitex = (limite[0], limite[1], limite[2] + finalIbs, limite[3])
                    # Limitey representa el trozo a interpolar de y.
                    limitey = (limite[0] - finalIbs, limite[1], limite[2], limite[3])
                    # LimiteFinal representa todo el trozo a interpolar.
                    limiteFinal = (limitey[0], limitey[1], limitex[2], limitex[3])

                    boxX = (x[1].getX1(), x[1].getY1(), x[1].getX2(), x[1].getY2())
                    regionX = im1.crop(boxX)
                    boxY = (y[1].getX1(), y[1].getY1(), y[1].getX2(), y[1].getY2())
                    regionY = im2.crop(boxY)
                    finalImage.paste(regionX, boxX)
                    finalImage.paste(regionY, boxY)

                    imI = im1.crop(limiteFinal)
                    imD = im2.crop(limiteFinal)
                    mask = Util_image.createMask(limiteFinal[2] - limiteFinal[0], limiteFinal[3] - limiteFinal[1])
                    im3 = Image.composite(imI, imD, mask)
                    finalImage.paste(im3, limiteFinal)                    

                # Se comprueba si y es el vecino inferior de x.
                t, limite = x[1].isDownNeighbour(y[1])
                if t and x[1].getDownNeighbour() > 0:

                    # Actualización de vecinos.
                    x[1].setDownNeighbour(x[1].getDownNeighbour() - 1)
                    y[1].setUpNeighbour(y[1].getUpNeighbour() - 1)

                    path1 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(x[0]) + EXT)
                    path2 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(x[0]) + EXT)
                    im1 = Image.open(path1)
                    im2 = Image.open(path2)
                    # finalIbs es el valor final de la banda de interpolación.
                    finalIbs = min(x[1].getIbs(), y[1].getIbs())
                    # Limitex representa el trozo a interpolar de x.
                    limitex = (limite[0], limite[1] - finalIbs, limite[2], limite[3])
                    # Limitey representa el trozo a interpolar de y.
                    limitey = (limite[0], limite[1], limite[2], limite[3] + finalIbs)
                    # LimiteFinal representa todo el trozo a interpolar.
                    limiteFinal = (limitex[0], limitex[1], limitey[2], limitey[3])

                    boxX = (x[1].getX1(), x[1].getY1(), x[1].getX2(), x[1].getY2())
                    regionX = im1.crop(boxX)
                    boxY = (y[1].getX1(), y[1].getY1(), y[1].getX2(), y[1].getY2())
                    regionY = im2.crop(boxY)
                    finalImage.paste(regionX, boxX)
                    finalImage.paste(regionY, boxY)

                    imI = im1.crop(limiteFinal)
                    imD = im2.crop(limiteFinal)
                    mask = Util_image.createMask(limiteFinal[2] - limiteFinal[0], limiteFinal[3] - limiteFinal[1])
                    im3 = Image.composite(imI, imD, mask)
                    finalImage.paste(im3, limiteFinal)

                # Se comprueba si y es el vecino superior de x.
                t, limite = x[1].isUpNeighbour(y[1])
                if t and x[1].getUpNeighbour() > 0:

                    # Actualización de vecinos.
                    x[1].setUpNeighbour(x[1].getUpNeighbour() - 1)
                    y[1].setDownNeighbour(y[1].getDownNeighbour() - 1)

                    path1 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(x[0]) + EXT)
                    path2 = os.path.join(MASTER_WORK_DIR, str(idWork) + '_' + str(x[0]) + EXT)
                    im1 = Image.open(path1)
                    im2 = Image.open(path2)
                    # finalIbs es el valor final de la banda de interpolación.
                    finalIbs = min(x[1].getIbs(), y[1].getIbs())
                    # Limitex representa el trozo a interpolar de x.
                    limitex = (limite[0], limite[1], limite[2], limite[3] + finalIbs)
                    # Limitey representa el trozo a interpolar de y.
                    limitey = (limite[0], limite[1] - finalIbs, limite[2], limite[3])
                    # LimiteFinal representa todo el trozo a interpolar.
                    limiteFinal = (limitey[0], limitey[1], limitex[2], limitex[3])

                    boxX = (x[1].getX1(), x[1].getY1(), x[1].getX2(), x[1].getY2())
                    regionX = im1.crop(boxX)
                    boxY = (y[1].getX1(), y[1].getY1(), y[1].getX2(), y[1].getY2())
                    regionY = im2.crop(boxY)
                    finalImage.paste(regionX, boxX)
                    finalImage.paste(regionY, boxY)

                    imI = im1.crop(limiteFinal)
                    imD = im2.crop(limiteFinal)
                    mask = Util_image.createMask(limiteFinal[2] - limiteFinal[0], limiteFinal[3] - limiteFinal[1])
                    im3 = Image.composite(imI, imD, mask)
                    finalImage.paste(im3, limiteFinal)                    
