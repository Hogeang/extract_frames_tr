 
import numpy

worldfilename = "world_timestamps"
eye0filename = "eye0_timestamps"
eye1filename = "eye1_timestamps"
def main():
	timestamps = numpy.fromfile(worldfilename+".npy", dtype='<f8')
	timestamps.tofile(worldfilename+".txt", "\n", "%s")

	timestamps = numpy.fromfile(eye0filename+".npy", dtype='<f8')
	timestamps.tofile(eye0filename+".txt", "\n", "%s")

	timestamps = numpy.fromfile(eye1filename+".npy", dtype='<f8')
	timestamps.tofile(eye1filename+".txt", "\n", "%s")

if __name__ == "__main__":
    main()