# Video: awesome-claude-video-skills

Video vertikal 44 detik (1080x1920, 30 fps) yang memperkenalkan repo
[zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills).

- `scene.html`: semua adegan dan animasi; `render(t)` menggambar frame pada detik ke-t
- `render.js`: merekam frame dengan Playwright
- `music.py`: membuat musik latar (numpy)

Render ulang:
```
python3 music.py /tmp/music.wav
node render.js /tmp/frames 30
ffmpeg -framerate 30 -i /tmp/frames/f%05d.jpg -i /tmp/music.wav -c:v libx264 -pix_fmt yuv420p -crf 20 -c:a aac -shortest awesome-claude-video-skills.mp4
```
