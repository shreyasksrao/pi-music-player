#!/usr/bin/env python3

import argparse
import logging
import os
# Set the environment variable to suppress the Pygame message
# This has to be set before importing pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import time


def setup_logger(log_directory, log_filename):
    # Ensure the log directory exists
    os.makedirs(log_directory, exist_ok=True)
    log_file_path = os.path.join(log_directory, log_filename)

    logger = logging.getLogger('MusicPlayer')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

# This method validate the passed music files for there existence. 
# If music_files parameter is not passed, then it add all the mp3s to the list.
# Each entry contains directory + filename 
def get_music_files_list(logger:logging.Logger, music_directory, music_files):
    logger.info("Getting MP3 files...")
    music_list = []
    if music_files:
        logger.info("Music list is passed as the argument, validating the file existence...")
        music_files = music_files.split(',')
        for music_file in music_files:
            file_path = os.path.join(music_directory, music_file.strip())
            if not os.path.isfile(file_path):
                logger.error(f"Music file - {music_file} not found in the directory ${music_directory}.")
            logger.info(f"Successfully added music file - {music_file} to the list.")
            music_list.append(file_path)
    else:
        # If no files are provided, get all MP3 files from the directory
        music_list = [os.path.join(music_directory, f) for f in os.listdir(music_directory) if f.endswith('.mp3')]
        logger.info(f"Added all the MP3 files to the list.")
    logger.info(f"Music file list is - {music_list}")

    if not music_list:
        logger.warning("No MP3 files found to play.")
        return
    return music_list

def play_music(logger:logging.Logger, music_files):
    # Initialize the pygame mixer
    pygame.mixer.init()
    logger.info(f"Starting to play music from the list: {music_files}")
    # Play each specified MP3 file
    for music_file in music_files:
        if os.path.isfile(music_file):
            logger.info(f"Playing: {music_file.strip()}")
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            try:
                # Keep the program running while the music plays
                while pygame.mixer.music.get_busy():
                    time.sleep(5)
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt signal received. Exiting...")
                pygame.mixer.music.stop()
                logger.info("Music stopped")
                break
        else:
            logger.error(f"File not found: {music_file}")
    pygame.mixer.quit()
    logger.info("Cleaned up the pygame mixer") 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play MP3 files from a specified directory or list.')
    parser.add_argument('--musicDirectory', type=str, default='.', 
                        help='Directory where the MP3 files are stored (default: current directory)')
    parser.add_argument('--musicFiles', type=str, help='Comma-separated list of specific MP3 files to play')
    parser.add_argument('--logDirectory', type=str, default='.', 
                        help='Directory to store the log file (default: current directory)')
    parser.add_argument('--logFilename', type=str, default='music_player.log',
                        help='Log file name (default: music_player.log)')
    args = parser.parse_args()

    musicDirectory = args.musicDirectory
    musicFiles = args.musicFiles

    logger = setup_logger(args.logDirectory, args.logFilename)
    music_list = get_music_files_list(logger, musicDirectory, musicFiles)
    play_music(logger, music_list)
