package main

import (
	"flag"
	"github.com/google/gopacket"
	"github.com/google/gopacket/tcpassembly"

	"github.com/google/gopacket/pcap"
	"log"
	"github.com/google/gopacket/layers"
	"fmt"
)

var (
	iface    = flag.String("i", "eth0", "Interface to get packets from")
	filter   = flag.String("f", "tcp", "BPF filter for pcap")
	port     = flag.String("p", "", "Port to filter")
	interval = flag.String("interval", "1s", "log interval. Any string parsed by time.ParseDuration is acceptable here")
)

func main() {

	log.Printf("starting capture on interface %q", *iface)

	// Set up pcap packet capture

	// http://www.tcpdump.org/pcap.html
	// pcap_t *pcap_open_live(char *device, int snaplen,
	// 						  int promisc, int to_ms, char *ebuf)
	// snaplen is an integer which defines the maximum number
	// of bytes to be captured by pcap
	// promisc promiscuous mode
	// to_ms is the read time out in milliseconds
	// 		a value of 0 means no time out
	// ebuf is a string we can store any error messages
	// p.cptr = C.pcap_open_live(dev, C.int(snaplen), pro, timeoutMillis(timeout), buf)
	// buf := (*C.char)(C.calloc(errorBufferSize, 1)) //  256
	handle, err := pcap.OpenLive(*iface, int32(65536), true, 0)
	if err != nil {
		log.Fatal("error opening pcap handle: ", err)
	}

	if len(port) > 0 {
		filter += " " + port
	}
	err = handle.SetBPFFilter(*filter)
	if err != nil {
		log.Fatal("error setting BPF filter: ", err)
	}

	// Set up assembly
	streamPool := tcpassembly.NewStreamPool(streamFactory)

	// Fast Decoding
	var eth layers.Ethernet
	var ip4 layers.IPv4
	var ip6 layers.IPv6
	var tcp layers.TCP
	parser := gopacket.NewDecodingLayerParser(layers.LayerTypeEthernet, &eth, &ip4, &ip6, &tcp)
	decoded := make([]gopacket.LayerType, 0, 4)

loop:
	for {
		data, ci, err := handle.ZeroCopyReadPacketData()

		if err != nil {
			log.Printf("error getting packet: %v", err)
			continue
		}

		err = parser.DecodeLayers(data, &decoded)
		if err != nil {
			log.Printf("error decoding packet: %v", err)
			continue
		}

		foundNetLayer := false
		for _, layerType := range decoded {
			switch layerType {
			case layers.LayerTypeIPv6:
				fmt.Println("    IP6 ", ip6.SrcIP, ip6.DstIP)
				foundNetLayer = true
			case layers.LayerTypeIPv4:
				fmt.Println("    IP4 ", ip4.SrcIP, ip4.DstIP)
				foundNetLayer = true
			case layers.LayerTypeTCP:
				if foundNetLayer {
					fmt.Println("    TCP ", tcp.SrcPort, tcp.DstPort)
				} else {
					log.Println("could not find IPv4 or IPv6 layer, inoring")
				}

				continue loop
			}
		}
	}

}
