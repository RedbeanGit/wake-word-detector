"""
Provides a WakeWordDetectorEngine class that can be run to start streaming audio from a microphone and detect wake words.
"""

import logging
import numpy as np
import pyaudio
import typing
import threading

from openwakeword.model import Model  # type: ignore

logger = logging.getLogger(__name__)

CHUNK = 16000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


def default_on_detection_callback():
    """
    A default callback function that logs the detection of a wake word.
    """
    logger.info("Wake word detected!")


class WakeWordDetectorEngine:
    """
    A class for running the wake word detection engine.
    """

    def __init__(
        self,
        model: Model,
        on_detection_callback: typing.Callable[
            [], None
        ] = default_on_detection_callback,
        precision: float = 0.05,
    ):
        """
        Initialize the engine with the given wake word models.

        Args:
            model (Model): The model to use for wake word detection.
        """

        logger.info("Initializing Wake Word Detector Engine...")
        self._model = model
        self._on_detection_callback = on_detection_callback
        self._precision = precision
        self._pyaudio_instance = pyaudio.PyAudio()

        self._running = False
        self._thread = None
        logger.info("Wake Word Detector Engine initialized.")

    def start(self):
        logger.info("Starting Wake Word Detector Engine...")
        stream = self._pyaudio_instance.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        self._running = True
        self._thread = threading.Thread(target=self.run, args=(stream,))
        self._thread.start()
        logger.info("Wake Word Detector Engine started.")

    def run(self, stream: pyaudio.Stream):
        while self._running:
            chunk = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            self.process(chunk)

        stream.stop_stream()
        stream.close()

    def stop(self):
        logger.info("Stopping Wake Word Detector Engine...")
        self._running = False

        if self._thread:
            self._thread.join()
        logger.info("Wake Word Detector Engine stopped.")

    def process(self, frame: typing.Iterable[np.ndarray[np.int16, typing.Any]]):
        prediction: dict[str, float] = self._model.predict(frame)  # type: ignore
        logger.debug(f"Prediction: {prediction}")

        for label, confidence in prediction.items():
            if confidence >= self._precision:
                logger.info(f"Detected wake word: {label}")
                self._on_detection_callback()
