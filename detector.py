import numpy


class Detector():

    def __init__(self):
        pass


    def detect(self, rgb):

        coords = numpy.nonzero(rgb)
        v = numpy.mean(coords[0])
        u = numpy.mean(coords[1])

        return numpy.array([u, v])
