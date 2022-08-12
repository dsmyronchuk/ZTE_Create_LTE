class CellObj:
    lte_cell = []

    def __init__(self, row, dct_standard, user_bs_type):
        self.user_bs_type = user_bs_type

        self.BSC = row[0]
        self.CI = row[1]
        self.SAC = row[2]
        self.LAC = row[3]
        self.Site_Name = row[5]
        self.Azimuth = row[6]
        self.Latitude = row[7]
        self.Longitude = row[8]
        self.Tilt = row[9]
        self.BSIC = int(row[10])
        self.Channel = row[11]
        self.PCI = int(row[12])
        self.RSI = int(row[13])

        self.csfb_arfcn = []
        self.csfb_arfcn_gsm = []
        self.csfb_arfcn_dcs = []

        self.ENBFunctionFDD = str(self.CI)[:6]
        self.ENBCell_id = str(self.CI)[-2:]
        self.EUtranCellFDD = (int(self.ENBFunctionFDD) * 256) + int(self.ENBCell_id)

        if self.Channel == 1700:
            self.CoSectorName = f'{self.Site_Name[:-1]}D'
        if self.Channel == 3676:
            self.CoSectorName = f'{self.Site_Name[:-1]}G'
        if self.Channel == 2900:
            self.CoSectorName = f'{self.Site_Name[:-1]}D'

        self.create_offset()
        self.Bandwidth = dct_standard[str(self.Channel)]
        self.parameter_about_bandwidth()
        self.parameter_aboud_standard()
        self.prach_index()
        self.eutrancellmeasurement()

        self.__class__.lte_cell.append(self)

    def create_offset(self):
        azz = self.Azimuth[:-1]
        if len(azz) == 2 or len(azz) == 1:
            self.offsetAngle = azz.zfill(3)
        if len(azz) == 3:
            self.offsetAngle = azz
        if azz == 'indoor':
            self.offsetAngle = '360'

    def parameter_about_bandwidth(self):
        if self.Bandwidth == '3':
            self.upInterfFreqEffThr = 4
            self.nB = 1
            self.bandWidthDl = 1
            self.bandWidthUl = 1
            self.maxUeRbNumDl = 15
            self.maxUeRbNumUl = 10
            self.pucchBlankNum = 2
            self.upInterfFreqEffThr = 4
            self.nB = 1
            self.bandWidthDl = 1
            self.bandWidthUl = 1
            self.maxUeRbNumDl = 15
            self.maxUeRbNumUl = 10
            self.pucchBlankNum = 2
            self.noneStdBwPwrCtrl = 0

        elif self.Bandwidth == '5':
            self.upInterfFreqEffThr = 4
            self.nB = 1
            self.bandWidthDl = 2
            self.bandWidthUl = 2
            self.maxUeRbNumDl = 24
            self.maxUeRbNumUl = 14
            self.pucchBlankNum = 0
            self.upInterfFreqEffThr = 4
            self.nB = 1
            self.bandWidthDl = 2
            self.bandWidthUl = 2
            self.maxUeRbNumDl = 24
            self.maxUeRbNumUl = 14
            self.pucchBlankNum = 0
            self.noneStdBwPwrCtrl = 14

        elif self.Bandwidth == '10':
            self.upInterfFreqEffThr = 4
            self.nB = 2
            self.bandWidthDl = 3
            self.bandWidthUl = 3
            self.maxUeRbNumDl = 50
            self.maxUeRbNumUl = 23
            self.upInterfFreqEffThr = 4
            self.nB = 2
            self.bandWidthDl = 3
            self.bandWidthUl = 3
            self.maxUeRbNumDl = 50
            self.maxUeRbNumUl = 23

        elif self.Bandwidth == '15':
            self.upInterfFreqEffThr = 5
            self.nB = 2
            self.bandWidthDl = 4
            self.bandWidthUl = 4
            self.maxUeRbNumDl = 75
            self.maxUeRbNumUl = 28
            self.upInterfFreqEffThr = 5
            self.nB = 2
            self.bandWidthDl = 4
            self.bandWidthUl = 4
            self.maxUeRbNumDl = 75
            self.maxUeRbNumUl = 28

        elif self.Bandwidth == '20':
            self.upInterfFreqEffThr = 5
            self.nB = 2
            self.bandWidthDl = 5
            self.bandWidthUl = 5
            self.maxUeRbNumDl = 100
            self.maxUeRbNumUl = 33
            self.upInterfFreqEffThr = 5
            self.nB = 2
            self.bandWidthDl = 5
            self.bandWidthUl = 5
            self.maxUeRbNumDl = 100
            self.maxUeRbNumUl = 33

    def parameter_aboud_standard(self):
        if self.Channel == 3676:
            self.numberOfRAPreambles = 6
            self.ncs = 13
            self.sizeOfRAPreamblesGroupA = 6
            self.macNonContenPreamble = 28
            self.prachFMRecOnTASwch = 0
            self.prachSupFarCoverSwch = 1

            self.threshSvrLow = 4
            self.cellReselectionPriority = 2
            self.eutranRslPara_eMTCInterReselPrio_1 = 6
            self.eutranRslPara_eMTCInterReselPrio_2 = 5
            self.eutranRslPara_eMTCInterThrdXHigh = 10
            self.eutranRslPara_interReselPrio_1 = 6
            self.eutranRslPara_interReselPrio_2 = 5
            self.eutranRslPara_interThrdXHigh_1 = 10
            self.eutranRslPara_interThrdXHigh_2 = 10
            self.eutranRslPara_interCarriFreq_1 = 2635.0
            self.eutranRslPara_interCarriFreq_2 = 1855.0
            self.eutranRslPara_freqBandInd_1 = 7
            self.eutranRslPara_freqBandInd_2 = 3
            self.eMTCIntraReselPrio = 6

            self.CellMeasGroup = 3

        elif self.Channel == 1700:
            self.numberOfRAPreambles = 12
            self.ncs = 10
            self.sizeOfRAPreamblesGroupA = 11
            self.macNonContenPreamble = 4
            self.prachFMRecOnTASwch = 1
            self.prachSupFarCoverSwch = 0

            self.threshSvrLow = 6
            self.cellReselectionPriority = 5
            self.eutranRslPara_eMTCInterReselPrio_1 = 6
            self.eutranRslPara_eMTCInterReselPrio_2 = 2
            self.eutranRslPara_eMTCInterThrdXHigh = 12
            self.eutranRslPara_interReselPrio_1 = 6
            self.eutranRslPara_interReselPrio_2 = 2
            self.eutranRslPara_interThrdXHigh_1 = 12
            self.eutranRslPara_interThrdXHigh_2 = 14
            self.eutranRslPara_interCarriFreq_1 = 2635.0
            self.eutranRslPara_interCarriFreq_2 = 947.6
            self.eutranRslPara_freqBandInd_1 = 7
            self.eutranRslPara_freqBandInd_2 = 8
            self.eMTCIntraReselPrio = 5

            self.CellMeasGroup = 1

        elif self.Channel == 2900:
            self.numberOfRAPreambles = 6
            self.ncs = 13
            self.sizeOfRAPreamblesGroupA = 6
            self.macNonContenPreamble = 28
            self.prachFMRecOnTASwch = 0
            self.prachSupFarCoverSwch = 1

            self.threshSvrLow = 6
            self.cellReselectionPriority = 6
            self.eutranRslPara_eMTCInterReselPrio_1 = 5
            self.eutranRslPara_eMTCInterReselPrio_2 = 2
            self.eutranRslPara_eMTCInterThrdXHigh = 12
            self.eutranRslPara_interReselPrio_1 = 5
            self.eutranRslPara_interReselPrio_2 = 2
            self.eutranRslPara_interThrdXHigh_1 = 12
            self.eutranRslPara_interThrdXHigh_2 = 14
            self.eutranRslPara_interCarriFreq_1 = 1855.0
            self.eutranRslPara_interCarriFreq_2 = 947.6
            self.eutranRslPara_freqBandInd_1 = 3
            self.eutranRslPara_freqBandInd_2 = 8
            self.eMTCIntraReselPrio = 6

            self.CellMeasGroup = 2

    def prach_index(self):
        self.prachConfigIndex = '5'

        if self.ENBCell_id == '81':
            self.prachConfigIndex = '35'
        if self.ENBCell_id == '82':
            self.prachConfigIndex = '36'
        if self.ENBCell_id == '83':
            self.prachConfigIndex = '37'
        if self.ENBCell_id == '84':
            self.prachConfigIndex = '38'
        if self.ENBCell_id == '85':
            self.prachConfigIndex = '39'

    def eutrancellmeasurement(self):
        if self.Channel == 3676 and self.user_bs_type:     # L09 GL GSM
            self.ratPriIdleCSFB2 = '100'                   # L09 GUL  UMTS
            self.ratPriIdleCSFB1 = '200'
            self.ratPriCnCSFB2 = '100'
            self.ratPriCnCSFB1 = '200'
            self.csfbMeasure = '0'
            self.endcPccFreqPrio_1 = '255'
            self.endcPccFreqPrio_2 = '254'
            self.clbInterFreqPriority_1 = '255'
            self.clbInterFreqPriority_2 = '254'
            self.scellFreqPriority_1 = '255'
            self.scellFreqPriority_2 = '254'
            self.lbInterFreqPriority_1 = '255'
            self.lbInterFreqPriority_2 = '254'
            self.interCarriFreq_1 = '2635.0'
            self.interCarriFreq_2 = '1855.0'
            self.freqBandInd_1 = '7'
            self.freqBandInd_2 = '3'
            self.geranFreqRdPriority = '200'
            self.geranFreqCsfbPriority = '200'
            self.quantityFddUtra = '0'
            self.utranFreqCsfbPriority = '100'
            self.utranFreqRdPriority = '100'
            self.ratPriority4 = '253'
            self.ratPriority3 = '254'

        if self.Channel == 1700 and self.user_bs_type in ['GUL City', 'GUL Rural']:  # L18 GUL  UMTS CITY
            self.ratPriIdleCSFB2 = '200'                                             # L18 GUL  UMTS Rural
            self.ratPriIdleCSFB1 = '100'
            self.ratPriCnCSFB2 = '200'
            self.ratPriCnCSFB1 = '100'
            self.endcPccFreqPrio_1 = '255'
            self.endcPccFreqPrio_2 = '253'
            self.clbInterFreqPriority_1 = '255'
            self.clbInterFreqPriority_2 = '253'
            self.scellFreqPriority_1 = '255'
            self.scellFreqPriority_2 = '253'
            self.lbInterFreqPriority_1 = '255'
            self.lbInterFreqPriority_2 = '253'
            self.interCarriFreq_1 = '2635.0'
            self.interCarriFreq_2 = '947.6'
            self.freqBandInd_1 = '7'
            self.freqBandInd_2 = '8'
            self.geranFreqRdPriority = '100'
            self.geranFreqCsfbPriority = '100'
            self.utranFreqCsfbPriority = '200'
            self.utranFreqRdPriority = '200'
            self.ratPriority4 = '254'
            self.ratPriority3 = '253'

            if self.user_bs_type == 'GUL City':
                self.quantityFddUtra = '1'
                self.csfbMeasure = '0'

            if self.user_bs_type == 'GUL Rural':
                self.quantityFddUtra = '0'
                self.csfbMeasure = '1'

        if self.Channel == 1700 and self.user_bs_type in ['GL City', 'GL Rural']:    # L18 GL  UMTS CITY
            self.ratPriIdleCSFB2 = '100'                                             # L18 GL  UMTS Rural
            self.ratPriIdleCSFB1 = '200'
            self.ratPriCnCSFB2 = '100'
            self.ratPriCnCSFB1 = '200'
            self.csfbMeasure = '0'
            self.endcPccFreqPrio_1 = '255'
            self.endcPccFreqPrio_2 = '253'
            self.clbInterFreqPriority_1 = '255'
            self.clbInterFreqPriority_2 = '253'
            self.scellFreqPriority_1 = '255'
            self.scellFreqPriority_2 = '253'
            self.lbInterFreqPriority_1 = '255'
            self.lbInterFreqPriority_2 = '253'
            self.interCarriFreq_1 = '2635.0'
            self.interCarriFreq_2 = '947.6'
            self.freqBandInd_1 = '7'
            self.freqBandInd_2 = '8'
            self.geranFreqRdPriority = '200'
            self.geranFreqCsfbPriority = '200'
            self.utranFreqCsfbPriority = '100'
            self.utranFreqRdPriority = '100'
            self.ratPriority4 = '253'
            self.ratPriority3 = '254'

            if self.user_bs_type == 'GL City':
                self.quantityFddUtra = '1'

            if self.user_bs_type == 'GL Rural':
                self.quantityFddUtra = '0'

        if self.Channel == 2900 and self.user_bs_type in ['GUL City', 'GUL Rural']:  # L26 GUL  UMTS
            self.ratPriIdleCSFB2 = '200'
            self.ratPriIdleCSFB1 = '100'
            self.ratPriCnCSFB2 = '200'
            self.ratPriCnCSFB1 = '100'
            self.csfbMeasure = '0'
            self.endcPccFreqPrio_1 = '255'
            self.endcPccFreqPrio_2 = '254'
            self.clbInterFreqPriority_1 = '255'
            self.clbInterFreqPriority_2 = '254'
            self.scellFreqPriority_1 = '255'
            self.scellFreqPriority_2 = '254'
            self.lbInterFreqPriority_1 = '255'
            self.lbInterFreqPriority_2 = '254'
            self.interCarriFreq_1 = '1855.0'
            self.interCarriFreq_2 = '947.6'
            self.freqBandInd_1 = '3'
            self.freqBandInd_2 = '8'
            self.geranFreqRdPriority = '100'
            self.geranFreqCsfbPriority = '100'
            self.quantityFddUtra = '1'
            self.utranFreqCsfbPriority = '200'
            self.utranFreqRdPriority = '200'
            self.ratPriority4 = '254'
            self.ratPriority3 = '253'

        if self.Channel == 2900 and self.user_bs_type in ['GL City', 'GL Rural']:    # L26 GL to GSM
            self.ratPriIdleCSFB2 = '100'
            self.ratPriIdleCSFB1 = '200'
            self.ratPriCnCSFB2 = '100'
            self.ratPriCnCSFB1 = '200'
            self.csfbMeasure = '0'
            self.endcPccFreqPrio_1 = '255'
            self.endcPccFreqPrio_2 = '253'
            self.clbInterFreqPriority_1 = '255'
            self.clbInterFreqPriority_2 = '253'
            self.scellFreqPriority_1 = '255'
            self.scellFreqPriority_2 = '253'
            self.lbInterFreqPriority_1 = '255'
            self.lbInterFreqPriority_2 = '253'
            self.interCarriFreq_1 = '1855.0'
            self.interCarriFreq_2 = '947.6'
            self.freqBandInd_1 = '3'
            self.freqBandInd_2 = '8'
            self.geranFreqRdPriority = '200'
            self.geranFreqCsfbPriority = '200'
            self.quantityFddUtra = '1'
            self.utranFreqCsfbPriority = '100'
            self.utranFreqRdPriority = '100'
            self.ratPriority4 = '253'
            self.ratPriority3 = '254'

    # метод вызывается снаружи
    @staticmethod
    def correct_arfcn_list():

        # Разбиваю Частоты на DCS/GSM для GsmReselection
        for i in CellObj.lte_cell:
            for j in i.csfb_arfcn:
                if int(j) > 125:
                    i.csfb_arfcn_dcs.append(j)
                else:
                    i.csfb_arfcn_gsm.append(j)

        # Заполнить не хватающие слоты пустыми значениями (65535)
        for i in CellObj.lte_cell:
            if len(i.csfb_arfcn) < 32:
                for j in range(32 - len(i.csfb_arfcn)):
                    i.csfb_arfcn.append('65535')

            if len(i.csfb_arfcn_gsm) < 32:
                for j in range(32 - len(i.csfb_arfcn_gsm)):
                    i.csfb_arfcn_gsm.append('65535')

            if len(i.csfb_arfcn_dcs) < 32:
                for j in range(32 - len(i.csfb_arfcn_dcs)):
                    i.csfb_arfcn_dcs.append('65535')



# ratPriIdleCSFB2 = self.ratPriIdleCSFB2,
# ratPriIdleCSFB1 = self.ratPriIdleCSFB1,
# ratPriCnCSFB2 = self.ratPriCnCSFB2,
# ratPriCnCSFB1 = self.ratPriCnCSFB1,
# csfbMeasure = self.csfbMeasure,
# endcPccFreqPrio_1 = self.endcPccFreqPrio_1,
# endcPccFreqPrio_2 = self.endcPccFreqPrio_2,
# clbInterFreqPriority_1 = self.clbInterFreqPriority_1,
# clbInterFreqPriority_2 = self.clbInterFreqPriority_2,
# scellFreqPriority_1 = self.scellFreqPriority_1,
# scellFreqPriority_2 = self.scellFreqPriority_2,
# lbInterFreqPriority_1 = self.lbInterFreqPriority_1,
# lbInterFreqPriority_2 = self.lbInterFreqPriority_2,
# interCarriFreq_1 = self.interCarriFreq_1,
# interCarriFreq_2 = self.interCarriFreq_2,
# freqBandInd_1 = self.freqBandInd_1,
# freqBandInd_2 = self.freqBandInd_2,
# geranFreqRdPriority = self.geranFreqRdPriority,
# geranFreqCsfbPriority = self.geranFreqCsfbPriority,
# quantityFddUtra = self.quantityFddUtra,
# utranFreqCsfbPriority = self.utranFreqCsfbPriority,
# utranFreqRdPriority = self.utranFreqRdPriority,
# ratPriority4 = self.ratPriority4,
# ratPriority3 = self.ratPriority3

