from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtWidgets import QVBoxLayout, QCheckBox

class CubeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.glWidget = CubeGLWidget()
        self.slice_checkbox = QCheckBox("Pokaż przekrój")
        self.slice_checkbox.stateChanged.connect(self.toggleSlice)

        layout = QVBoxLayout()
        layout.addWidget(self.glWidget)
        layout.addWidget(self.slice_checkbox)
        self.setLayout(layout)

    def toggleSlice(self, state):
        self.glWidget.showSlice = (state == 2)
        self.glWidget.update()
        
        
class CubeGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.slice_position = 0
        self.showSlice = False
        
        self.lastPos = None

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

        glBegin(GL_QUADS)
  
        glEnd()


    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, w / h, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

        glTranslatef(0.0, 0.0, -6.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -6.0)
        
        glRotatef(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotatef(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotatef(self.zRot / 16.0, 0.0, 0.0, 1.0)
        
        if self.showSlice:
            self.drawSlice()
        else:
            self.drawCube()
        self.drawEdges()

    def drawCube(self):
        glBegin(GL_QUADS)
        
        vertices = [
            # Przód
            [-1, -1, 1],  [1, -1, 1],  [1, 1, 1],  [-1, 1, 1],
            # Tył
            [-1, -1, -1], [-1, 1, -1], [1, 1, -1], [1, -1, -1],
            # Góra
            [-1, 1, -1],  [-1, 1, 1],  [1, 1, 1],  [1, 1, -1],
            # Dół
            [-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1],
            # Prawo
            [1, -1, -1],  [1, 1, -1],  [1, 1, 1],  [1, -1, 1],
            # Lewo
            [-1, -1, -1], [-1, -1, 1], [-1, 1, 1], [-1, 1, -1]
        ]

        for i in range(0, len(vertices), 4):
            for vertex in vertices[i:i+4]:
                
                color = [(x + 1) / 2 for x in vertex]
                glColor3f(color[0], color[1], color[2])
                glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

    def drawSlice(self):
        glBegin(GL_QUADS)
        # Define vertices for the slice
        slice_vertices = [
            [-1, -1, self.slice_position], [1, -1, self.slice_position],
            [1, 1, self.slice_position], [-1, 1, self.slice_position]
        ]
        for vertex in slice_vertices:
            color = [(x + 1) / 2 for x in vertex]
            glColor3f(color[0], color[1], color[2])
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

    def drawEdges(self):
        glBegin(GL_LINES)
        edges = [
            # Przód
            [-1, -1, 1], [1, -1, 1], [1, -1, 1], [1, 1, 1], [1, 1, 1], [-1, 1, 1], [-1, 1, 1], [-1, -1, 1],
            # Tył
            [-1, -1, -1], [1, -1, -1], [1, -1, -1], [1, 1, -1], [1, 1, -1], [-1, 1, -1], [-1, 1, -1], [-1, -1, -1],
            # Łączenia przód-tył
            [-1, -1, 1], [-1, -1, -1], [1, -1, 1], [1, -1, -1], [1, 1, 1], [1, 1, -1], [-1, 1, 1], [-1, 1, -1]]
        for edge in edges:
            glColor3f(1.0, 1.0, 1.0)  # White 
            glVertex3f(edge[0], edge[1], edge[2])
        glEnd()

    def mousePressEvent(self, event):
        self.lastPos = event.position()
    def mouseMoveEvent(self, event):
        dx = event.position().x() - self.lastPos.x()
        dy = event.position().y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.position()

    def setXRotation(self, angle):
        self.xRot = angle
        self.update()

    def setYRotation(self, angle):
        self.yRot = angle
        self.update()

    def setZRotation(self, angle):
        self.zRot = angle
        self.update()