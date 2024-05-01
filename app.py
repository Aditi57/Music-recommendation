from flask import Flask, render_template, Response
from camera import VideoCamera, music_rec

app = Flask(__name__)

headings = ("Name", "Album", "Artist")
df1 = music_rec()
df1 = df1.head(15)

@app.route('/')
def index():
    json_data = df1.to_json(orient='records', force_ascii=False).encode('utf-8')  # Encode to UTF-8
    return render_template('index.html', headings=headings, data=json_data.decode('utf-8'))  # Decode back to string

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
