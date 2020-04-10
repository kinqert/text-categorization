from progressbar import ProgressBar, Percentage, ETA, Bar

def defaultProgress(maxValue):
    return ProgressBar(maxValue, [Percentage(), Bar( marker='█'), ETA()])