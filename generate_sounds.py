import numpy as np
from scipy.io.wavfile import write

# Parameters
sample_rate = 44100  # Hz
duration = 0.1  # seconds for short sounds

# Generate a simple sine wave sound
def generate_tone(freq, duration, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sound = amplitude * np.sin(2 * np.pi * freq * t)
    return (sound * 32767).astype(np.int16)

# Paddle hit: High-pitched blip (800 Hz, 0.1s)
paddle_sound = generate_tone(800, 0.1)
write("paddle_hit.wav", sample_rate, paddle_sound)

# Brick break: Mid-pitched pop (500 Hz, 0.2s)
brick_sound = generate_tone(500, 0.2)
write("brick_break.wav", sample_rate, brick_sound)

# Game over: Low-pitched descending tone (400 Hz to 200 Hz, 0.5s)
t = np.linspace(0, 0.5, int(sample_rate * 0.5), False)
freq = np.linspace(400, 200, len(t))
game_over_sound = 0.5 * np.sin(2 * np.pi * freq * t)
write("game_over.wav", sample_rate, (game_over_sound * 32767).astype(np.int16))

# Game win: High-pitched ascending tone (200 Hz to 600 Hz, 0.5s)
freq = np.linspace(200, 600, len(t))
game_win_sound = 0.5 * np.sin(2 * np.pi * freq * t)
write("game_win.wav", sample_rate, (game_win_sound * 32767).astype(np.int16))

# Start game: Short chime (1000 Hz, 0.2s)
start_sound = generate_tone(1000, 0.2)
write("start_game.wav", sample_rate, start_sound)

print("Generated WAV files: paddle_hit.wav, brick_break.wav, game_over.wav, game_win.wav, start_game.wav")