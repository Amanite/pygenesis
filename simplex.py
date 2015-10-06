import random

class Simplex():
    def __init__(self, tile_size=16):
        self.tile_size = tile_size
        self.perm = []
        for x in xrange(2 * self.tile_size):
            self.perm.append(0)

        permutation = []
        for value in xrange(self.tile_size):
            permutation.append(value)
        random.shuffle(permutation)

        for i in xrange(self.tile_size):
            self.perm[i] = permutation[i]
            self.perm[self.tile_size + i] = self.perm[i]

    @staticmethod
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def lerp(t, a, b):
        return a + t * (b - a)

    @staticmethod
    def grad(seed, x, y, z):
        # CONVERT LO 4 BITS OF HASH CODE INTO 12 GRADIENT DIRECTIONS.
        h = seed & 15
        if h < 8:
            u = x
        else:
            u = y
        if h < 4:
            v = y
        else:
            if h == 12 or h == 14:
                v = x
            else:
                v = z
        if h & 1 == 0:
            first = u
        else:
            first = -u
        if h & 2 == 0:
            second = v
        else:
            second = -v
        return first + second

    def noise_3D(self, x, y, z):
        # FIND UNIT CUBE THAT CONTAINS POINT.
        X = int(x) & (self.tile_size - 1)
        Y = int(y) & (self.tile_size - 1)
        Z = int(z) & (self.tile_size - 1)
        # FIND RELATIVE X,Y,Z OF POINT IN CUBE.
        x -= int(x)
        y -= int(y)
        z -= int(z)
        # COMPUTE FADE CURVES FOR EACH OF X,Y,Z.
        u = self.fade(x)
        v = self.fade(y)
        w = self.fade(z)
        # HASH COORDINATES OF THE 8 CUBE CORNERS
        A = self.perm[X] + Y
        AA = self.perm[A] + Z
        AB = self.perm[A + 1] + Z
        B = self.perm[X + 1] + Y
        BA = self.perm[B] + Z
        BB = self.perm[B + 1] + Z
        # AND ADD BLENDED RESULTS FROM 8 CORNERS OF CUBE
        return self.lerp(w, self.lerp(v,
                                      self.lerp(u, self.grad(self.perm[AA], x, y, z),
                                                self.grad(self.perm[BA], x - 1, y, z)),
                                      self.lerp(u, self.grad(self.perm[AB], x, y - 1, z),
                                                self.grad(self.perm[BB], x - 1, y - 1, z))),
                         self.lerp(v,
                                   self.lerp(u, self.grad(self.perm[AA + 1], x, y, z - 1),
                                             self.grad(self.perm[BA + 1], x - 1, y, z - 1)),
                                   self.lerp(u, self.grad(self.perm[AB + 1], x, y - 1, z - 1),
                                             self.grad(self.perm[BB + 1], x - 1, y - 1, z - 1))))

    def generate_tile(self, size, X, Y):
        octaves = 5
        persistence = 0.8

        amplitude = 1.0
        maxamplitude = 1.0
        for octave in xrange(octaves):
            amplitude *= persistence
            maxamplitude += amplitude

        result = [i[:] for i in [[0]*size]*size]

        for x in xrange(size):
            for y in xrange(size):
                sc = float(size) / self.tile_size
                frequency = 1.0
                amplitude = 1.0
                value = 0.0
                for octave in xrange(octaves):
                    sc *= frequency
                    grey = self.noise_3D((sc * float(x) / size)+X, (sc * float(y) / size)+Y, 0.0)
                    grey = (grey + 1.0) / 2.0
                    grey *= amplitude
                    value += grey
                    frequency *= 2.0
                    amplitude *= persistence
                value /= maxamplitude
                value = int(round(value * 255.0))
                result[y][x] = value
        return result
