import matlab.engine
import os
from subprocess import Popen, PIPE, STDOUT

class InputError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return str(self.msg)

class SemanticHyperlapse(object):
    def __init__(self):
        self.video = None
        self.path = ''
        self.extractor = ''
        self.velocity = 0
        self.maxVel = 0
        self.alpha = []
        self.beta = []
        self.gama = []
        self.eta = []

    def getVideo(self):
        return self.video

    def setVideo(self, video):
        self.video = video

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    def getExtractor(self):
        return self.extractor

    def setExtractor(self, extractor):
        self.checkExtractor(extractor)
        self.extractor = extractor

    def getVelocity(self):
        return self.velocity

    def setVelocity(self, velocity):
        try:
            self.checkVelocity(velocity)
            self.velocity = float(int(velocity))
        except ValueError:
            raise InputError('Invalid speedup value')
            
    def getMaxVel(self):
        return self.maxVel

    def setMaxVel(self, maxVel):
        self.maxVel = maxVel

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, alpha):
        self.alpha = self.checkAndSetWeights(alpha)
        
    def getBeta(self):
        return self.beta

    def setBeta(self, beta):
        self.beta = self.checkAndSetWeights(beta)

    def getGama(self):
        return self.gama

    def setGama(self, gama):
        self.gama = self.checkAndSetWeights(gama)

    def getEta(self):
        return self.eta

    def setEta(self, eta):
        self.eta = self.checkAndSetWeights(eta)

    def setPaths(self):
        self.setPath(os.getcwd()) #get project path 
        self.video.setPaths()

    def checkExtractor(self, extractor):
        if self.isEmpty(extractor):
            raise InputError('Please select an extractor')

    def checkVelocity(self, velocity):
        if self.isEmpty(velocity):
            raise InputError('Please insert speedup')

        velocity = int(velocity) #raises ValueError if it isn't a number
        if velocity <= 1:
            raise InputError('Error: speedup <= 1')
    
    def checkVideoInput(self):
        if self.getVideo().isEmpty():
            raise InputError('Please insert input video first')

        if self.getVideo().isInvalid():
            raise InputError('Video format invalid.\nValid formats: mp4, avi')

    def checkAndSetWeights(self, weights):
        try:
            return self.convertWeights(weights)
        except ValueError:
            raise InputError('Please fill correctly all weights inputs')

    def isEmpty(self, inputText):
        if inputText == '':
            return True
        return False

    def convertWeights(self, weights):
        for i in range(len(weights)):
            weights[i] = int(weights[i])	#if it isn't a number, it'll raises a ValueError
        return weights

    def opticalFlowCommand(self):
        videoFile = self.correctPath(self.video.getVideoFile())
        command = './optflow'
        videoParam = ' -v ' + videoFile
        configParam = ' -c default-config.xml'
        outputParam = ' -o ' + videoFile[:-4] + '.csv'

        fullCommand = command + videoParam + configParam + outputParam		
        
        return fullCommand

    def runOpticalFlow(self): # pragma: no cover
        os.chdir('../Vid2OpticalFlowCSV')

        os.system(self.opticalFlowCommand())
        
        os.chdir(self.getPath())


    def runMatlabSemanticInfo(self, eng): # pragma: no cover
        videoFile = self.video.getVideoFile()
        extractionFile = videoFile[:-4] + '_face_extracted.mat'
        extractor = self.extractor

        eng.ExtractAndSave(videoFile, extractor, nargout=0)
        (aux, nonSemanticFrames, semanticFrames) = eng.GetSemanticRanges(extractionFile, nargout=3)

        return (float(nonSemanticFrames), float(semanticFrames))

    def getSemanticInfo(self, eng): # pragma: no cover
        eng.cd('SemanticScripts')
        eng.addpath(self.video.getVideoPath())
        eng.addpath(os.getcwd())
        
        nonSemanticFrames, semanticFrames = self.runMatlabSemanticInfo(eng)
        
        eng.cd(self.getPath())
        return (nonSemanticFrames, semanticFrames)

    def speedUp(self, eng, nonSemanticFrames, semanticFrames): # pragma: no cover
        eng.addpath(os.getcwd())
        eng.addpath('Util')
    
        alpha = matlab.double([self.getAlpha()])
        beta = matlab.double([self.getBeta()])
        gama = matlab.double([self.getGama()])
        eta = matlab.double([self.getEta()])

        velocity = self.getVelocity()
        video = self.getVideo()
    
        (ss, sns) = eng.FindingBestSpeedups(nonSemanticFrames, semanticFrames,
                                            velocity, True, nargout=2)
            
        eng.SpeedupVideo(
            video.getVideoPath(), video.getVideoName(), self.getExtractor(),
            ss, sns, alpha, beta, gama, eta, 'Speedup', velocity, nargout=0
        )

    def setup(self, inputSpeedUp, extractor, alphaInput, betaInput, gamaInput, etaInput):	
        self.checkVideoInput()
        
        self.setExtractor(extractor)

        self.setVelocity(inputSpeedUp)
        self.setMaxVel(self.getVelocity() * 10.0)

        self.setAlpha(alphaInput)
        self.setBeta(betaInput)
        self.setGama(gamaInput)
        self.setEta(etaInput)

    def run(self, writeFunction): # pragma: no cover
        function = writeFunction
        
        function('1/5 - Running Optical Flow\n', 'title')
        self.runOpticalFlow()
    
        function('2/5 - Starting Matlab\n', 'title')
        eng = matlab.engine.start_matlab('-nodisplay')
    
        function('3/5 - Getting Semantic Info\n', 'title')
        (nonSemanticFrames, semanticFrames) = self.getSemanticInfo(eng)

        function('4/5 - Speeding-Up Video\n', 'title')
        self.speedUp(eng, nonSemanticFrames, semanticFrames)
        eng.quit()
    
        function('5/5 - Finished\n', 'title')

    def correctPath(self, path):
        splittedPath = path.split(' ')
        finalPath = ''
        for i in splittedPath:
            finalPath += (i + '\ ')
        return finalPath[:-2]
