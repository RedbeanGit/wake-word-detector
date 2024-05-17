# Wake word detector

This is a simple wake word detector that uses the [OpenWakeWord library](https://github.com/dscripka/openWakeWord) with audio streaming support

## Requirements

- [Python 3.10](https://www.python.org/)
- [Poetry](https://python-poetry.org/)
- [PortAudio](http://www.portaudio.com/)

## Installation

1. Clone the repository

```bash
git clone git@github.com:RedbeanGit/wake-word-detector.git
```

2. Install the dependencies

```bash
cd wake-word-detector
poetry install
```

## Usage

1. Run the detector

```bash
poetry run python src/main.py
```

2. Say the wake word "Dis Cyril"

3. The detector will print "Wake word detected" if the wake word is detected

## Change the callback function

You can change the callback function by modifying the `callback` function in `src/main.py`

```python
import logging
import time

from openwakeword.model import Model  # type: ignore
from wakeworddetector.engine import WakeWordDetectorEngine

logger = logging.getLogger(__name__)

# Create your callback function here
def your_callback():
    # Your code here
    print("Wake word detected")

def main():
    logging.basicConfig(level=logging.INFO)

    logging.info("Loading model...")
    model = Model(
        wakeword_models=["models/dis-cyril.tflite"],
    )

    engine = WakeWordDetectorEngine(model=model, on_detection_callback=your_callback) # Change the callback function here
    engine.start()

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            engine.stop()
            break


if __name__ == "__main__":
    main()
```
