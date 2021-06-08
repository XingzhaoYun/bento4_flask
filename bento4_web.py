from flask import Flask, render_template, url_for, request, redirect, send_file
import subprocess
import logging
import os
from datetime import datetime

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
        return send_file('/Users/xyun/Documents/Git/bento4_flask/output/' + live_manifest_filename, mimetype='text/mpd',as_attachment=True)
    except Exception as e:
        return str(e)

@app.route('/return-manifest-vod/')
def return_files_vod():
    try:
        return send_file('/Users/xyun/Documents/Git/bento4_flask/output/' + vod_manifest_filename, mimetype='text/mpd', as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/', methods=['GET', 'POST'])
@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == "POST":
        timestamp = datetime.now().strftime('%Y_%b_%d_%H_%M_%S')
        request_ip = request.remote_addr
        print(timestamp)
        print(request_ip)
        global vod_manifest_filename, live_manifest_filename
        vod_manifest_filename  = request_ip.replace('.','_',3) + '_' + timestamp + '_ondemand.mpd'
        live_manifest_filename = request_ip.replace('.','_',3) + '_' + timestamp + '_live.mpd'
        print(vod_manifest_filename)
        print(live_manifest_filename)
        video_tracks = request.form.getlist("video_track")
        v_set = [('frag_mp4_DASH/video/'+video_track).replace('.h264', '_f_dash.mp4').replace('.h265', '_f_dash.mp4') for video_track in video_tracks]
        video_args = ' '.join(v_set)

        audio_tracks = request.form.getlist("audio_track")
        a_set = [('frag_mp4_DASH/audio/'+ audio_track).replace('.aac', '_f_dash.mp4'). \
                replace('.ac3', '_f_dash.mp4').replace('.ec3', '_f_dash.mp4').replace('.ac4', '_f_dash.mp4') for audio_track in audio_tracks]
        audio_args = ' '.join(a_set)

        # subprocess.call("python " + "utils/mp4-dash.py", shell=True)
        subprocess.call('python bento4/utils/mp4-dash.py -f -o output --no-media --mpd-name ' \
            + vod_manifest_filename + ' --language-map English:eng,French:fra --profiles on-demand --no-split ' + video_args + ' ' + audio_args, shell=True)

        subprocess.call('python bento4/utils/mp4-dash.py -f -o output --no-media --mpd-name ' \
            + live_manifest_filename + ' --language-map English:eng,French:fra --profiles live --use-segment-template-number-padding --use-segment-timeline ' \
            + video_args + ' ' + audio_args, shell=True)
        print(video_args)
        print(audio_args)
        with open("output/" + live_manifest_filename, "r") as live_file:
            live_content = live_file.read()
        with open("output/" + vod_manifest_filename, "r") as vod_file:
            vod_content = vod_file.read()
        profile = request.form.get("profile", None)
        if profile!=None:
            return render_template("downloads.html", live_content = live_content, live_manifest_filename = live_manifest_filename, \
                vod_content = vod_content, vod_manifest_filename = vod_manifest_filename)
    return render_template("config.html")


if __name__ == '__main__':
    #app.run(threaded=True)
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80, threaded=True)




