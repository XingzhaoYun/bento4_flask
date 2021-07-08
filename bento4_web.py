from flask import Flask, render_template, url_for, request, redirect, send_file
import subprocess
import logging
import os
from datetime import datetime
from fix_media_path import update_live_path, update_ondemand_path

app = Flask(__name__)

media_tracks = {
    'video': {
        'AVC': {
            '25fps' :[
                'Holi_360p_25fps_h264.h264',
                'Holi_540p_25fps_h264.h264',
                'Holi_720p_25fps_h264.h264',
                'Holi_1080p_4500kbps_25fps_h264.h264',
                'Holi_1080p_6000kbps_25fps_h264.h264'
            ]
        },
        'HEVC': {
            '25fps': [
                'Holi_360p_25fps_h265.h265',
                'Holi_540p_25fps_h265.h265',
                'Holi_720p_25fps_h265.h265',
                'Holi_1080p_25fps_h265.h265',
                'Holi_1440p_25fps_h265.h265',
                'Holi_2160p_25fps_h265.h265'
            ],
            '50fps': [
                'Holi_720p_50fps_h265.h265',
                'Holi_1080p_50fps_h265.h265',
                'Holi_1440p_50fps_h265.h265',
                'Holi_2160p_50fps_h265.h265'
            ]
        },
        'DolbyVision': {
            '25fps': [
                'Holi_360p_25fps_h265_str.h265',
                'Holi_540p_25fps_h265_str.h265',
                'Holi_720p_25fps_h265_str.h265',
                'Holi_1080p_25fps_h265_str.h265',
                'Holi_1440p_25fps_h265_str.h265',
                'Holi_2160p_25fps_h265_str.h265'
            ],
            '50fps': [
                'Holi_720p_50fps_h265_str.h265',
                'Holi_1080p_50fps_h265_str.h265',
                'Holi_1440p_50fps_h265_str.h265',
                'Holi_2160p_50fps_h265_str.h265'
            ]
        }
    },
    'audio': {
        'AAC': {
            'NA' : [
                'Holi_en_2ch_64kbps_aac.aac',
                'Holi_fr_2ch_64kbps_aac.aac'
            ]
        },
        'DDP-2ch': {
            'NA' : [
                'Holi_en_2ch_128kbps_ddp.ec3',
                'Holi_fr_2ch_128kbps_ddp.ec3'
            ]
        },
        'DDP-6ch': {
            'NA' : [
                'Holi_en_6ch_256kbps_ddp.ec3',
                'Holi_fr_6ch_256kbps_ddp.ec3',
            ]
        },
        'DDP-JOC': {
            'NA' : [
                'Holi_en_6ch_640kbps_ddp_joc.ec3',
                'Holi_fr_6ch_640kbps_ddp_joc.ec3'
            ]
        },
        'AC4-IMS': {
            '25fps': [
                'Holi_en_ims_112kbps_25fps_ac4.ac4',
                'Holi_fr_ims_112kbps_25fps_ac4.ac4'
            ]
        },
        'AC4-6ch': {
            '25fps':[
                'Holi_en_6ch_128kbps_25fps_ac4.ac4',
                'Holi_fr_6ch_128kbps_25fps_ac4.ac4'
            ]
        },
        'AC4-514ch': {
            '25fps': [
                'Holi_en_514ch_192kbps_25fps_ac4.ac4',
                'Holi_fr_514ch_192kbps_25fps_ac4.ac4'
            ]
        }
    }
}


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
        if request.form.get('action') == 'Submit':
            input_list = request.form.getlist("selected_track")
            print(input_list)

            timestamp = datetime.now().strftime('%Y_%b_%d_%H_%M_%S')
            request_ip = request.remote_addr
            global vod_manifest_filename, live_manifest_filename
            vod_manifest_filename  = request_ip.replace('.','_',3) + '_' + timestamp + '_ondemand.mpd'
            live_manifest_filename = request_ip.replace('.','_',3) + '_' + timestamp + '_live.mpd'

            v_set = []
            a_set = []
            for track in input_list:
                if '.h264' in track or '.h265' in track:
                    v_set.append(('frag_mp4_DASH/video/' + track).replace('.h264', '.mp4').replace('.h265', '.mp4'))
                    print(v_set)
                elif '.aac' in track or '.ac3' in track or '.ec3' in track or '.ac4' in track:
                    a_set.append(('frag_mp4_DASH/audio/'+ track).replace('.aac', '.mp4'). \
                    replace('.ac3', '.mp4').replace('.ec3', '.mp4').replace('.ac4', '.mp4'))
                    print(a_set)
            video_args = ' '.join(v_set)
            audio_args = ' '.join(a_set)
            print(video_args)
            print(audio_args)

            if not v_set and not a_set:
                return render_template("config.html", media_tracks = media_tracks)
            # subprocess.call("python " + "utils/mp4-dash.py", shell=True)
            subprocess.call('python bento4/utils/mp4-dash.py -f -o output --no-media --mpd-name ' \
                + vod_manifest_filename + ' --language-map English:eng,French:fra --profiles on-demand --no-split ' + video_args + ' ' + audio_args, shell=True)

            subprocess.call('python bento4/utils/mp4-dash.py -f -o output --no-media --mpd-name ' \
                + live_manifest_filename + ' --language-map English:eng,French:fra --profiles live --use-segment-template-number-padding --use-segment-timeline ' \
                + video_args + ' ' + audio_args, shell=True)

            update_ondemand_path("output/" + vod_manifest_filename)
            update_live_path("output/" + live_manifest_filename)

            with open("output/" + live_manifest_filename, "r") as live_file:
                live_content = live_file.read()
            with open("output/" + vod_manifest_filename, "r") as vod_file:
                vod_content = vod_file.read()
            return render_template("downloads.html", live_content = live_content, live_manifest_filename = live_manifest_filename, \
                vod_content = vod_content, vod_manifest_filename = vod_manifest_filename)
        elif request.form.get('action') == 'Reset':
            return render_template("config.html", media_tracks = media_tracks)
    return render_template("config.html", media_tracks = media_tracks)


if __name__ == '__main__':
    #app.run(threaded=True)
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=80, threaded=True)




