class Circle(object):

    def __init__(self,centre,radius):

        self.centre = centre
        self.radius = radius

    def __contains__(self,pt):

        x  = pt[0]
        x1 = self.centre[0]
        y  = pt[1]
        y1 = self.centre[1] 
        
        rd_sq = (x - x1)**2 + (y - y1)**2

        if rd_sq <= self.radius**2:
            return True
        else:
            return False