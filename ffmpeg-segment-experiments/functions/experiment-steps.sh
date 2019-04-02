function init_experiment_dir {
    local experiment_dir="$1"
    local video_file="$2"
    local output_format="$3"

    input_format="$(get_extension "$video_file")"
    input_file="$experiment_dir/input.$input_format"

    if [[ "$output_format" == "" ]]; then
        local output_format="$input_format"
    fi

    mkdir --parents "$experiment_dir"
    cp "$video_file" "$input_file"

    printf "%s" "$input_format"             > "$experiment_dir/input-format"
    printf "%s" "$output_format"            > "$experiment_dir/output-format"
    printf "%s" "$(basename "$video_file")" > "$experiment_dir/video-name"
}


function split_input {
    local experiment_dir="$1"
    local split_command="$2"

    local input_file="$experiment_dir/input.$(cat "$experiment_dir/input-format")"

    $split_command    \
        "$input_file" \
        "$experiment_dir/split"
}


function merge_segments {
    local experiment_dir="$1"
    local merge_command="$2"

    local output_format="$(cat "$experiment_dir/output-format")"

    $merge_command              \
        "$experiment_dir/split" \
        "$experiment_dir"       \
        "$output_format"
}


function merge_transcoded_segments {
    local experiment_dir="$1"
    local merge_command="$2"

    local output_format="$(cat "$experiment_dir/output-format")"

    $merge_command                  \
        "$experiment_dir/transcode" \
        "$experiment_dir"           \
        "$output_format"
}


function transcode_input {
    local experiment_dir="$1"
    local transcode_command="$2"

    local input_file="$experiment_dir/input.$(cat "$experiment_dir/input-format")"
    local output_file="$experiment_dir/monolithic.$(cat "$experiment_dir/output-format")"

    $transcode_command \
        "$input_file"  \
        "$output_file"
}


function transcode_segments {
    local experiment_dir="$1"
    local transcode_command="$2"

    mkdir --parents "$experiment_dir/transcode"

    local output_format="$(cat "$experiment_dir/output-format")"

    rewrite_flat_file_list_with_different_format \
        "$output_format"                         \
        "$experiment_dir/split/segments.txt"     \
        "$experiment_dir/transcode/segments.txt"

    for segment_file in $(cat "$experiment_dir/split/segments.txt"); do
        local input_file="$experiment_dir/split/$segment_file"
        local output_file="$(strip_extension "$experiment_dir/transcode/$segment_file").$(cat "$experiment_dir/output-format")"

        $transcode_command \
            "$input_file"  \
            "$output_file"
    done
}


function dump_frame_types_for_experiment {
    local experiment_dir="$1"

    echo "Generating frame-type.txt files for $experiment_dir/"

    local input_file="$experiment_dir/input.$(cat "$experiment_dir/input-format")"
    local output_file="$experiment_dir/monolithic.$(cat "$experiment_dir/output-format")"
    local merged_file="$experiment_dir/merged.$(cat "$experiment_dir/output-format")"

    dump_frame_types_for_video "$input_file"
    dump_frame_types_for_video "$merged_file"

    if [ -e "$output_file" ]; then
        dump_frame_types_for_video "$output_file"
    fi

    for segment_file in $(cat "$experiment_dir/split/segments.txt"); do
        dump_frame_types_for_video "$experiment_dir/split/$segment_file"
    done

    if [ -e "$output_file" ]; then
        for segment_file in $(cat "$experiment_dir/transcode/segments.txt"); do
            dump_frame_types_for_video "$experiment_dir/transcode/$segment_file"
        done
    fi
}