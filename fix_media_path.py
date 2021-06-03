import sys
import os
from lxml import etree

ns = '{urn:mpeg:dash:schema:mpd:2011}'

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


def update_live_path(manifest):
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
                element.attrib['initialization'] = '../../content/DASH/Live/Video/' + element.attrib['initialization']
                element.attrib['media'] = '../../content/DASH/Live/Video/' + element.attrib['media']
            
        if in_audio_adaptationset == True:
            if element.tag == ns + 'SegmentTemplate':
                element.attrib['initialization'] = '../../content/DASH/Live/Audio/' + element.attrib['initialization']
                element.attrib['media'] = '../../content/DASH/Live/Audio/' + element.attrib['media']
    tree.write(manifest, xml_declaration=True)


