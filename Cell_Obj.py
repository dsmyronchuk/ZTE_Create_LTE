class CellObj:
    lte_cell = []

    def __init__(self, row, dct_standard, user_bs_type, user_choice):
        self.user_bs_type = user_bs_type
        self.user_choice = user_choice

        self.BSC = row[0]
        self.CI = row[1]
        self.SAC = row[2]
        self.LAC = row[3]
        self.Site_Name = row[5]
        self.Azimuth = row[6]
        self.Latitude = row[7].replace("'", "").replace('.', '').replace('°', '.').replace('"N', '')
        self.Longitude = row[8].replace("'", "").replace('.', '').replace('°', '.').replace('"E', '')
        self.Tilt = row[9]
        self.BSIC = int(row[10])
        self.Channel = row[11]
        self.PCI = int(row[12])
        self.RSI = int(row[13])
        self.enbName = self.Site_Name.replace('_', ' ')

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

        if self.user_choice.lower() != 'parameter':
            self.rru_pipe_func()
            self.parameter_cell()

        self.full_name = self.correct_name_cell()
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
            self.nB = 1
            self.bandWidthDl = 1
            self.bandWidthUl = 1
            self.maxUeRbNumDl = 15
            self.maxUeRbNumUl = 10
            self.pucchBlankNum = 2
            self.noneStdBwPwrCtrl = 0
            self.closeFrameRatio = 20
            self.cellBW = '1.5'

        elif self.Bandwidth == '5':
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
            self.closeFrameRatio = 20
            self.cellBW = '1.5'             # под вопросом, на сети нет

        elif self.Bandwidth == '10':
            self.upInterfFreqEffThr = 4
            self.nB = 2
            self.bandWidthDl = 3
            self.bandWidthUl = 3
            self.maxUeRbNumDl = 50
            self.maxUeRbNumUl = 23
            self.nB = 2
            self.bandWidthDl = 3
            self.bandWidthUl = 3
            self.maxUeRbNumDl = 50
            self.maxUeRbNumUl = 23
            self.noneStdBwPwrCtrl = 0
            self.closeFrameRatio = 30
            self.cellBW = '5'

        elif self.Bandwidth == '15':
            self.upInterfFreqEffThr = 5
            self.nB = 2
            self.bandWidthDl = 4
            self.bandWidthUl = 4
            self.maxUeRbNumDl = 75
            self.maxUeRbNumUl = 28
            self.nB = 2
            self.bandWidthDl = 4
            self.bandWidthUl = 4
            self.maxUeRbNumDl = 75
            self.maxUeRbNumUl = 28
            self.noneStdBwPwrCtrl = 0
            self.closeFrameRatio = 40
            self.cellBW = '7.5'

        elif self.Bandwidth == '20':
            self.upInterfFreqEffThr = 5
            self.nB = 2
            self.bandWidthDl = 5
            self.bandWidthUl = 5
            self.maxUeRbNumDl = 100
            self.maxUeRbNumUl = 33
            self.nB = 2
            self.bandWidthDl = 5
            self.bandWidthUl = 5
            self.maxUeRbNumDl = 100
            self.maxUeRbNumUl = 33
            self.noneStdBwPwrCtrl = 0
            self.closeFrameRatio = 40
            self.cellBW = '10'

    def parameter_aboud_standard(self):
        if self.Channel == 3676:
            self.numberOfRAPreambles = 6
            self.ncs = 13
            self.sizeOfRAPreamblesGroupA = 6
            self.macNonContenPreamble = 28
            self.prachFMRecOnTASwch = 0
            self.prachSupFarCoverSwch = 1
            self.freqBandInd = '8'
            self.earfcnUl = '902.6'
            self.earfcnDl = '947.6'
            self.configDRXTimerForNSA = '1000'

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
            self.freqBandInd = '3'
            self.earfcnUl = '1760'
            self.earfcnDl = '1855'
            self.configDRXTimerForNSA = '0'

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
            self.freqBandInd = '7'
            self.earfcnUl = '2515'
            self.earfcnDl = '2635'
            self.configDRXTimerForNSA = '1000'

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

    def rru_pipe_func(self):
        input_rru_pipe = input(f'Enter EquipmentFunction for CI{self.CI}: ')  # '51=1,4; 52=1,4' формат от юзера

        self.rru_1 = input_rru_pipe.replace(' ', '').split(';')[0].split('=')[0]        # Получаю номер первой ррю
        if ';' in input_rru_pipe:                                                       # Если на вход пришло 2 ррю:
            self.rru_2 = input_rru_pipe.replace(' ', '').split(';')[1].split('=')[0]    # Получаю номер второй ррю

        self.rru_pipe = {}                                        # Словарь для хранения пайпов к кадой ррю
        for i in input_rru_pipe.replace(' ', '').split(';'):      # '51=1,4; 52=1,4' формат который приходит
            i = i.split('=')
            self.rru_pipe[i[0]] = i[1]                            # [{'51': '1'}, {'52': '1'}] формат на выходе

        def config_selection(obj):
            first_elem = list(obj.rru_pipe)[0]                 # '1,4' // '1'  формат который получается
            if len(obj.rru_pipe) == 2 and len(obj.rru_pipe[first_elem]) == 3:
                return '2x2'

            elif len(obj.rru_pipe) == 2 and len(obj.rru_pipe[first_elem]) == 1:
                return '2x1'

            elif len(obj.rru_pipe) == 1 and len(obj.rru_pipe[first_elem]) == 3:
                return '1x2'

            elif len(obj.rru_pipe) == 1 and len(obj.rru_pipe[first_elem]) == 1:
                return '1x1'

        def power_selection(obj):
            if obj.Channel == 1700 and obj.rru_config == '2x2':
                return ['49', '18.2']

            elif obj.Channel == 1700 and obj.rru_config == '2x1':
                return ['47.8', '15.2']

            elif obj.Channel == 3676 and obj.rru_config == '2x1':
                return ['46', '18.2']

            elif obj.Channel == 1700 and obj.rru_config == '1x2':       # 47.8 под вопросом, возможно нужно будет 49
                return ['49', '15.2']

            elif obj.Channel == 3676 and obj.rru_config == '1x2':
                return ['46', '18.2']

            elif obj.Channel == 1700 and obj.rru_config == '1x1':       # Очень редко используется, ближе к никогда
                return ['43', '8']

            elif obj.Channel == 3676 and obj.rru_config == '1x1':
                return ['46', '18.2']

        def ECellEquipmentFunction_selection(obj):
            if obj.Channel == 3676:
                return obj.ENBCell_id

            else:
                return CellObj.lte_cell.index(obj)

        def MIMO_selection(obj):     # MIMO 2x2 // 4x4
            if obj.rru_config == '2x2':
                obj.cellRSPortnum = '2'
                obj.flagswimode = '6'
                obj.tm34T4RSwch = '1'
                obj.tm44T4RSwch = '1'

            elif obj.rru_config in ('1x2', '2x1'):
                obj.cellRSPortnum = '1'
                obj.flagswimode = '6'
                obj.tm34T4RSwch = '0'
                obj.tm44T4RSwch = '0'

            elif obj.rru_config == '1x1':
                obj.cellRSPortnum = '0'
                obj.flagswimode = '1'
                obj.tm34T4RSwch = '0'
                obj.tm44T4RSwch = '0'

        self.rru_config = config_selection(self)
        self.rru_power = power_selection(self)
        self.ECellEquipmentFunction = ECellEquipmentFunction_selection(self)
        MIMO_selection(self)

    def correct_name_cell(self):

        def azimuth(obj):
            azz = obj.Azimuth[:-1]
            if len(azz) == 2 or len(azz) == 1:
                azz = azz.zfill(3)
            if azz == 'indoor':
                azz = 'ind'
            return azz

        def type_lte(obj):
            if obj.Channel == 1700:
                return 'L18'
            if obj.Channel == 3676:
                return 'L09'
            if obj.Channel == 2900:
                return 'L26'

        return f'{self.Site_Name[:11]}_{azimuth(self)}_{type_lte(self)}'

    def parameter_cell(self):
        if self.Channel == 1700:
            self.pcilist = '0;0;0;0;0;0;0;0;0;0;0;0;'
            self.urgencyeai = '0;4294967295;4294967295;4294967295;4294967295;4294967295;4294967295;4294967295;' \
                              '4294967295;4294967295;4294967295;4294967295;4294967295;4294967295;4294967295;4294967295'
        if self.Channel in (3676, 2900):
            self.pcilist = '65535;65535;65535;65535;65535;65535;65535;65535;65535;65535;65535;65535;'
            self.urgencyeai = '0'




