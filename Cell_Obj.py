class CellObj:
    lte_cell = []

    def __init__(self, row):
        self.BSC = row[0]
        self.CI = row[1]
        self.SAC = row[2]
        self.LAC = row[3]
        self.RAC = row[4]
        self.Site_Name = row[5]
        self.Azimuth = row[6]
        self.Latitude = row[7]
        self.Longitude = row[8]
        self.Tilt = row[9]
        self.BSIC = row[10]
        self.Channel = row[11]
        self.PCI = row[12]
        self.RSI = row[13]
        self.BCCH = row[14]


        self.ENBFunctionFDD = str(self.CI)[6]
        self.EUtranCellFDD = (int(self.ENBFunctionFDD) * 256) + int(self.CI[-2:])

        if self.Channel == 1700:
            self.CoSectorName = f'{self.Site_Name[:9]}_D'
        if self.Channel == 3676:
            self.CoSectorName = f'{self.Site_Name[:9]}_G'
        if self.Channel == 2900:
            self.CoSectorName = f'{self.Site_Name[:9]}_D'

        self.__class__.lte_cell.append(self)

