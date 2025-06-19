# Timeline_video

This project generates an animated video timeline in Python, visualizing the main events of your PhD journey. The video features a dynamic map, highlights locations relevant to each event, and displays corresponding images and event details along a timeline.

## Features

- Animated timeline of key PhD events, with event dates and descriptions
- World map highlighting event locations as the timeline progresses (using Folium and PIL)
- Event images appear alongside the timeline with fade-in/fade-out effects
- Events slide onto the timeline, with visually engaging transitions
- Fully customizable data for events, images, and locations

## Requirements

- Python 3.x
- Required libraries (install with pip):
    - numpy
    - pandas
    - moviepy
    - pillow
    - folium
    - matplotlib
    - requests

You can install all dependencies with:
```bash
pip install numpy pandas moviepy pillow folium matplotlib requests
```

## Usage

1. **Clone the repository:**
    ```bash
    git clone https://github.com/arnaudmolle/Timeline_video.git
    cd Timeline_video
    ```

2. **Prepare your images:**
    - Place all the image files referenced in the script (e.g., `belgium.jpg`, `parma.jpg`, etc.) in the same directory as the script, or update the paths as needed in the DataFrame within the script.

3. **Run the script:**
    ```bash
    python "Videotimeline (1).py"
    ```

4. **Output:**
    - The script will generate a video file named `phd_timeline_improved_folium.mp4` in the current directory.

## Customization

- To modify the timeline events, dates, locations, coordinates, or images, edit the `data = pd.DataFrame({ ... })` section in the script.
- You can adjust video parameters (width, height, duration) at the top of the script.
- To use different fonts, update the font path in `ImageFont.truetype`.

## Example

![Example screenshot or GIF here if available]

## License

[Specify your license here, e.g., MIT]

## Author

- Arnaud Molle

---

### Acknowledgements

- The script uses world country data from the [Folium project](https://github.com/python-visualization/folium).
- Developed using open-source Python libraries.
