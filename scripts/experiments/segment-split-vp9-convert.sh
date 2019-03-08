#!/bin/bash -e

source functions/all.sh

num_segments="$1"
video_file="$2"
output_dir="$3"

experiment_name="$(basename_without_extension "${BASH_SOURCE[0]}")"
experiment_dir="$output_dir/$experiment_name/$(basename "$video_file")"

init_experiment_dir       "$experiment_dir" "$video_file" mkv
split_input               "$experiment_dir" "split_with_ffmpeg_segment $num_segments"
transcode_input           "$experiment_dir" "ffmpeg_transcode_with_codec vp9"
transcode_segments        "$experiment_dir" "ffmpeg_transcode_with_codec vp9"
merge_transcoded_segments "$experiment_dir" "merge_with_ffmpeg_concat_demuxer"

dump_frame_types_for_experiment "$experiment_dir"
