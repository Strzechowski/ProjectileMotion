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


    def draw_X_axis(self, q_painter, axis_distance, x_start_point, y_start_point, scale):
        q_painter.drawLine(x_start_point, y_start_point + 5, x_start_point + axis_distance * scale, y_start_point + 5)
        fake_axis_distance_used_in_a_loop = int(axis_distance * 1000)
        one_part_of_fake_distance = int(fake_axis_distance_used_in_a_loop/25)
        for x in range(0, fake_axis_distance_used_in_a_loop + 1, one_part_of_fake_distance):
            x_real_value = x / 1000
            x_pixels = x_real_value * scale
            pixels_below_the_axis = 25
            q_painter.drawLine(x_start_point + x_pixels, y_start_point, x_start_point + x_pixels, y_start_point + 10)

            # TO DO is it working ok now?
            # TO DO if scale has 3 digit numbers, they seem to close to each other
            # two and three digit numbers should be moved few pixels more to the left, so they are directly under the ticks
            if x < 10:
                q_painter.drawText(x_start_point + x_pixels - 3, y_start_point + pixels_below_the_axis, str(x_real_value))
            elif x < 100:
                q_painter.drawText(x_start_point + x_pixels - 9, y_start_point + pixels_below_the_axis, str(x_real_value))
            else:
                q_painter.drawText(x_start_point + x_pixels - 13, y_start_point + pixels_below_the_axis, str(x_real_value))


    def draw_balls(self, q_painter, ball_distance, x_start_point, y_start_point, scale):
        # TO DO NEEDS EXPLANATION WHY * 1000
        fake_ball_distance_used_in_a_loop = int(ball_distance * 1000)
        one_part_of_fake_distance = int(fake_ball_distance_used_in_a_loop/25)
        for x in range(0, fake_ball_distance_used_in_a_loop + 1, one_part_of_fake_distance):
            x_real_value = x / 1000
            x_pixels = x_real_value * scale
            # TO DO formula needs explanation
            y_value = x_real_value * math.tan(self.alfa_in_radians) - (self.g / (2 * (self.v0**2) * math.cos(self.alfa_in_radians)**2) * x_real_value**2)
            y_pixels = y_value * scale
            q_painter.drawEllipse(x_start_point + x_pixels - self.DotSize/2, y_start_point - y_pixels, self.DotSize, self.DotSize)


    # TO DO explanation
    def get_scale(self, distance):
        if distance <= 10:
            scale = 100
        elif distance <= 100:
            scale = 10
        else:
            scale = 4
        return scale

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.setPen(QPen(Qt.black))

        self.v0 = 45
        # TO DO formula eplanation
        Z = self.v0**2 / self.g * math.sin(2 * self.alfa_in_radians)
        pixel_scale = self.get_scale(Z)
        axis_distance = 4 * 250 / pixel_scale

        PositionY = self.sizeY - (4*self.DotSize)
        PositionX = 2*self.DotSize

        self.draw_X_axis(qp, axis_distance, PositionX, PositionY, pixel_scale)
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