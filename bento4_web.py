from flask import Flask, render_template, url_for, request, redirect, send_file
import subprocess
import os
app = Flask(__name__)

# media_tracks = {
#     'videos': {
#         'AVC': [
#         'Holi_360p_25fps_h264.h264',
#         'Holi_540p_25fps_h264.h264',
#         'Holi_720p_25fps_h264.h264',
#         'Holi_1080p_4500kbps_25fps_h264.h264',
#         'Holi_1080p_6000kbps_25fps_h264.h264'
#         ],
#         'HEVC': [
#         'Holi_360p_25fps_h265.h265',
#         'Holi_540p_25fps_h265.h265',
#         'Holi_720p_25fps_h265.h265',
#         'Holi_1080p_25fps_h265.h265',
#         'Holi_1440p_25fps_h265.h265',
#         'Holi_2160p_25fps_h265.h265',
#         'Holi_720p_50fps_h265.h265',
#         'Holi_1080p_50fps_h265.h265',
#         'Holi_1440p_50fps_h265.h265',
#         'Holi_2160p_50fps_h265.h265'
#         ],
#         'Dolby Vision': [
#         'Holi_360p_25fps_h265_str.h265',
#         'Holi_540p_25fps_h265_str.h265',
#         'Holi_720p_25fps_h265_str.h265',
#         'Holi_1080p_25fps_h265_str.h265',
#         'Holi_1440p_25fps_h265_str.h265',
#         'Holi_2160p_25fps_h265_str.h265',
#         'Holi_720p_50fps_h265_str.h265',
#         'Holi_1080p_50fps_h265_str.h265',
#         'Holi_1440p_50fps_h265_str.h265',
#         'Holi_2160p_50fps_h265_str.h265'
#         ]
#     },
#     'audios': {
#         'AAC': [
#         'Holi_en_2ch_64kbps_aac.aac',
#         'Holi_fr_2ch_64kbps_aac.aac'
#         ],
#         'DDP-2ch': [
#         'Holi_en_2ch_128kbps_ddp.ec3',
#         'Holi_fr_2ch_128kbps_ddp.ec3'
#         ],
#         'DDP-6ch': [
#         'Holi_en_6ch_256kbps_ddp.ec3',
#         'Holi_fr_6ch_256kbps_ddp.ec3',
#         ],
#         'DDP-JOC': [
#         'Holi_en_6ch_640kbps_ddp_joc.ec3',
#         'Holi_fr_6ch_640kbps_ddp_joc.ec3'
#         ],
#         'AC4-IMS': [
#         'Holi_en_ims_112kbps_25fps_ac4.ac4',
#         'Holi_fr_ims_112kbps_25fps_ac4.ac4',
#         ],
#         'AC4-6ch': [
#         'Holi_en_6ch_128kbps_25fps_ac4.ac4',
#         'Holi_fr_6ch_128kbps_25fps_ac4.ac4',
#         ],
#         'AC4-514ch': [
#         'Holi_en_514ch_192kbps_25fps_ac4.ac4',
#         'Holi_fr_514ch_192kbps_25fps_ac4.ac4'
#         ]
#     }
# }

@app.route('/return-manifest-live/')
def return_files_live():
    try:
        return send_file('/Users/xyun/Documents/Online/online_bento4/output/output_live/live.mpd', mimetype='text/mpd',as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/return-manifest-vod/')
def return_files_vod():
    try:
        return send_file('/Users/xyun/Documents/Online/online_bento4/output/output_vod/ondemand.mpd', mimetype='text/mpd', as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/', methods=['GET', 'POST'])
@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == "POST":
        video_tracks = request.form.getlist("video_track")
        v_set = [('es/video/'+video_track).replace('.h264', '_f_dash.mp4').replace('.h265', '_f_dash.mp4') for video_track in video_tracks]
        video_args = ' '.join(v_set)

        audio_tracks = request.form.getlist("audio_track")
        a_set = [('es/audio/'+ audio_track).replace('.aac', '_f_dash.mp4'). \
                replace('.ac3', '_f_dash.mp4').replace('.ec3', '_f_dash.mp4').replace('.ac4', '_f_dash.mp4') for audio_track in audio_tracks]
        audio_args = ' '.join(a_set)

        # subprocess.call("python " + "utils/mp4-dash.py", shell=True)
        subprocess.call('python bento4/utils/mp4-dash.py -f -o output/output_vod --no-media --mpd-name ' \
            'ondemand.mpd --language-map English:eng,French:fra --profiles ondemand --no-split ' + video_args + ' ' + audio_args, shell=True)
        subprocess.call('python bento4/utils/mp4-dash.py -f -o output/output_live --no-media --mpd-name ' \
            'live.mpd --language-map English:eng,French:fra --profiles live --use-segment-template-number-padding --use-segment-timeline ' \
            + video_args + ' ' + audio_args, shell=True)
        print(video_args)
        print(audio_args)
        with open("output/output_live/live.mpd", "r") as live_file:
            live_content = live_file.read()
        with open("output/output_vod/ondemand.mpd", "r") as vod_file:
            vod_content = vod_file.read()
        profile = request.form.get("profile", None)
        if profile!=None:
            return render_template("downloads.html", live_content = live_content, vod_content = vod_content)
    return render_template("config.html")


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80)




