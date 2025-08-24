import subprocess
import os
from moviepy.editor import VideoFileClip

def convert_to_sticker(input_path, output_path):
    # Riduci durata massima a 10s per sticker più leggeri
    clip = VideoFileClip(input_path).subclip(0, min(10, int(VideoFileClip(input_path).duration))).resize(height=320)
    temp_path = os.path.join(os.path.dirname(output_path), "temp_sticker.mp4")
    # Scrivi un mp4 intermedio
    clip.write_videofile(temp_path, codec="libx264", audio=False, fps=30, verbose=False, logger=None)
    clip.close()

    # Converti a webm (VP9). NOTA: trasparenza reale richiede canale alfa; qui manteniamo sfondo originale.
    # In seguito si può integrare rimozione sfondo con rembg + compositing su bg trasparente.
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_path,
        "-vf", "scale=320:-1:flags=lanczos,fps=30",
        "-an",
        "-c:v", "libvpx-vp9",
        "-b:v", "700k",
        output_path
    ]
    subprocess.run(cmd, check=True)
    try:
        os.remove(temp_path)
    except Exception:
        pass
