import numpy as np
import pandas as pd
from .ColMapper import ColMapper
from .TrajectoryProcessor import TrajectoryProcessor

class TrajectoryCleaner(TrajectoryProcessor):

    def __init__(self,
            colMapper: ColMapper,
            minSpeed,
            maxSpeed,
            minYDisplacement,
            maxXDisplacement,
            minAcceleration,
            maxAcceleration,
        ):
        
        super().__init__(colMapper)
        self.minSpeed = minSpeed
        self.maxSpeed = maxSpeed
        self.minYDisplacement = minYDisplacement
        self.maxXDisplacement = maxXDisplacement
        self.maxAcceleration = maxAcceleration
        self.minAcceleration = minAcceleration


        pass

    #region outliers
    

    def getOutliersByCol(self,    #dekhi nai
            summary: pd.DataFrame,
            col: str,
            byIQR=False,
            returnVals=False
        ) -> pd.Series:

        if byIQR:
            Q3 = np.quantile(summary[col], 0.75)
            Q1 = np.quantile(summary[col], 0.25)
            IQR = Q3 - Q1
            lowerBoundary = Q1 - 1.5 * IQR
            higherBoundary = Q3 + 1.5 * IQR

            print("IQR value for column %s is: %s" % (col, IQR))
            print(f"using range ({lowerBoundary}, {higherBoundary})")
            

        else:
            raise NotImplementedError("Not implemented non IQR yet")


        criterion = summary[col].map(
            lambda val: val < lowerBoundary or val > higherBoundary)

        outliers = summary[criterion]

        if returnVals:
            return outliers
        else:
            return outliers.index
    

    def getMinOutliersByCol(self, 
            tracksDf:pd.DataFrame, 
            col: str,
            byIQR=False,
            returnVals=False
        ) -> pd.Series:


        mainVals = tracksDf[[self.idCol, col]].groupby([self.idCol]).min()

        return self.getOutliersByCol(summary=mainVals, col=col, byIQR=byIQR, returnVals=returnVals)


    def getMaxOutliersByCol(self, 
            tracksDf:pd.DataFrame, 
            col: str,
            byIQR=False,
            returnVals=False
        ) -> pd.Series:


        maxVals = tracksDf[[self.idCol, col]].groupby([self.idCol]).max()

        return self.getOutliersByCol(summary=maxVals, col=col, byIQR=byIQR, returnVals=returnVals)


    def getOutliersBySpeed(self,
            tracksDf:pd.DataFrame, 
            byIQR=False,
            returnVals=False
        ) -> pd.Series:


        if byIQR:
            return self.getMaxOutliersByCol(
                tracksDf,
                self.speedCol,
                byIQR=byIQR,
                returnVals=returnVals
            )
            

        else:
            print(f"using range ({self.minSpeed}, {self.maxSpeed})")
            maxVals = tracksDf[[self.idCol, self.speedCol]].groupby([self.idCol]).max()
            criterion = maxVals[self.speedCol].map(
                lambda val: val < self.minSpeed or val > self.maxSpeed)

            outliers = maxVals[criterion]

            if returnVals:
                return outliers
            else:
                return outliers.index

    def getOutliersByAcceleration(self,
            tracksDf:pd.DataFrame, 
            byIQR=False,
            returnVals=False
        ) -> pd.Series:


        if byIQR:
            return self.getMaxOutliersByCol(
                tracksDf,
                self.accelerationCol,
                byIQR=byIQR,
                returnVals=returnVals
            )
            

        else:
            print(f"using range ({self.minAcceleration}, {self.maxAcceleration})")
            maxVals = tracksDf[[self.idCol, self.accelerationCol]].groupby([self.idCol]).max()
            criterion = maxVals[self.accelerationCol].map(
                lambda val: val < self.minAcceleration or val > self.maxAcceleration)

            outliers = maxVals[criterion]

            if returnVals:
                return outliers
            else:
                return outliers.index


    

    
    def getOutliersByYDisplacement(self,
            tracksDf:pd.DataFrame, 
            byIQR=False,
            returnVals=False
        ) -> pd.Series:

        if byIQR:
            return self.getMaxOutliersByCol(
                tracksDf,
                col = self.displacementY,
                byIQR=byIQR,
                returnVals=returnVals
            )
            

        else:
            print(f"using min Y displacement ({self.minYDisplacement})")
            maxVals = tracksDf[[self.idCol, self.displacementYCol]].groupby([self.idCol]).max()
            criterion = maxVals[self.displacementYCol].map(
                lambda val: val < self.minYDisplacement)

            outliers = maxVals[criterion]

            if returnVals:
                return outliers
            else:
                return outliers.index

    
    def getOutliersByXDisplacement(self,
            tracksDf:pd.DataFrame, 
            byIQR=False,
            returnVals=False
        ) -> pd.Series:

        if byIQR:
            return self.getMaxOutliersByCol(
                tracksDf,
                col = self.displacementY,
                byIQR=byIQR,
                returnVals=returnVals
            )
            

        else:
            print(f"using max X displacement ({self.maxXDisplacement})")
            maxVals = tracksDf[[self.idCol, self.displacementXCol]].groupby([self.idCol]).max()
            criterion = maxVals[self.displacementXCol].map(
                lambda val: val > self.maxXDisplacement)

            outliers = maxVals[criterion]

            if returnVals:
                return outliers
            else:
                return outliers.index


    
    def cleanBySpeed(self, 
            tracksDf:pd.DataFrame, 
            byIQR=False,
        ) -> pd.DataFrame:

        outlierIds = self.getOutliersBySpeed(
            tracksDf, 
            byIQR
        )
        criterion = tracksDf[self.idCol].map(
            lambda trackId: trackId not in outlierIds)
        
        return tracksDf[criterion].copy()

    def cleanByAcceleration(self, 
            tracksDf:pd.DataFrame, 
            byIQR=False,
        ) -> pd.DataFrame:

        outlierIds = self.getOutliersByAcceleration(
            tracksDf, 
            byIQR
        )
        criterion = tracksDf[self.idCol].map(
            lambda trackId: trackId not in outlierIds)
        
        return tracksDf[criterion].copy()

    
    def cleanByYDisplacement(self, 
            tracksDf:pd.DataFrame, 
            byIQR=False,
        ) -> pd.DataFrame:

        outlierIds = self.getOutliersByYDisplacement(
            tracksDf, 
            byIQR
        )
        criterion = tracksDf[self.idCol].map(
            lambda trackId: trackId not in outlierIds)
        
        return tracksDf[criterion].copy()
    
    def cleanByXDisplacement(self, 
            tracksDf:pd.DataFrame, 
            byIQR=False,
        ) -> pd.DataFrame:

        outlierIds = self.getOutliersByXDisplacement(
            tracksDf, 
            byIQR
        )
        criterion = tracksDf[self.idCol].map(
            lambda trackId: trackId not in outlierIds)
        
        return tracksDf[criterion].copy()



        



    