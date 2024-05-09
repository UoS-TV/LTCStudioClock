import pygame
import time
import math

# Initialize Pygame and set up full-screen mode
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Studio Clock")

# Hide the mouse cursor
pygame.mouse.set_visible(False)

# Colors
background_color = (0, 0, 0)  # Black
text_color = (255, 0, 0)  # Red
dot_color = (50,0,0)
hour_color = (255,255,0)

# Font and size settings
# Load the dot matrix font (replace 'dot_matrix.ttf' with your font file)
font_path = "/home/pi/LTCStudioClock/5x7-matrix.ttf"
clock_font_size = 180  # Size for the hour and minute
sec_font_size = 140  # Size for the seconds
clock_font = pygame.font.Font(font_path, clock_font_size)
sec_font = pygame.font.Font(font_path, sec_font_size)

# Clock position
x_center = screen.get_width() // 2
y_center = screen.get_height() // 2

# Circle radius for second markers
sec_radius = screen.get_height() // 2.3

hour_radius = screen.get_height() // 2.5

# Dots size for seconds
dot_size = screen.get_height() // 70

# Main loop to keep the clock running
running = True
while running:
    # Fill the background with black
    screen.fill(background_color)

    # Get current time
    current_time = time.localtime()
    hours_minutes = time.strftime("%H:%M", current_time)  # Hours and minutes
    seconds = int(time.strftime("%S", current_time))  # Seconds as integer
    
    # Draw digital clock (hours and minutes)
    text_hm = clock_font.render(hours_minutes, True, text_color)
    rect_hm = text_hm.get_rect(center=(x_center, y_center - 60))
    screen.blit(text_hm, rect_hm)
    
    # Draw digital seconds
    text_sec = sec_font.render(f"{seconds:02}", True, text_color)
    rect_sec = text_sec.get_rect(center=(x_center, y_center + 120))
    screen.blit(text_sec, rect_sec)

    for angle in range(0, 360, 6):  # Draw up to the current second
        corrected_angle = angle + 90  # To start from the top
        x = x_center - int(sec_radius * math.cos(math.radians(corrected_angle)))
        y = y_center - int(sec_radius * math.sin(math.radians(corrected_angle)))
        pygame.draw.circle(screen, dot_color, (x, y), dot_size)

    # Draw second dots (based on circle parametric equations)
    for angle in range(0, seconds * 6, 6):  # Draw up to the current second
        corrected_angle = angle + 96  # To start from the top
        x = x_center - int(sec_radius * math.cos(math.radians(corrected_angle)))
        y = y_center - int(sec_radius * math.sin(math.radians(corrected_angle)))
        pygame.draw.circle(screen, text_color, (x, y), dot_size)

    for angle in range(0, 360, 30):  # Draw up to the current second
        corrected_angle = angle + 90  # To start from the top
        x = x_center - int(hour_radius * math.cos(math.radians(corrected_angle)))
        y = y_center - int(hour_radius * math.sin(math.radians(corrected_angle)))
        pygame.draw.circle(screen, hour_color, (x, y), dot_size)


    # Update the display
    pygame.display.flip()

    # Event handling (to allow exiting the program)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_q, pygame.K_ESCAPE}:  # Press 'q' or ESC to exit
                running = False

    # Maintain a stable frame rate
    pygame.time.Clock().tick(1)  # Update once per second

# Clean up and exit
pygame.quit()
