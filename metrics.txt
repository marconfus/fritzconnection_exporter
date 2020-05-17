call_action("UserInterface1", "X_AVM-DE_GetInfo"

{'NewX_AVM-DE_AutoUpdateMode': 'important',
 'NewX_AVM-DE_CurrentFwVersion': '113.07.12',
 'NewX_AVM-DE_LastFwVersion': '113.07.11',
 'NewX_AVM-DE_LastInfoUrl': 'http://download.avm.de/fritzbox/fritzbox-7490/deutschland/fritz.os/info_de.txt',
 'NewX_AVM-DE_UpdateSuccessful': 'succeeded',
 'NewX_AVM-DE_UpdateTime': '2019-08-17T18:57:50+02:00'}

call_action("WANDSLInterfaceConfig1", "GetInfo")
 {'NewATURCountry': '0400',
 'NewATURVendor': '41564d00',
 'NewDataPath': 'Interleaved',
 'NewDownstreamAttenuation': 100,
 'NewDownstreamCurrRate': 63679,
 'NewDownstreamMaxRate': 77660,
 'NewDownstreamNoiseMargin': 110,
 'NewDownstreamPower': 496,
 'NewEnable': True,
 'NewStatus': 'Up',
 'NewUpstreamAttenuation': 100,
 'NewUpstreamCurrRate': 12735,
 'NewUpstreamMaxRate': 22710,
 'NewUpstreamNoiseMargin': 130,
 'NewUpstreamPower': 496}

call_action("WANDSLInterfaceConfig1", "GetStatisticsTotal")
{'NewATUCCRCErrors': 44,
 'NewATUCFECErrors': 64215,
 'NewATUCHECErrors': 0,
 'NewCRCErrors': 187,
 'NewCellDelin': 0,
 'NewErroredSecs': 46,
 'NewFECErrors': 383051,
 'NewHECErrors': 0,
 'NewInitErrors': 0,
 'NewInitTimeouts': 0,
 'NewLinkRetrain': 0,
 'NewLossOfFraming': 0,
 'NewReceiveBlocks': 1449353021,
 'NewSeverelyErroredSecs': 0,
 'NewTransmitBlocks': 477290725}

call_action("WANDSLInterfaceConfig1", "X_AVM-DE_GetDSLDiagnoseInfox")
{'NewX_AVM-DE_CableNokDistance': -1,
 'NewX_AVM-DE_DSLActive': True,
 'NewX_AVM-DE_DSLDiagnoseState': 'NONE',
 'NewX_AVM-DE_DSLLastDiagnoseTime': 0,
 'NewX_AVM-DE_DSLSignalLossTime': 0,
 'NewX_AVM-DE_DSLSync': True}

call_action("WANDSLLinkConfig1", "GetInfo")
{'NewATMEncapsulation': 'LLC',
 'NewATMPeakCellRate': 0,
 'NewATMQoS': 'UBR',
 'NewATMSustainableCellRate': 0,
 'NewAutoConfig': False,
 'NewDestinationAddress': 'PVC: 1/32',
 'NewEnable': True,
 'NewLinkStatus': 'Up',
 'NewLinkType': 'PPPoE'}

call_action("WANDSLLinkConfig1", "GetStatistics")
{'NewAAL5CRCErrors': 0,
 'NewATMCRCErrors': 0,
 'NewATMReceivedBlocks': 374144169,
 'NewATMTransmittedBlocks': 578028475}

