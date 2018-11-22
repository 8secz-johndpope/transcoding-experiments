import sys
import os

import ffmpeg_commands as ffmpeg
from bisect import bisect_left


######################################
## https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before

######################################
##
def create_splitted_filename( src_file, start_time, end_time ):

    [ _, filename ] = os.path.split( src_file )
    [ basename, extension ] = os.path.splitext( filename )

    return basename + "_{}-{}".format( start_time, end_time ) + extension


######################################
##
def split_video( input_file, output_dir, num_splits, video_len ):

    results = []

    split_len = video_len / num_splits

    for split in range( 0, num_splits ):

        start_time = split * split_len
        end_time = ( split + 1 ) * split_len

        file_name = create_splitted_filename( input_file, start_time, end_time )
        output_file = os.path.join( output_dir, file_name )

        ffmpeg.extract_video_part( input_file, output_file, start_time, end_time )

        results.append( output_file )

    return results


######################################
##
def split_video_by_keyframes( input_file, output_dir, num_splits, video_len ):

    keyframes = ffmpeg.list_keyframes( input_file, output_dir )

    results = []
    split_points = []

    split_len = video_len / num_splits
    prev_end_time = 0.0

    for split in range( 0, num_splits ):

        start_time = prev_end_time
        end_time = ( split + 1 ) * split_len

        # Take closest keyframe if it's not last split.
        if split == num_splits - 1:
            end_time = video_len
        else:
            end_time = take_closest( keyframes, end_time )

        # end_time from this iteration will be start_time from next iteration.
        # Move timestamp one frame forward. Otherwise ffmpeg will include video
        # from last keyframe.
        # TODO: Find way to compute magic number 0.1 depending on video frame rate.
        prev_end_time = end_time# + 0.1

        file_name = create_splitted_filename( input_file, start_time, end_time )
        output_file = os.path.join( output_dir, file_name )

        ffmpeg.extract_video_part( input_file, output_file, start_time, end_time )

        results.append( output_file )
        split_points.append( end_time )

    return results, split_points

######################################
##
def split_video_ffmpeg_function( input_file, output_dir, split_len ):

    [ _, filename ] = os.path.split( input_file )
    [basename, _] = os.path.splitext( filename )
    
    output_list_file = os.path.join( output_dir, basename + ".m3u8" )
    
    split_list_file = ffmpeg.split_video( input_file, output_list_file, split_len )

    return split_list_file



######################################
##
def run():

    file_name = sys.argv[ 1 ]
    output_dir = sys.argv[ 2 ]
    num_splits = int( sys.argv[ 3 ] )
    video_len = float( sys.argv[ 4 ] )       # We should read this from file

    results = split_video( file_name, output_dir, num_splits, video_len )
    print( results )



if __name__ == "__main__":
    run()
