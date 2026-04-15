from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet

class AccessControlSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Whitelist of allowed MAC addresses
    WHITELIST = {
        "00:00:00:00:00:01",
        "00:00:00:00:00:02"
    }

    def __init__(self, *args, **kwargs):
        super(AccessControlSwitch, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Default rule: send unknown packets to controller
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        src = eth.src
        dst = eth.dst

        # Check whitelist
        if src in self.WHITELIST:
            self.logger.info(f"ALLOWED: {src} -> {dst}")

            match = parser.OFPMatch(eth_src=src)
            actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]  # allowed rules

            # Install allow rule
            self.add_flow(datapath, 10, match, actions)

        else:
            self.logger.info(f"BLOCKED: {src}")

            match = parser.OFPMatch(eth_src=src)
            actions = []  # No actions = drop (denied rules)

            # Install deny rule
            self.add_flow(datapath, 20, match, actions)