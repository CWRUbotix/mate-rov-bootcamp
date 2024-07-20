from typing import TypeVar, Any
import pickle

import zmq

from bootcamp_harness.rclpy.qos import QoSProfile, QoSPresetProfiles

MsgType = TypeVar('MsgType')


class Publisher:
    def __init__(
        self,
        msg_type: MsgType,
        topic: str,
        qos_profile: QoSProfile
    ) -> None:
        """
        Create a container for a ROS publisher.

        .. warning:: Users should not create a publisher with this constuctor, instead they should
           call :meth:`.Node.create_publisher`.

        A publisher is used as a primary means of communication in a ROS system by publishing
        messages on a ROS topic.

        :param msg_type: The type of ROS messages the publisher will publish.
        :param topic: The name of the topic the publisher will publish to.
        :param qos_profile: The quality of service profile to apply to the publisher.
        """

        if qos_profile != QoSPresetProfiles.DEFAULT.value:
            raise ValueError('CWRUbotix tip: your qos_profile should be'
                             'QoSPresetProfiles.DEFAULT.value')

        self.msg_type = msg_type
        self.topic = topic
        self.topic_bytes = bytes(topic, 'utf-8')
        self.qos_profile = qos_profile

        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://localhost:5555")

        print(f'Publisher connected to topic {topic}')

    def publish(self, msg: Any) -> None:
        """
        Send a message to the topic for the publisher.

        :param msg: The ROS message to publish.
        :raises: TypeError if the type of the passed message isn't an instance
          of the provided type when the publisher was constructed.
        """

        msg_bytes: bytes
        if isinstance(msg, self.msg_type):  # TODO: why doesn't Mypy like this?
            msg_bytes = pickle.dumps(msg)
        elif isinstance(msg, bytes):
            msg_bytes = msg
        else:
            raise TypeError(f'Expected {self.msg_type}, got {type(msg)}')
        
        multipart_msg = [self.topic_bytes, msg_bytes]
        print(f'Publishing: {multipart_msg}')
        self.socket.send_multipart(multipart_msg)
