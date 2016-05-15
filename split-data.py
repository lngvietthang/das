import argparse
import os
from random import shuffle
from shutil import copyfile

from utils import getFilenames, ProgressBar

def main():
    # TODO: Parse the list of arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-indir', required=True, type=str)
    parser.add_argument('-outdir', required=True, type=str)
    args = parser.parse_args()

    path2InDir = args.indir
    path2OutDir = args.outdir

    path2TrainDir = os.path.join(path2OutDir, 'training')
    path2DevDir = os.path.join(path2OutDir, 'dev')
    path2TestDir = os.path.join(path2OutDir, 'test')

    if not os.path.exists(path2OutDir):
        os.mkdir(path2OutDir)
    if not os.path.exists(path2TrainDir):
        os.mkdir(path2TrainDir)
    if not os.path.exists(path2DevDir):
        os.mkdir(path2DevDir)
    if not os.path.exists(path2TestDir):
        os.mkdir(path2TestDir)

    lstFiles = getFilenames(path2InDir)

    shuffle(lstFiles)

    trainingRatio = 0.8
    devRatio = 0.1

    nbDoc = len(lstFiles)

    nbInsTrain = int(round(nbDoc * trainingRatio, 0))
    if nbInsTrain < nbDoc * trainingRatio:
        nbInsTrain += 1

    nbInsDev = int(round(nbDoc * devRatio, 0))
    if nbInsDev < nbDoc * devRatio:
        nbInsDev += 1

    lstFilesTrain = lstFiles[:nbInsTrain]
    lstFilesDev = lstFiles[nbInsTrain: nbInsTrain + nbInsDev]
    lstFilesTest = lstFiles[nbInsTrain+nbInsDev:]

    assert len(lstFilesTrain) + len(lstFilesDev) + len(lstFilesTest) == nbDoc, \
        "Total documents in training, dev, test set are not matched with the original dataset!"

    print "Copy files in to Training Directory..."
    progress_bar = ProgressBar(len(lstFilesTrain))
    for filename in lstFilesTrain:
        copyfile(os.path.join(path2InDir, filename), os.path.join(path2TrainDir, filename))
        progress_bar.Increment()

    print "Copy files in to Dev Directory..."
    progress_bar = ProgressBar(len(lstFilesDev))
    for filename in lstFilesDev:
        copyfile(os.path.join(path2InDir, filename), os.path.join(path2DevDir, filename))
        progress_bar.Increment()

    print "Copy files in to Test Directory..."
    progress_bar = ProgressBar(len(lstFilesTest))
    for filename in lstFilesTest:
        copyfile(os.path.join(path2InDir, filename), os.path.join(path2TestDir, filename))
        progress_bar.Increment()



if __name__ == '__main__':
    main()