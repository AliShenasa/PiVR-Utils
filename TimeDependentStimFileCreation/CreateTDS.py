# Create Time Dependent Stim file for PiVr
# Input: input file
#        Header line: FPS
#        Normal line: starttime length intensity
# Output: CSV file
#
# Assumptions: Only Channel 1 is used.

import argparse

def lineout(frame, time, c1=0, c2=0, c3=0, c4=0):
    """Create output line"""
    return "{frame},{time:.2g},{c1:.2g},{c2:.2g},{c3:.2g},{c4:.2g}\n".format(frame=frame, time=time, c1=c1, c2=c2, c3=c3, c4=c4)

def main():
    # Parse cmdline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, action='store', help='input file')
    parser.add_argument('--output', '-o', type=str, action='store', help='output file')
    args = parser.parse_args()
    infilename = args.input
    outfilename = args.output

    with open(infilename) as infile, open(outfilename, 'w') as outfile:
        # Create output header
        headers = ["","Time [s]","Channel 1","Channel 2","Channel 3","Channel 4"]
        outfile.write(",".join(headers))

        # Get fps from input file
        fps = float(infile.readline())

        # Initialize frame
        curframe = 0
        curtime = 0

        for line in infile:
            splitline = line.split()
            starttime = float(splitline[0])
            length = float(splitline[1])
            intensity = float(splitline[2])

            startframe = starttime * fps
            endframe = startframe + length*fps

            while(curframe < startframe):
                # Fill in rows before startframe with 0s
                curtime = curframe / fps
                outfile.write(lineout(curframe, curtime, 0))
                curframe += 1
            
            while(curframe <= endframe):
                # Fill in rows in segment with given intensity
                curtime = curframe / fps
                outfile.write(lineout(curframe, curtime, intensity))
                curframe += 1






if __name__ == "__main__":
    main()