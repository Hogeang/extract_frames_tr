import ConfigParser, tr_definitions, shutil, os

synced_folder_name = 'cam%02d_video_r' # cam01_video_r
info_file_template = "#\n# File generated by build_directory.py\n#\n\n# trial info\n# trial number, onset, offset\n1,-1,-1\n\n# sensor\n# recording time\n# hour, min, sec, ms\n-1,-1,-1,-1\n\n# speech\n# recording time\n# hour, min, sec, ms, rate\n%s\n\n# video cam03\n# hour, min, sec, ms, rate\n%s"
additional_folders = ['derived', 'extra_p', 'speech_transcription_p']
#Step 1   : Read 'config.ini'.
#Step 2   : Read files in present folder.
#Step 3   : Check if pattern *cam00*.* ~ *cam99*.* is exist in folder. If it is true, operate step 3-1.
#Step 3-1 : Create the backup folder and move file into the folder with specific format(synced_folder_name). e.g. cam22_fideo_r_bak2
#Step 4   : Create 3 kind of folders. e.g. "derived_bak1", "extra_p_bak6"
def main():
    config = ConfigParser.ConfigParser()
    config.read(tr_definitions.config_name)
    
    files = os.listdir('.')
    for i in range(0,100):
        check_name = 'cam%02d' % i
        for f in files:
            if check_name in f and '.' in f:
                tr_definitions.make_folder_bak(synced_folder_name % i)
                print("moving file")
                shutil.move(f, synced_folder_name % i)
                break
    
    for i in range(0,len(additional_folders)-1):
        foldername = additional_folders[i]
        tr_definitions.make_folder_bak(foldername)
        
if __name__ == "__main__":
    main()