class Exercise: 
    def __init__(self, name, anchors, startEndAngles, reps, reduceTop, startInverted, poseType):
        self.name = name
        self.anchors = anchors
        self.startEndAngles = startEndAngles
        self.poseType = poseType
        self.reps = reps
        self.reduceTop = reduceTop
        self.startInverted = startInverted
        self.sets = 4