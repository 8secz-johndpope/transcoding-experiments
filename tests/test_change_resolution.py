import sys
sys.path.append("test_pipeline/")

import os

import pytest
import pipeline as pipeline
import test_utils as utils


def run_test_changing_resolution(video, parts, resolution, codec ):

    file_to_transcode = video

    task_def = utils.create_resolution_change_params( file_to_transcode, parts, resolution, codec )
    tests_dir = utils.build_test_directory_path( file_to_transcode, "change-resolution" )

    pipeline.run_pipeline(task_def, tests_dir, utils.DOCKER_IMAGE)
    
    # This intentionally won't happen if tests fails. User can check content of test directory.
    pipeline.clean_step(tests_dir)  


@pytest.mark.parametrize("videofile,num_parts,resolution, codec", [
    ("tests/videos/different-codecs/big-bunny-[codec=flv1].flv", 3, [400, 400], "flv1"),
    ("tests/videos/different-codecs/big-buck-bunny-[codec=theora].ogv", 3, [320, 180], "theora"),
    ("tests/videos/different-codecs/carphone_qcif-[codec=rawvideo].y4m", 3, [1760, 1440], "rawvideo"),
    ("tests/videos/different-codecs/Dance-[codec=mpeg2video].mpeg", 3, [160, 120], "mpeg2video"),
    ("tests/videos/different-codecs/ForBiggerBlazes-[codec=h264].mp4", 3, [128, 72], "h264"),
    ("tests/videos/different-codecs/ForBiggerMeltdowns-[codec=mpeg4].mp4", 3, [400, 400], "mpeg4"),
    ("tests/videos/different-codecs/Panasonic-[codec=vp9].webm", 3, [1280, 720], "vp9"),
    ("tests/videos/different-codecs/star_trails-[codec=wmv2].wmv", 3, [400, 400], "wmv2"),
    ("tests/videos/different-codecs/TRA3106-[codec=h263].3gp", 3, [400, 400], "h263"),
])
def test_changing_resolution(videofile, num_parts, resolution, codec):
    run_test_changing_resolution( videofile, num_parts, resolution, codec)
