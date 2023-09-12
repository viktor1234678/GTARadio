import pygame
import time
import os

music_folder = "RadioMusik/GTA5"
image_folder = 'RadioLogos/GTA5'

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png') or f.endswith('.jpg')]

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.init()

music_files = [file for file in os.listdir(music_folder)]
num_songs = len(music_files)

current_song_index = 0
start_time = time.time()

pygame.mixer.music.load(os.path.join(music_folder, music_files[current_song_index]))
pygame.mixer.music.play()

# Set the display size
window_size = (240, 240)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Image Viewer')

# Initialize variables
ChannelIndex = 0
total_images = len(image_files)
running = True
sliding = False  # Flag to control sliding effect
slidingLeft = False  # Flag to control sliding effect
slidingRight = False  # Flag to control sliding effect

key_pressed = False  # Flag to indicate if a key is currently being held down

def load_and_resize_image(index, target_size):
    image_path = os.path.join(image_folder, image_files[index])
    loaded_image = pygame.image.load(image_path)
    return pygame.transform.smoothscale(loaded_image, target_size)

# Initialize surfaces and positions
current_image_surface = load_and_resize_image(ChannelIndex, window_size)
next_image_surface = None
current_image_x = 0
if(slidingLeft):
    next_image_x = window_size[0]
if(slidingRight):
    next_image_x = -window_size[0]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not sliding:
                ChannelIndex = (ChannelIndex - 1) % total_images
                next_image_surface = load_and_resize_image(ChannelIndex, window_size)
                current_image_x = 0
                next_image_x = -window_size[0]
                slidingLeft = True
                sliding = True
                key_pressed = True

                # Move to the previous song
                current_song_index = (current_song_index - 1) % num_songs
                pygame.mixer.music.load(os.path.join(music_folder, music_files[current_song_index]))
                elapsed_time = time.time() - start_time
                pygame.mixer.music.play()
                pygame.mixer.music.set_pos(elapsed_time % pygame.mixer.Sound(
                    os.path.join(music_folder, music_files[current_song_index])).get_length())

            elif event.key == pygame.K_RIGHT and not sliding:
                ChannelIndex = (ChannelIndex + 1) % total_images
                next_image_surface = load_and_resize_image(ChannelIndex, window_size)
                current_image_x = 0
                next_image_x = window_size[0]
                slidingRight = True
                sliding = True
                key_pressed = True

                current_song_index = (current_song_index + 1) % num_songs
                pygame.mixer.music.load(os.path.join(music_folder, music_files[current_song_index]))
                elapsed_time = time.time() - start_time
                pygame.mixer.music.play()
                pygame.mixer.music.set_pos(elapsed_time % pygame.mixer.Sound(
                os.path.join(music_folder, music_files[current_song_index])).get_length())

        elif event.type == pygame.KEYUP:
            key_pressed = False

    if sliding:
        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the current and next images with sliding effect

        if slidingLeft:
            screen.blit(current_image_surface, (current_image_x, 0))
            screen.blit(next_image_surface, (next_image_x, 0))
            current_image_x += 1
            next_image_x += 1

        if slidingRight:
            screen.blit(current_image_surface, (current_image_x, 0))
            screen.blit(next_image_surface, (next_image_x, 0))
            current_image_x -= 1
            next_image_x -= 1

        # If the current image has moved completely off the screen, stop sliding
        if current_image_x <-window_size[0] or current_image_x > 240:
            current_image_x = 0
            current_image_surface = next_image_surface
            slidingLeft = False
            slidingRight = False
            sliding = False

    pygame.display.flip()
    pygame.time.delay(1)  # Delay for smoother animation

# Quit pygame
pygame.mixer.quit()
pygame.quit()