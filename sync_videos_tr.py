import ConfigParser, datetime, os, subprocess, sys, tr_definitions, shutil, glob
"""
step 1: Read config.ini. Syncpoints has attributes of sycvideos of config.ini(Type is dictionary).
step 2: Distinguish syncpoints element. There is 4 ways to distinguish.
step 2-1 : if attribute[0] is 1,2,3 than it means camID and attribute[1] is timestamps.
step 2-2 : if attribute[0] is 'refID' than attribute[1] is camID to syc.?
step 2-3 : if attribute[0] is 'begin' than attribute[1] is camID to begin frame.?
step 2-4 : if attribute[0] is 'begin' than attribute[1] is camID to end frame.?
step 3 : if there is any parameter program run with, the parameter(tosync) is used to step 10.
step 4 : WHAT'S THE NOTATION_TO_MS? There is no definition.
"""
def main():
    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)
    
    syncpoints = config.items("syncvideos")
    camID = []
    timestamps = []
    for s in syncpoints:
        if s[0].isdigit():
            camID.append(s[0])
            timestamps.append(s[1])
        elif s[0] == "refid": # ConfigParser makes everything lower-case
            synccamID = s[1]
        elif s[0] == "begin":
            sync_begin = s[1]
        elif s[0] == "end":
            sync_end = s[1]
            
    if len(sys.argv) > 1:
        tosync = sys.argv[1:]
    else:
        tosync = camID
    
    syncidx = camID.index(synccamID)
    timestamps = [tr_definitions.notation_to_ms(x) for x in timestamps]
    sync_begin = tr_definitions.notation_to_ms(sync_begin)
    sync_end = tr_definitions.notation_to_ms(sync_end)
    
    print("camID", camID)
    print("synccamID", synccamID)
    print("sync_begin", sync_begin)
    print("sync_end", sync_end)
    
    syncoffsets = [x-timestamps[syncidx] for x in timestamps]
    print("syncoffsets", syncoffsets)
    syncduration_str = "%0.3f" % (sync_end - sync_begin)
    print("syncduration_str", syncduration_str)
    
    outdirvideo = "sync"

    tr_definitions.make_folder_bak(outdirvideo)
  
    for i in range(0, len(camID)):
    
        videonames = glob.glob('*cam%02d*.*' % int(camID[i]))
        subcommand = ""
        if len(videonames) > 0 and camID[i] in tosync:
            videoname = videonames[0] # grab first video in the list
            videonameparts = videoname.split('.')
            outputvideoname = videonameparts[0] + '.MOV'
            sync_starttime = sync_begin + syncoffsets[i]
            sync_starttime_str = "%0.3f" % sync_starttime
            
            subcommand = ' -t ' + syncduration_str + ' -vcodec mpeg4 -qscale:v 2 -r 30 -acodec aac -b:a 128k -f mov ' + outdirvideo + '\\' + outputvideoname
            command = 'ffmpeg -ss ' + sync_starttime_str + ' -i ' + videoname + subcommand  

            print(command)
            subprocess.call(command.split(' '))
            
    shutil.copy(tr_definitions.config_name, outdirvideo)
            
            
if __name__ == "__main__":
    main()