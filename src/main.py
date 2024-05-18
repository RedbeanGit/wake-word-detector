import logging
import time
import openwakeword  # type: ignore

from openwakeword.model import Model  # type: ignore
from wakeworddetector.engine import WakeWordDetectorEngine

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    logging.info("Loading model...")
    openwakeword.utils.download_models()  # type: ignore
    model = Model(
        wakeword_models=["models/dis-cyril.tflite"],
    )

    engine = WakeWordDetectorEngine(model=model)
    engine.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            engine.stop()
            break


if __name__ == "__main__":
    main()
