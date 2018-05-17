import sys, os, subprocess, shutil
import numpy
import itertools
"""
STEP-T0 : python pupil_lab_sync.py world.mp4 world_timestamps.npy world_out.mp4 world_timestamps.txt
STEP-T1 : python pupil_lab_sync.py eye0.mp4 eye0_timestamps.npy eye0_out.mp4 eye0_timestamps.txt
STEP-T2 : python pupil_lab_sync.py eye1.mp4 eye1_timestamps.npy eye1_out.mp4 eye1_timestamps.txt
STEP1 : python pupil_lab_sync.py eye0.mp4 eye0_timestamps.npy eye0_out.mp4 eye0_timestamps.txt &&python pupil_lab_sync.py eye1.mp4 eye1_timestamps.npy eye1_out.mp4 eye1_timestamps.txt
STEP2 : Check world_out_dir.tmp1, world_out_dir.tmp2 are exist. If no, make directory with tmp1, tmp2.
STEP3 : Save screenshots from world.mp4 in directory tmp1.
STEP4 : Read timestamp file with numpy. Rearange the data with \n and save output file.
STEP5 : Subtract first element from all of element. Frist element is standard of the timestamps.
"""
def main():
    video_filename = sys.argv[1]
    timestamps_filename = sys.argv[2]
    output_filename = sys.argv[3]
    output_timestamps_filename = sys.argv[4]
    
    frame_time = 1 / 30.0

    tmp1 = output_filename + ".tmp1"
    if not os.path.exists(tmp1):
        os.mkdir(tmp1)

    command = "ffmpeg -i " + video_filename + " -f image2 -qscale:v 2 " + tmp1 + "\%d.jpg"
    print(command)
    subprocess.call(command.split(' '))
    
    tmp2 = output_filename + ".tmp2"
    if not os.path.exists(tmp2):
        os.mkdir(tmp2)

    timestamps = numpy.fromfile(timestamps_filename, dtype='<f8')
    timestamps.tofile(output_timestamps_filename, "\n", "%s")
    index = numpy.arange(10)
    timestamps = numpy.array(list(itertools.compress(timestamps, [i not in index for i in range(len(timestamps))])))
    print("first element..",timestamps[0])
    timestamps = timestamps - timestamps[0]
    curr_time = 0.0
    curr_image = 1

    previdx = -1
    prevdest = "-1"
    while curr_time <= timestamps[-1]:
        idx = numpy.argmin(numpy.absolute(timestamps-curr_time))
        curr_time += frame_time
        if idx == previdx:
            src = prevdest
            movefile = False
        else:
            src = tmp1 + "\\" + "%d.jpg" % (idx+1)
            movefile = True
        dest = tmp2 + "\\" + "n_%d.jpg" % curr_image
        if curr_image < 10:
            print(src, dest, movefile)
        prevdest = dest;
        previdx = idx;
        curr_image += 1
        if movefile:
            shutil.move(src, dest)
        else:
            shutil.copy(src, dest)
        
    command = "ffmpeg -framerate 30 -i " + tmp2 + "\\n_%d.jpg -pix_fmt yuv420p -vcodec mpeg4 -qscale:v 2 -r 30 " + output_filename
    subprocess.call(command.split(' '))

if __name__ == "__main__":
    main()