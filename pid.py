
class PI():

    def __init__(self, p_gain, i_gain, dt):

        self.p = p_gain
        self.i = i_gain
        self.dt = dt

        self.error_integral = 0.0


    def control(self, error):

        self.error_integral += error * self.dt

        return self.p * error + self.i * self.error_integral
