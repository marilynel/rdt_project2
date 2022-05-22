from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    # Add items as needed

    messageIndex = 0
    dataReceived = ''
    myDataList = []
    lastAckRecd = -1


    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        # Add items as needed

        self.messageIndex = 0
        self.dataReceived = ''
        self.myDataList = [None] * 100
        self.lastAckRecd = -1

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        self.dataReceived = ''
        #print('getDataReceived(): Complete this...')
        for seg in self.myDataList:
            if seg:
                self.dataReceived += seg.payload
            else:
                break
        # ############################################################################################################ #
        return self.dataReceived

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):
        #segmentSend = Segment()

        # ############################################################################################################ #
        print('processSend():')

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        # break up message into self.DATA_LENGTH sized pieces

        # check if there is anything to send
        if not self.dataToSend:
            return

        i = (self.lastAckRecd + 1) * self.DATA_LENGTH
        data = ""
        seqnum = self.messageIndex
        count = 0
        while (count + self.DATA_LENGTH < self.FLOW_CONTROL_WIN_SIZE):
            segmentSend = Segment()
            data = self.dataToSend[i:i + self.DATA_LENGTH]
            seqnum = i // 4
            #self.messageIndex += self.DATA_LENGTH
            segmentSend.setData(seqnum, data)
            print("Sending segment:", segmentSend.to_string())
            self.sendChannel.send(segmentSend)
            count += self.DATA_LENGTH
            i += self.DATA_LENGTH

        # can't send until i get an ack
        # ack must be less than
        # know where I am in the window
        # when is it ok to move past the window?
        # its the sender's responsibility to stay in the window
        # ack value is the sequence number
        # cannot leave seq num until ack equals or exceeds it




        # ############################################################################################################ #
        # Display sending segment
        #segmentSend.setData(seqnum,data)
        #print("Sending segment: ", segmentSend.to_string())

        # Use the unreliable sendChannel to send the segment
        #self.sendChannel.send(segmentSend)

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()                  # Segment acknowledging packet(s) received

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        # append data in segments to self.dataReceived


        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?
        print('processReceiveAndSendRespond():')

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...

        isPayload = False

        if listIncomingSegments:
            for seg in listIncomingSegments:
                if seg.payload:
                    self.myDataList[seg.seqnum] = seg
                    isPayload = True
                else:
                    # change this is last ack??
                    self.lastAckRecd = seg.seqnum

            if isPayload:
                #is this cumulative ack?
                lastAck = 0
                for seg in self.myDataList:
                    if not seg:
                        break
                    else:
                        lastAck = seg.seqnum
                # Display response segment
                segmentAck.setAck(lastAck)
                print("Sending ack: ", segmentAck.to_string())
                # Use the unreliable sendChannel to send the ack packet
                self.sendChannel.send(segmentAck)
            else:
                print(f"Rec'd an ACK {seg.acknum}")
                self.lastAckRecd = seg.acknum
