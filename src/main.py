import logging
import time

from openwakeword.model import Model  # type: ignore
from wakeworddetector.engine import WakeWordDetectorEngine

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    logging.info("Loading model...")
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
