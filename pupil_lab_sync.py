import sys, os, subprocess, shutil
from natsort import natsorted
import numpy
import itertools
"""
STEP-T0 : python pupil_lab_sync.py world world_timestamps 1 1
STEP-T1 : python pupil_lab_sync.py eye0 eye0_timestamps 1 1 
STEP-T2 : python pupil_lab_sync.py eye1 eye1_timestamps 1 1

STEP1 : Command above 3 of one. python pupil_lab_sync.py eye0 eye0_timestamps 1 1; python pupil_lab_sync.py eye1 eye1_timestamps 1 1
STEP2 : Check world_out_dir.tmp1, world_out_dir.tmp2 are exist. If no, make directory with tmp1, tmp2.
STEP3 : Save screenshots from world.mp4 in directory tmp1.
STEP4 : Read timestamp file with numpy. Rearange the data with \n and save output file.
STEP5 : Subtract first element from all of element. Frist element is standard of the timestamps.
STEP6 : Move file to tmp2 from tmp1 at first. Then copy file till next timestamp comes.
STEP7 : Reconstruct tmp2 to video.
"""
def main():
	video_filename = sys.argv[1] + ".mp4"
	timestamps_filename = sys.argv[2] + ".npy"
	output_filename = sys.argv[1] + "_out.mp4"
	output_timestamps_filename = sys.argv[2] + ".txt"
	beginSec = sys.argv[3]
	endSec = sys.argv[4]
	output_filename2 = sys.argv[1] + "_out_trc.mp4"

	framerate = 30.0
	frame_time = 1 / framerate

	tmp1 = output_filename + ".tmp1"
	if not os.path.exists(tmp1):
		os.mkdir(tmp1)
	else:
		shutil.rmtree(tmp3)
	command = "ffmpeg -i " + video_filename + " -f image2 -qscale:v 2 " + tmp1 + "\%d.jpg"
	print(command)
	subprocess.call(command.split(' '))

	tmp2 = output_filename + ".tmp2"
	if not os.path.exists(tmp2):
		os.mkdir(tmp2)
	else:
		shutil.rmtree(tmp3)

	timestamps = numpy.load(timestamps_filename)
	timestamps.tofile(output_timestamps_filename, "\n", "%s")
	#index = numpy.arange(10)
	#timestamps = numpy.array(list(itertools.compress(timestamps, [i not in index for i in range(len(timestamps))])))
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
	if beginSec==0 and endSec == 0:
		return
	else:
		beginframe_toTrc = int(framerate) * int(beginSec)
		endframe_toTrc = int(framerate) * int(endSec)
		tmp2list = os.listdir(tmp2)
		tmp2list = natsorted(tmp2list)
		totalframe = int(len(tmp2list)) -1
		endframe_toTrc = totalframe - endframe_toTrc
		tmp3 = output_filename + ".tmp3"
		if not os.path.exists(tmp3):
		    os.mkdir(tmp3)
		else:
			shutil.rmtree(tmp3)

		actB = 0
		actE = 0
		destnum = 1
		for i,filestr in enumerate(tmp2list):
			if i<beginframe_toTrc:
				actB+=1
				continue
			if i>endframe_toTrc:
				actE+=1
				continue
			src = tmp2+"\\"+filestr
			dest = tmp3+"\\"+"n_%d.jpg" % destnum
			shutil.copy(src, dest)
			destnum +=1
		print("beginframe_toTrc......",beginframe_toTrc)
		print("endframe_toTrc......",endframe_toTrc)
		print("totalframe......",totalframe)
		print("actualB, actualE......",str(actB), str(actE))
		command = "ffmpeg -framerate 30 -i " + tmp3 + "\\n_%d.jpg -pix_fmt yuv420p -vcodec mpeg4 -qscale:v 2 -r 30 " + output_filename2
		subprocess.call(command.split(' '))

if __name__ == "__main__":
    main()
