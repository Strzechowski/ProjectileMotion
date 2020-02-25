#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSlider
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QPointF
from PyQt5.QtGui import QBrush, QPainter, QPen, QPainterPath
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
        self.placeWindowInTheMiddle()
        self.g = 10
        self.v0 = 5
        self.alfa = 5
        self.DotSize = 10

        # Timer setup
        self.wait_at_the_last_ball = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)

        # List of tuples with X and Y coordinates eg. [(x1_pixels, x1_real_value, y1_pixels, y1_real_value),  ...]
        self.coordinates_of_balls = []
        self.amount_of_visible_balls = 0
        # List of tuples with pixels and distance values eg. [(pixels, real_value), ...]
        self.axis_coordinates_and_values = []

        self.create_controls_for_motion_parameters()
        self.basic_motion_calculations()


    def showTime(self):
        if self.amount_of_visible_balls == 27:
            self.wait_at_the_last_ball += 1
            if self.wait_at_the_last_ball == 4:
                self.amount_of_visible_balls = 0
                self.wait_at_the_last_ball = 0
        else:
            self.amount_of_visible_balls += 1
        # Updates the drawing
        self.update()


    def create_controls_for_motion_parameters(self):
        controls = QWidget(self)
        controls.setMaximumSize(self.sizeX/4, self.sizeY/4)
        self.setCentralWidget(controls)

        start_button = QPushButton('Start!', self)
        start_button.clicked.connect(self.on_click)

        self.angle_label = QLabel(self)
        self.angle_label.setText('Angle: %s' % self.alfa)

        self.initial_speed_label = QLabel(self)
        self.initial_speed_label.setText('Initial speed: %s' % self.v0)


        self.initial_speed_slider = QSlider(Qt.Horizontal)
        self.initial_speed_slider.setTickInterval(5)
        self.initial_speed_slider.setMaximum(50)
        self.initial_speed_slider.setMinimum(5)
        self.initial_speed_slider.setSingleStep(5)
        self.initial_speed_slider.setTickPosition(QSlider.TicksBothSides)
        self.initial_speed_slider.valueChanged.connect(self.slider_value_update)


        self.angle_slider = QSlider(Qt.Horizontal)
        self.angle_slider.setTickInterval(5)
        self.angle_slider.setMaximum(70)
        self.angle_slider.setMinimum(5)
        self.angle_slider.setSingleStep(5)
        self.angle_slider.setTickPosition(QSlider.TicksBothSides)
        self.angle_slider.valueChanged.connect(self.angle_slider_value_update)


        main_vertical_layout = QVBoxLayout()
        horizontal_layout_1 = QHBoxLayout()
        horizontal_layout_1.addWidget(self.angle_label)
        horizontal_layout_1.addWidget(self.angle_slider)

        horizontal_layout_2 = QHBoxLayout()
        horizontal_layout_2.addWidget(self.initial_speed_label)
        horizontal_layout_2.addWidget(self.initial_speed_slider)

        horizontal_layout_3 = QHBoxLayout()
        horizontal_layout_3.addWidget(start_button)


        main_vertical_layout.addLayout(horizontal_layout_1)
        main_vertical_layout.addLayout(horizontal_layout_2)
        main_vertical_layout.addLayout(horizontal_layout_3)
        controls.setLayout(main_vertical_layout)


    def slider_value_update(self):
        self.timer.stop()
        self.v0 = self.initial_speed_slider.value()
        self.initial_speed_label.setText('Initial speed: %s' % self.v0)


    def angle_slider_value_update(self):
        self.timer.stop()
        self.alfa = self.angle_slider.value()
        self.angle_label.setText('Angle: %s' % self.alfa)


    def basic_motion_calculations(self):
        self.alfa_in_radians = math.radians(self.alfa)
        # TO DO: Formula explanation
        Z = self.v0**2 / self.g * math.sin(2 * self.alfa_in_radians)
        self.pixel_scale = self.get_scale(Z)

        gap_beetwen_axis_and_frame = 40

        self.y_start_point = self.sizeY - gap_beetwen_axis_and_frame
        self.x_start_point = gap_beetwen_axis_and_frame

        self.count_balls(Z)
        self.count_axis()


    def get_scale(self, distance):
            """ Returns scale based on a distance argument"""
            if distance <= 10:
                scale = 100
            elif distance <= 100:
                scale = 10
            else:
                scale = 4
            return scale


    def count_axis(self):
        temporary_axis_data = []
        for x in range(0, 1001, 40):
            temporary_axis_data.append((x, x / self.pixel_scale))

        self.axis_coordinates_and_values = temporary_axis_data


    def count_balls(self, distance):
        # Loop needs integer values, in case the distance is small it is multiplied by 1000 and divided inside the loop
        fake_ball_distance_used_in_a_loop = int(distance * 1000)
        one_part_of_fake_distance = int(fake_ball_distance_used_in_a_loop/26)
        temporary_balls = []
        for x in range(0, fake_ball_distance_used_in_a_loop + 1, one_part_of_fake_distance):
            x_value = x / 1000
            x_pixels = x_value * self.pixel_scale
            # TO DO: Formula explanation
            y_value = x_value * math.tan(self.alfa_in_radians) - (self.g / (2 * (self.v0**2) * math.cos(self.alfa_in_radians)**2) * x_value**2)
            y_pixels = y_value * self.pixel_scale
            temporary_balls.append((x_pixels, x_value, y_pixels, y_value))

        self.coordinates_of_balls = temporary_balls


    @pyqtSlot()
    def on_click(self):
        self.basic_motion_calculations()
        self.timer.start(200)
        self.amount_of_visible_balls = 0


    def placeWindowInTheMiddle(self):
        X = (self.resolution.width() - self.sizeX) / 2
        Y = (self.resolution.height() - self.sizeY) / 2
        self.setGeometry(X, Y, self.sizeX, self.sizeY)
        self.setMaximumSize(2*self.sizeX, self.sizeY)


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))

        self.draw_X_axis(qp)
        self.draw_Y_axis(qp)
        self.draw_balls(qp)


    def draw_X_axis(self, q_painter):
        q_painter.drawLine(self.x_start_point, self.y_start_point, self.x_start_point + 1000, self.y_start_point)

        for i in range(len(self.axis_coordinates_and_values)):
            x = self.x_start_point + self.axis_coordinates_and_values[i][0]
            x_real_value = self.axis_coordinates_and_values[i][1]
            q_painter.drawLine(x, self.y_start_point - 5, x, self.y_start_point + 5)

            move_label_by_x_pixels, label = self.return_label(x_real_value)
            q_painter.drawText(x - move_label_by_x_pixels - 9, self.y_start_point + 25 , label)


    def draw_Y_axis(self, q_painter):
        q_painter.drawLine(self.x_start_point, self.y_start_point, self.x_start_point, self.y_start_point - 480)

        for i in range(13):
            y = self.y_start_point - self.axis_coordinates_and_values[i][0]
            y_real_value = self.axis_coordinates_and_values[i][1]
            q_painter.drawLine(self.x_start_point - 5, y, self.x_start_point + 5, y)

            move_label_by_x_pixels, label = self.return_label(y_real_value)
            q_painter.drawText(self.x_start_point - move_label_by_x_pixels - 34, y + 5 , label)


    def return_label(self, point_value):
        # When distance is very small the X axis is only up to distance of 10, in that case floating point is apreciated
        # Three digit numbers should be moved few pixels more to the left, so they are directly under the ticks
        move_label_by_x_pixels = 0

        if point_value < 10 and self.pixel_scale == 100:
            label = str(point_value)
        else:
            label = '%.0f' % (point_value)

        if len(label) == 1:
            move_label_by_x_pixels = -4
        elif point_value >= 100:
            move_label_by_x_pixels = 4

        return move_label_by_x_pixels, label



    def draw_balls(self, q_painter):
        start_point = QPointF(self.x_start_point, self.y_start_point)
        path = QPainterPath(start_point)
        for i in range(self.amount_of_visible_balls):
            x = self.x_start_point + self.coordinates_of_balls[i][0]
            y = self.y_start_point - self.coordinates_of_balls[i][2]
            q_painter.drawEllipse(x - self.DotSize/2, y - self.DotSize/2, self.DotSize, self.DotSize)
            if i == 13:
                q_painter.drawText(x, y - 20, 'Highest point y = %.02f' % ( self.coordinates_of_balls[i][3] ))
            path.lineTo(x, y)
            path.moveTo(x, y)
        q_painter.setPen(QPen(Qt.black,  2, Qt.SolidLine))
        q_painter.drawPath(path)


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