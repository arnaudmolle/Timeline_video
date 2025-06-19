import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import folium
import io
from matplotlib import cm
from matplotlib.colors import rgb2hex
import requests
import textwrap
# Create a DataFrame with your PhD timeline data
data = pd.DataFrame({
    'Date': [
        '2021-10-01', '2021-11-01', '2021-12-01', '2022-01-01', '2022-02-01','2022-04-01', '2022-05-01', '2022-06-05',
        '2022-07-10', '2022-08-15', '2022-09-20', '2022-10-25', '2022-12-01', '2023-02-01','2023-04-01',
        '2023-06-01', '2023-09-01', '2023-10-01', '2023-11-15', '2024-02-01', '2024-03-01',
        '2024-04-01', '2024-05-01', '2024-07-01'
    ],
    'Event': [
        'Accepted as a Food Science PhD Candidate',
        'Start of the PhD at the University of Parma',
        'Cow milk sampling and analysis',
        'Course: Data Analysis and Reproductibility with R',
        'Sheep milk sampling and analysis',
        'First workshop: International Workshop on Spectroscopy and Chemometrics',
        'First oral presentation: SensorFINT International conference',
        'Short term scientific mission Teagasc, financed by CA19145',
        'Course: Advanced Statistical Analysis for Zootechnical science',
        'Visit of Centre Wallon de Recherche Agronomique, CRA-W Gembloux',
        'Oral presentation: Annual meeting of EAAP',
        'Poster presentation: Workshop on the Developments in the Italian PhD Research',
        'Course: Presenting and writing research activities',
        'Teaching Food Science in Rwandan Higher Education institutions',
        'Goat milk sampling and analysis',
        'Oral presentation: SensorFINT Workshop AK Chemometrik with COST',
        'Start of International mobility at Unicamp in the LINA group',
        'First publication: The use of milk FT-IR spectra for predicting cheese-making traits in Grana Padano PDO',
        'Poster presentation: Simposio Latino Americano de Ciencia de los Alimentos y Nutricion',
        'Collaboration: Exploring the use of NIR and Raman spectroscopy for PDO cheeses',
        'Course: Fundamentals and Applications of Near Infrared Spectroscopy',
        'Data Competition. International Workshop on Spectroscopy and Chemometrics',
        'Oral presentation: SensorFint last Conference',
        'Poster presentation: NIR Italia'
    ],
    'Location': [
        'Belgium', 'Italy', 'Italy','Italy', 'Italy','Ireland', 'Slovenia', 'Ireland',
        'Italy', 'Belgium', 'Portugal', 'Italy', 'Italy', 'Rwanda', 'Italy',
        'Germany', 'Brazil', 'Italy', 'Brazil', 'Italy', ' Spain',
        'Ireland', 'Spain', 'Italy'
    ],
    'Coordinates': [
        (50.5039, 4.4699), (44.8015, 10.3279),(44.8015, 10.3279), (44.8015, 10.3279), (44.8015, 10.3279), (53.3498, -6.2603), (45.5289, 13.6569), (53.4129, -8.2439),
        (43.7228, 10.4017), (50.5605, 4.6997), (41.1579, -8.6291), (44.9013, 8.2067), (44.8015, 10.3279), (-1.9403, 29.8739),(44.8015, 10.3279),
        (52.5200, 13.4050), (-22.9068, -47.0622), (44.8015, 10.3279), (-22.9068, -47.0622), (44.8015, 10.3279), (37.8882, -4.7794),
        (53.3498, -6.2603), (37.8882, -4.7794), (45.0703, 7.6869)
    ],
    'Image': [
        'belgium.jpg', 'parma.jpg', 'cow.jpg','unipr.jpg', 'sheep.jpg','dublin.jpg', 'izola.jpg', 'moorepark.jpg',
        'pisa.jpg', 'gembloux.jpg', 'porto.jpg', 'asti.jpg', 'unipr.jpg', 'rwanda.jpg', 'goat.jpg',
        'berlin.jpg', 'campinas.jpg', 'primo.jpg', 'slacan.jpg', 'secondo.jpg', 'cordoba.jpg',
        'dublin.jpg', 'sensorfintcordoba.jpg', 'torino.jpg'
    ]
})

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Set video parameters
width, height = 1920, 1080
duration = 60  # seconds

# Calculate date range
start_date = data['Date'].min() - timedelta(days=30)
end_date = data['Date'].max() + timedelta(days=30)
date_range = (end_date - start_date).days

# Load event images
event_images = {row['Event']: Image.open(row['Image']).resize((600, 400)) for _, row in data.iterrows()}

url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
world_geo = requests.get(url).json()

def create_base_map():
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodbpositron')
    folium.GeoJson(
        world_geo,
        style_function=lambda feature: {
            'fillColor': 'white',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.1,
        }
    ).add_to(m)
    img_data = m._to_png(5)
    return Image.open(io.BytesIO(img_data)).resize((width, height), Image.LANCZOS).convert('RGB')

def create_highlighted_country(country, color):
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodbpositron')
    folium.GeoJson(
        world_geo,
        style_function=lambda feature: {
            'fillColor': 'red' if feature['properties']['name'] == country else 'white',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.5 if feature['properties']['name'] == country else 0,
        }
    ).add_to(m)
    img_data = m._to_png(5)
    return Image.open(io.BytesIO(img_data)).resize((width, height), Image.LANCZOS).convert('RGBA')

# Pre-render base map and highlighted countries

base_map = create_base_map()
highlighted_countries = {event['Location']: create_highlighted_country(event['Location'], 'red')
                         for idx, event in data.iterrows()}

def get_layout_position(index, total):
    positions = ['left', 'center', 'right']
    return positions[index % len(positions)]

def make_frame(t):
    current_date = start_date + timedelta(days=int(t * date_range / duration))
    
    frame = Image.alpha_composite(base_map.convert('RGBA'), highlighted_countries[data.iloc[0]['Location']])  # Initial highlight
    
    # Composite highlighted countries (keeping them highlighted once they appear)
    for idx, event in data.iterrows():
        if event['Date'] <= current_date:
            frame = Image.alpha_composite(frame.convert('RGBA'), highlighted_countries[event['Location']])
    
    frame = frame.convert('RGB')
    draw = ImageDraw.Draw(frame)
    
    timeline_y = 150
    draw.line([(100, timeline_y), (width-100, timeline_y)], fill='black', width=4)

    date_text = current_date.strftime('%B %d, %Y')
    font = ImageFont.truetype("arial.ttf", 36)
    draw.text((width//2-150, 50), date_text, fill='black', font=font)
    
    progress = (current_date - start_date).days / date_range
    current_x = 100 + (width-300)*progress
    draw.ellipse([(current_x - 10, timeline_y - 10), 
                  (current_x + 10, timeline_y + 10)], fill='red')
    
    visible_events = []
    for idx, event in data.iterrows():
        event_initial_x = int((event['Date'] - start_date).days * (width-300) / date_range) + 100
        time_diff = (current_date - event['Date']).days
        
        if -5 <= time_diff < 4 * date_range / duration:
            # Calculate the sliding position with progressive speed increase
            base_speed = 3  # Base sliding speed
            max_speed = 10  # Maximum sliding speed
            speed_factor = min(1, time_diff / (2 * date_range / duration))  # Increases from 0 to 1
            current_speed = base_speed + (max_speed - base_speed) * speed_factor
            
            slide_distance = (current_x - event_initial_x) * current_speed
            event_current_x = event_initial_x - slide_distance
            
            # Only show events that are still on screen
            if 0 <= event_current_x <= width:
                draw.ellipse([(event_initial_x-15, timeline_y-15), (event_initial_x+15, timeline_y+15)], fill='blue')
                visible_events.append((idx, event, time_diff, event_current_x, speed_factor))
    
    # Sort visible events by their current x position, rightmost first
    visible_events.sort(key=lambda x: x[3], reverse=True)
    
    # Display events along the timeline
    for i, (idx, event, time_diff, event_current_x, speed_factor) in enumerate(visible_events):
        # Adjust fade to start later and progress faster
        fade_start = 0.8  # Start fading when speed_factor reaches 0.5
        fade = max(0, min(1, 1 - (speed_factor - fade_start) / (1 - fade_start)))
        
        # Calculate vertical position, alternating above and below the timeline
        image_bottom = height - 50  # 50 points higher than the bottom
        image_pos = (int(event_current_x) - 150, image_bottom - 300)  # 200 is the height of the image
        
        
        # Ensure the image stays within the frame
        image_pos = (max(0, min(width - 600, image_pos[0])), max(0, min(height - 600, image_pos[1])))
        
        # Paste the event image
        event_image = event_images[event['Event']].copy()
        event_image = event_image.convert('RGBA')
        event_image.putalpha(int(255 * fade))
        frame.paste(event_image, image_pos, event_image)
        
        # Create text box
        text_box_width = 600
        text_box_height = 100
        text_box_pos = (image_pos[0], image_pos[1] + 410)  # Position right under the image
        text_box = Image.new('RGBA', (text_box_width, text_box_height), (255, 255, 255, int(200 * fade)))
        text_box_draw = ImageDraw.Draw(text_box)
        
        # Wrap and draw text
        font = ImageFont.truetype("arial.ttf", 28)
        wrapped_text = textwrap.fill(event['Event'], width=40)
        text_box_draw.text((10, 10), wrapped_text, fill=(0, 0, 0, int(255 * fade)), font=font)
        
        # Paste text box onto frame
        frame.paste(text_box, text_box_pos, text_box)
    
    return np.array(frame)

# Create the video clip
video = VideoClip(make_frame, duration=duration)

# Write the result to a file with higher quality settings
video.write_videofile("phd_timeline_improved_folium.mp4", fps=24, codec='libx264', bitrate='8000k')


print("Improved high-quality video saved as 'phd_timeline_improved_folium.mp4'")
