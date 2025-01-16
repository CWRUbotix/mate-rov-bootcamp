# https://github.com/CWRUbotix/rov-software-bootcamp/blob/main/docs/challenge_1_1.md
# TODO write loop to reduce repeating code
from PyQt6.QtWidgets import QApplication, QWidget,QVBoxLayout, QHBoxLayout, QPushButton
from enum import Enum
from bootcamp_harness.rclpy.node import Node
from bootcamp_harness.rclpy.qos import QoSPresetProfiles
from bootcamp_harness.rov_msgs.msg import PixhawkInstruction
from bootcamp_harness import rclpy

def main():
    rclpy.init()
    app = QApplication([])

    window = ButtonPanel()
    window.show()
    
    app.exec()

class MovementType(Enum):
    Stop = 0
    Forward = 1  # Forward/backward
    Vertical = 2  # Up/down
    Lateral = 3  # Left/right
    Pitch = 4  # Tilting up/down
    Yaw = 5  # Turning left/right

class ButtonPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

        node = Node('pixhawk_publisher')
        self.pixhawk_publisher = node.create_publisher(
            PixhawkInstruction,
            'pixhawk_control',
            QoSPresetProfiles.DEFAULT.value
        )

        layout = QVBoxLayout()
        self.setLayout(layout)

        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)

        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

     # Moving up/down, left/right, forward/back, as well as for yawing (turning) left/right ()'←', '→') and pitching (tilting) up/down ('/', '\'). 
        buttons_top = [['Up', MovementType.Vertical, True], ['←', MovementType.Yaw, False], ['↑', MovementType.Forward, True], ['→', MovementType.Yaw, True], ['/', MovementType.Pitch, True], ['Stop', MovementType.Stop, True]]
        buttons_bot = [['Down', MovementType.Vertical, False], ['L', MovementType.Lateral, False], ['↓', MovementType.Forward, False], ['R', MovementType.Lateral, True], ['\\', MovementType.Pitch, False]]
        
        for button in buttons_top:
            button_obj = QPushButton(button[0]);
            top_layout.addWidget(button_obj)
            button_obj.clicked.connect(
                lambda: self.on_button_press(button[1], button[2]))

        for button in buttons_bot:
            button_obj = QPushButton(button[0]);
            bottom_layout.addWidget(button_obj)
            button_obj.clicked.connect(
                lambda: self.on_button_press(button[1], button[2]))
        
    # Functions
    def on_button_press(self, movement_type: MovementType, direction: bool):
        direction_str = 'positively' if direction else 'negatively'

        value = 0.5 if direction else -0.5
        value = 0 if movement_type == MovementType.Stop else value

        instruction = PixhawkInstruction(
            forward=(value if movement_type == MovementType.Forward else 0),
            vertical=(value if movement_type == MovementType.Vertical else 0),
            lateral=(value if movement_type == MovementType.Lateral else 0),
            pitch=(value if movement_type == MovementType.Pitch else 0),
            yaw=(value if movement_type == MovementType.Yaw else 0),
            author=PixhawkInstruction.MANUAL_CONTROL
        )
        self.pixhawk_publisher.publish(instruction)


if __name__ == '__main__':
    main()

