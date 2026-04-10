#Github repository: https://github.com/Spl4shd/Sprite-Previewer
# (I didn't see the instruction at the top of the assignment to commit 4 times
# throughout the assignment till after I finished.)

import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class SpritePreview(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_frames = 21
        self.frames = load_sprite('spriteImages',self.num_frames)

        # Add any other instance variables needed to track information as the program
        # runs here
        self.current_frame = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        # Make the GUI in the setupUI method
        self.setupUI()

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.sprite_label.setPixmap(self.frames[self.current_frame])

    def setupUI(self):
        # An application needs a central widget - often a QFrame
        frame = QFrame()
        main_layout = QVBoxLayout()

        self.sprite_label = QLabel()
        self.sprite_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sprite_label.setPixmap(self.frames[self.current_frame])

        main_layout.addWidget(self.sprite_label)
        frame.setLayout(main_layout)

        self.setCentralWidget(frame)
        # Add a lot of code here to make layouts, more QFrame or QWidgets, and
        # the other components of the program.
        # Create needed connections between the UI components and slot methods
        # you define in this class.

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.toggle_animation)

        main_layout.addWidget(self.start_button)

        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setRange(1, 100)
        self.fps_slider.setValue(10)
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fps_slider.setTickInterval(10)
        self.fps_slider.valueChanged.connect(self.update_fps)

        main_layout.addWidget(self.fps_slider)

        self.fps_label = QLabel("Frames per second: 10")
        main_layout.addWidget(self.fps_label)

        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_animation)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(pause_action)
        file_menu.addAction(exit_action)

    # You will need methods in the class to act as slots to connect to signals
    def toggle_animation(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("Start")
        else:
            self.timer.start(200)
            self.start_button.setText("Stop")

    def update_fps(self):
        fps = self.fps_slider.value()
        self.fps_label.setText("Frames per second: {fps}".format(fps=fps))

        delay = int(1000 / fps)
        if self.timer.isActive():
            self.timer.start(delay)

    def pause_animation(self):
        self.timer.stop()
        self.start_button.setText("Pause")


def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()