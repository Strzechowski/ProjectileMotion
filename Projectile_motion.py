#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPainter, QPen
import math

class ProjectileUI(QMainWindow):
    """Projectile's View (GUI)."""
    def __init__(self, resolution):
        super().__init__()
        # Set main window's properties
        self.setWindowTitle('Projectile!')
        self.resolution = resolution
        self.sizeX = 1100
        self.sizeY = 600
        self._placeWindowInTheMiddle()
        self.g = 10
        self.v0 = 5
        self.alfa = 45
        self.alfa_in_radians = math.radians(self.alfa)
        self.DotSize = 10


    def _placeWindowInTheMiddle(self):
        X = (self.resolution.width() - self.sizeX) / 2
        Y = (self.resolution.height() - self.sizeY) / 2
        self.setGeometry(X, Y, self.sizeX, self.sizeY)
        self.setMaximumSize(2*self.sizeX, self.sizeY)


    def draw_X_axis(self, q_painter, ball_distance, x_start_point, y_start_point, scale):
        q_painter.drawLine(x_start_point, y_start_point + 5, x_start_point + ball_distance * scale, y_start_point + 5)
        fake_ball_distance_used_in_a_loop = int(ball_distance * 100)
        one_part_of_fake_distance = int(fake_ball_distance_used_in_a_loop/25)
        for x in range(0, fake_ball_distance_used_in_a_loop + 1, one_part_of_fake_distance):
            x_value = x / 100
            x_pixels = x_value * scale
            pixels_below_the_axis = 25
            q_painter.drawLine(x_start_point + x_pixels, y_start_point, x_start_point + x_pixels, y_start_point + 10)

            # two and three digit numbers should be moved few pixels more to the left, so they are directly under the ticks
            if x < 10:
                q_painter.drawText(x_start_point + x_pixels - 3, y_start_point + pixels_below_the_axis, str(x_value))
            elif x < 100:
                q_painter.drawText(x_start_point + x_pixels - 9, y_start_point + pixels_below_the_axis, str(x_value))
            else:
                q_painter.drawText(x_start_point + x_pixels - 13, y_start_point + pixels_below_the_axis, str(x_value))


    def draw_balls(self, q_painter, ball_distance, x_start_point, y_start_point, scale):
        fake_ball_distance_used_in_a_loop = int(ball_distance * 100)
        one_part_of_fake_distance = int(fake_ball_distance_used_in_a_loop/25)
        for x in range(0, fake_ball_distance_used_in_a_loop + 1, one_part_of_fake_distance):
            x_value = x / 100
            x_pixels = x_value * scale
            y_value = x_value * math.tan(self.alfa_in_radians) - (self.g / (2 * (self.v0**2) * math.cos(self.alfa_in_radians)**2) * x_value**2)
           # Z_test = self.v0**2 / self.g * math.sin(2 * self.alfa_in_radians)
           # print('X pixels test #%s = %s' %(x, x_pixels))
            y_pixels = y_value * scale
            q_painter.drawEllipse(x_start_point + x_pixels - self.DotSize/2, y_start_point - y_pixels, self.DotSize, self.DotSize)


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.setPen(QPen(Qt.red))

        self.v0 = 30
        Z = self.v0**2 / self.g * math.sin(2 * self.alfa_in_radians)
        print('Z distane = ' + str(Z))

        PositionY = self.sizeY - (4*self.DotSize)
        PositionX = 2*self.DotSize
        pixel_scale = 4 * 250 / Z
        #scale = 4

        print('scale = ' + str(pixel_scale))

        qp.setPen(QPen(Qt.black))
        self.draw_X_axis(qp, Z, PositionX, PositionY, pixel_scale)
        self.draw_balls(qp, Z , PositionX, PositionY, pixel_scale)


class ProjectileCtrl:
    def __init__(self, view):
        self._view = view


def main():
    # Create an instance of QApplication
    projectile = QApplication(sys.argv)
    resolution = projectile.desktop().screenGeometry()

    view = ProjectileUI(resolution)
    view.show()

    ProjectileCtrl(view=view)
    sys.exit(projectile.exec_())

if __name__ == '__main__':
    main()