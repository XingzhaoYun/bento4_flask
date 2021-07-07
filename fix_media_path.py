import sys
import os
from lxml import etree

ns = '{urn:mpeg:dash:schema:mpd:2011}'

# live_content_rep_map = {
#     'Holi_360p_25fps_h264': 'video/avc1/1',
#     'Holi_540p_25fps_h264': 'video/avc1/2',
#     'Holi_720p_25fps_h264': 'video/avc1/3',
#     'Holi_1080p_4500kbps_25fps_h264': 'video/avc1/4',
#     'Holi_1080p_6000kbps_25fps_h264': 'video/avc1/5',
#     'Holi_360p_25fps_h265': 'video/hvc1/1',
#     'Holi_540p_25fps_h265': 'video/hvc1/2',
#     'Holi_720p_25fps_h265': 'video/hvc1/3',
#     'Holi_1080p_25fps_h265': 'video/hvc1/4',
#     'Holi_1440p_25fps_h265': 'video/hvc1/5',
#     'Holi_2160p_25fps_h265': 'video/hvc1/6',
#     'Holi_720p_50fps_h265': 'video/hvc1/7',
#     'Holi_1080p_50fps_h265': 'video/hvc1/8',
#     'Holi_1440p_50fps_h265': 'video/hvc1/9',
#     'Holi_2160p_50fps_h265': 'video/hvc1/10',
#     'Holi_360p_25fps_h265_str': 'video/dvh1/dvh1/1',
#     'Holi_540p_25fps_h265_str': 'video/dvh1/dvh1/2',
#     'Holi_720p_25fps_h265_str': 'video/dvh1/dvh1/3',
#     'Holi_1080p_25fps_h265_str': 'video/dvh1/dvh1/4',
#     'Holi_1440p_25fps_h265_str': 'video/dvh1/dvh1/5',
#     'Holi_2160p_25fps_h265_str': 'video/dvh1/dvh1/6',
#     'Holi_720p_50fps_h265_str': 'video/dvh1/dvh1/7',
#     'Holi_1080p_50fps_h265_str': 'video/dvh1/dvh1/8',
#     'Holi_1440p_50fps_h265_str': 'video/dvh1/dvh1/9',
#     'Holi_2160p_50fps_h265_str': 'video/dvh1/dvh1/10',
#     'Holi_en_2ch_64kbps_aac': 'audio/en/mp4a',
#     'Holi_fr_2ch_64kbps_aac': 'audio/fr/mp4a',
#     'Holi_en_2ch_128kbps_ddp': 'audio/en/ec-3/1',
#     'Holi_fr_2ch_128kbps_ddp': 'audio/fr/ec-3/1',
#     'Holi_en_6ch_256kbps_ddp': 'audio/en/ec-3/2',
#     'Holi_fr_6ch_256kbps_ddp': 'audio/fr/ec-3/2',
#     'Holi_en_6ch_640kbps_ddp_joc': 'audio/en/ec-3/3',
#     'Holi_fr_6ch_640kbps_ddp_joc': 'audio/fr/ec-3/3',
#     'Holi_en_ims_112kbps_25fps_ac4': 'audio/en/ac-4/1',
#     'Holi_fr_ims_112kbps_25fps_ac4': 'audio/fr/ac-4/1',
#     'Holi_en_6ch_128kbps_25fps_ac4': 'audio/en/ac-4/2',
#     'Holi_fr_6ch_128kbps_25fps_ac4': 'audio/fr/ac-4/2',
#     'Holi_en_514ch_192kbps_25fps_ac4': 'audio/en/ac-4/3',
#     'Holi_fr_514ch_192kbps_25fps_ac4': 'audio/fr/ac-4/3',
# }

def update_ondemand_path(manifest):
    parser = etree.XMLParser(ns_clean=True)
    tree = etree.parse(manifest, parser)
    xmlroot = tree.getroot()
    in_video_adaptationset = False
    in_audio_adaptationset = False
    for element in xmlroot.iter():
        if element.tag == ns + 'AdaptationSet':
            if 'video' in element.attrib['mimeType']:
                in_video_adaptationset = True
                in_audio_adaptationset = False
            elif 'audio' in element.attrib['mimeType']:
                in_video_adaptationset = False
                in_audio_adaptationset = True

        if in_video_adaptationset == True:
            if element.tag == ns + 'Initialization':
                element.attrib['sourceURL'] = '../../content/DASH/OnDemand/Video/' + element.attrib['sourceURL']
            elif element.tag == ns + 'SegmentURL':
                element.attrib['media'] = '../../content/DASH/OnDemand/Video/' + element.attrib['media']

        if in_audio_adaptationset == True:
            if element.tag == ns + 'Initialization':
                element.attrib['sourceURL'] = '../../content/DASH/OnDemand/Audio/' + element.attrib['sourceURL']
            elif element.tag == ns + 'SegmentURL':
                element.attrib['media'] = '../../content/DASH/OnDemand/Audio/' + element.attrib['media']
    tree.write(manifest, xml_declaration=True)


def update_live_path(manifest, input_list):
    parser = etree.XMLParser(ns_clean=True)
    tree = etree.parse(manifest, parser)
    xmlroot = tree.getroot()
    in_video_adaptationset = False
    in_audio_adaptationset = False
    for element in xmlroot.iter():
        if element.tag == ns + 'AdaptationSet':
            if 'video' in element.attrib['mimeType']:
                in_video_adaptationset = True
                in_audio_adaptationset = False
            elif 'audio' in element.attrib['mimeType']:
                in_video_adaptationset = False
                in_audio_adaptationset = True

        if in_video_adaptationset == True:
            if element.tag == ns + 'SegmentTemplate':
                element.attrib['initialization'] = '../../content/dash_live/video/' + element.attrib['initialization']
                element.attrib['media'] = '../../content/dash_live/video/' + element.attrib['media']
            if element.tag == ns + 'Representation':
                rep_id = element.attrib['id']
                if 'video/avc1' in rep_id:
                    if element.attrib['height'] == '360':
                        element.attrib['id'] = 'video/avc1/1'
                    elif element.attrib['height'] == '540':
                        element.attrib['id'] = 'video/avc1/2'
                    elif element.attrib['height'] == '720':
                        element.attrib['id'] = 'video/avc1/3'
                    elif element.attrib['height'] == '1080':
                        if int(element.attrib['bandwidth']) > int('5200000'):
                            element.attrib['id'] = 'video/avc1/4'
                        else:
                            element.attrib['id'] = 'video/avc1/5'
                elif 'video/dvh1/dvh1' in rep_id:
                    if element.attrib['height'] == '360' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/dvh1/dvh1/1'
                    elif element.attrib['height'] == '540' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/dvh1/dvh1/2'
                    elif element.attrib['height'] == '720' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/dvh1/dvh1/3'
                    elif element.attrib['height'] == '1080' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/dvh1/dvh1/4'
                    elif element.attrib['height'] == '1440' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/dvh1/dvh1/5'
                    elif element.attrib['height'] == '2160' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/dvh1/dvh1/6'
                    elif element.attrib['height'] == '720' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/dvh1/dvh1/7'
                    elif element.attrib['height'] == '1080' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/dvh1/dvh1/8'
                    elif element.attrib['height'] == '1440' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/dvh1/dvh1/9'
                    elif element.attrib['height'] == '2160' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/dvh1/dvh1/10'
                elif 'video/dvh1' in rep_id:
                    if element.attrib['height'] == '360' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/hvc1/1'
                    elif element.attrib['height'] == '540' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/hvc1/2'
                    elif element.attrib['height'] == '720' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/hvc1/3'
                    elif element.attrib['height'] == '1080' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/hvc1/4'
                    elif element.attrib['height'] == '1440' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/hvc1/5'
                    elif element.attrib['height'] == '2160' and element.attrib['frameRate'] == '25':
                        element.attrib['id'] = 'video/hvc1/6'
                    elif element.attrib['height'] == '720' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/hvc1/7'
                    elif element.attrib['height'] == '1080' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/hvc1/8'
                    elif element.attrib['height'] == '1440' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/hvc1/9'
                    elif element.attrib['height'] == '2160' and element.attrib['frameRate'] == '50':
                        element.attrib['id'] = 'video/hvc1/10'

        if in_audio_adaptationset == True:
            if element.tag == ns + 'SegmentTemplate':
                element.attrib['initialization'] = '../../content/dash_live/audio/' + element.attrib['initialization']
                element.attrib['media'] = '../../content/dash_live/video/' + element.attrib['media']
            if element.tag == ns + 'Representation':
                channel = ''
                for child in element.getchildren():
                    if child.tag == ns + 'AudioChannelConfiguration':
                        channel = child.attrib['value']
                    if 'virtualized' in child.attrib['schemeIdUri']:
                        if 'en' in element.attrib['id']:
                            element.attrib['id'] = 'audio/en/ac-4/1'
                        elif 'fr' in element.attrib['id']:
                            element.attrib['id'] = 'audio/fr/ac-4/1'
                        channel = 'IMS'
                        break
                    if 'JOC' in child.attrib['value']:
                        if 'en' in element.attrib['id']:
                            element.attrib['id'] = 'audio/en/ec-3/3'
                        elif 'fr' in element.attrib['id']:
                            element.attrib['id'] = 'audio/fr/ec-3/3'
                        channel = 'JOC'
                        break
                if element.attrib['codecs'] == 'mp4a':
                    if 'en' in element.attrib['id']:
                        element.attrib['id'] = 'audio/en/mp4a'
                    elif 'fr' in element.attrib['id']:
                        element.attrib['id'] = 'audio/fr/mp4a'
                elif element.attrib['codecs'] == 'ec-3':
                    if channel == '2':
                        if 'en' in element.attrib['id']:
                            element.attrib['id'] = 'audio/en/ec-3/1'
                        elif 'fr' in element.attrib['id']:
                            element.attrib['id'] = 'audio/fr/ec-3/1'
                    elif channel == '6':
                        if 'en' in element.attrib['id']:
                            element.attrib['id'] = 'audio/en/ec-3/2'
                        elif 'fr' in element.attrib['id']:
                            element.attrib['id'] = 'audio/fr/ec-3/2'
                elif element.attrib['codecs'] == 'ac-4':
                    if channel == '6':
                        if 'en' in element.attrib['id']:
                            element.attrib['id'] = 'audio/en/ac-4/2'
                        elif 'fr' in element.attrib['id']:
                            element.attrib['id'] = 'audio/fr/ac-4/2'
                    elif channel == '16':
                        if 'en' in element.attrib['id']:
                            element.attrib['id'] = 'audio/en/ac-4/3'
                        elif 'fr' in element.attrib['id']:
                            element.attrib['id'] = 'audio/fr/ac-4/3'
    tree.write(manifest, xml_declaration=True)


