import prometheus_client
import fritzconnection
import time
import os
from fritzconnection.lib.fritzstatus import FritzStatus
from prometheus_client.core import REGISTRY
from pprint import pprint

fc = None
registry = REGISTRY

info_metric = prometheus_client.Info(
    'fritzconnection', 'Fritz!Box information', registry=registry)
uptime_metric = prometheus_client.Gauge(
    'fritzconnection_uptime', "System uptime", registry=registry)
wan_info_metric = prometheus_client.Info(
    'fritzconnection_wan', 'WAN information', registry=registry)
max_bitrate_downstream_metric = prometheus_client.Gauge('fritzconnection_wan_max_bitrate_downstream',
                                                        "Downstream max downstream", registry=registry)
max_bitrate_upstream_metric = prometheus_client.Gauge('fritzconnection_wan_max_bitrate_upstream',
                                                      "Downstream max upstream", registry=registry)
link_metric = prometheus_client.Gauge('fritzconnection_wan_physical_link_up',
                                      "Physical link status", ["link_status"], registry=registry)
wan_bytes_received_metric = prometheus_client.Gauge('fritzconnection_wan_total_bytes_received',
                                                    "WAN total bytes received", registry=registry)
wan_bytes_sent_metric = prometheus_client.Gauge('fritzconnection_wan_total_bytes_sent',
                                                "WAN total bytes sent", registry=registry)
external_ip_info_metric = prometheus_client.Info("fritzconnection_external_ip", "External IP adresses",
                                                 registry=registry)
lan_total_bytes_received_metric = prometheus_client.Gauge('fritzconnection_lan_total_bytes_received',
                                                          "LAN total bytes received", registry=registry)

lan_total_bytes_sent_metric = prometheus_client.Gauge('fritzconnection_lan_total_bytes_sent',
                                                      "LAN total bytes received", registry=registry)


def init_fritzconnection():
    global fc

    fc = fritzconnection.FritzConnection(
        address=os.getenv("FB_ADDRESS"), password=os.getenv("FB_PASSWORD"))


def init_prometheus():
    # global registry
    # registry = REGISTRY
    # registry = prometheus_client.CollectorRegistry()
    pass


def get_info():
    status = FritzStatus(fc)
    device_info = fc.call_action("DeviceInfo1", "GetInfo")
    description = device_info.get("NewDescription")
    software_version = device_info.get("NewSoftwareVersion")
    serial_number = device_info.get("NewSerialNumber")
    uptime = device_info.get("NewUpTime")
    info_metric.info({"model": status.modelname, "software_version": software_version,
                      "device_description": description, "serial_number": serial_number})
    uptime_metric.set(uptime)


def get_wan_info():
    wan_info = fc.call_action("WANCommonIFC1", "GetCommonLinkProperties")
    wan_access_type = wan_info.get("NewWANAccessType")
    max_bitrate_downstream = wan_info.get("NewLayer1DownstreamMaxBitRate")
    max_bitrate_upstream = wan_info.get("NewLayer1UpstreamMaxBitRate")
    wan_info_metric.info({"access_type": wan_access_type})

    max_bitrate_downstream_metric.set(max_bitrate_downstream)
    max_bitrate_upstream_metric.set(max_bitrate_upstream)

    wan_physical_link_status = wan_info.get("NewPhysicalLinkStatus")
    if wan_physical_link_status == "Up":
        link_status = 1
    else:
        link_status = 0
    link_metric.labels(link_status=wan_physical_link_status).set(link_status)

    wan_info = fc.call_action("WANCommonIFC1", "GetAddonInfos")
    total_bytes_received = wan_info.get("NewX_AVM_DE_TotalBytesReceived64")
    total_bytes_sent = wan_info.get("NewX_AVM_DE_TotalBytesSent64")

    wan_bytes_received_metric.set(total_bytes_received)
    wan_bytes_sent_metric.set(total_bytes_sent)

    # dsl_info = fc.call_action("WANDSLLinkC1", "GetDSLLinkInfo")
    # -> PPPoE
    # link_type = dsl_info.get("NewLinkType")

    ip_conn = fc.call_action("WANIPConn1", "GetExternalIPAddress")
    external_ipv4 = ip_conn.get("NewExternalIPAddress")

    ip_conn = fc.call_action("WANIPConn1", "X_AVM_DE_GetExternalIPv6Address")
    external_ipv6 = ip_conn.get("NewExternalIPv6Address")

    external_ip_info_metric.info(
        {'ipv4': external_ipv4, 'ipv6': external_ipv6})


def get_lan_info():
    lan_info = fc.call_action("LANEthernetInterfaceConfig1", "GetStatistics")

    lan_total_bytes_received_metric.set(lan_info.get("NewBytesReceived"))
    lan_total_bytes_sent_metric.set(lan_info.get("NewBytesSent"))

    # info = fc.call_action("WANIPConnection1", "GetInfo")
    # pprint(info)


def main():
    init_fritzconnection()
    init_prometheus()
    # prometheus_client.start_http_server(int(os.getenv("PROM_PORT", 9090)))
    prometheus_client.start_http_server(
        int(os.getenv("PROM_PORT", 9090)), registry=registry)

    while True:
        get_info()
        get_wan_info()
        get_lan_info()
        time.sleep(60)

    # print(prometheus_client.generate_latest(registry).decode())


if __name__ == "__main__":
    main()
