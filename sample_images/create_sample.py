"""
TransitGuard AI - Sample Image Provisioner
Creates test images and downloads standard transit test imagery if network is available.
"""

import urllib.request
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SAMPLE_DIR = Path(__file__).resolve().parent

# Standard lightweight test images (Ultralytics public domain sample assets)
SAMPLE_URLS = {
    "transit_bus_passengers.jpg": "https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/assets/bus.jpg",
}


def download_or_generate_samples():
    """Ensure at least sample images exist for demonstration and testing."""
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Attempt download of realistic commuter/transit test image
    for filename, url in SAMPLE_URLS.items():
        filepath = SAMPLE_DIR / filename
        if not filepath.exists():
            try:
                urllib.request.urlretrieve(url, str(filepath))
                print(f"[OK] Downloaded sample image: {filename}")
            except Exception as e:
                print(f"[Notice] Could not download {filename} ({e}). Generating fallback.")

    # 2. Always generate a local synthetic test image (zero-network guarantee)
    fallback_path = SAMPLE_DIR / "station_platform_ramp_sim.jpg"
    if not fallback_path.exists():
        # Create a 640x480 synthetic station scene
        img = Image.new("RGB", (640, 480), color=(30, 41, 59))
        draw = ImageDraw.Draw(img)

        # Platform floor
        draw.polygon([(0, 200), (640, 200), (640, 480), (0, 480)], fill=(71, 85, 105))
        # Yellow safety edge
        draw.rectangle([(0, 190), (640, 205)], fill=(234, 179, 8))
        # Wheelchair Accessible Ramp (Blue shaded path)
        draw.polygon([(180, 210), (460, 210), (520, 470), (120, 470)], fill=(30, 58, 138))
        # Tactile strips
        for y in range(230, 460, 40):
            draw.line([(150, y), (490, y)], fill=(59, 130, 246), width=3)

        # Labeling
        draw.text((200, 240), "WHEELCHAIR ACCESSIBLE RAMP", fill=(248, 250, 252))
        draw.text((30, 50), "TRANSIT STATION CCTV SIMULATION", fill=(148, 163, 184))
        draw.text((30, 80), "Zone: Platform 1 - West Concourse", fill=(203, 213, 225))

        # Luggage obstruction box on the ramp
        draw.rectangle([(250, 320), (370, 430)], fill=(185, 28, 28), outline=(239, 68, 68), width=3)
        draw.rectangle([(290, 295), (330, 320)], fill=(120, 53, 15), outline=(239, 68, 68), width=2)
        draw.text((270, 365), "SUITCASE", fill=(255, 255, 255))

        img.save(str(fallback_path), quality=95)
        print(f"[OK] Generated synthetic station scene: {fallback_path.name}")


if __name__ == "__main__":
    download_or_generate_samples()
