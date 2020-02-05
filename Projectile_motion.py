#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPainter, QPen

class ProjectileUI(QMainWindow):
    """Projectile's View (GUI)."""
    def __init__(self, resolution):
        super().__init__()
        # Set main window's properties
        self.setWindowTitle('Projectile!')
        self.resolution = resolution
        self.sizeX = 800
        self.sizeY = 600
        self._placeWindowInTheMiddle()

    def _placeWindowInTheMiddle(self):
        X = (self.resolution.width() - self.sizeX) / 2
        Y = (self.resolution.height() - self.sizeY) / 2
        self.setGeometry(X, Y, self.sizeX, self.sizeY)
        self.setMaximumSize(2*self.sizeX, self.sizeY)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))

        DotSize = 10
        qp.drawEllipse(2*DotSize, self.sizeY - (2*DotSize), DotSize, DotSize)


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