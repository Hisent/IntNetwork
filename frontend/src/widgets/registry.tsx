import { lazy, type ComponentType } from 'react'
import type { Lang } from '@/lib/i18n'

// Alle Widgets lazy: sie machen den Großteil des Bundles aus, aber pro
// Modulseite wird höchstens eine Handvoll gebraucht. Named-Export -> default
// mappen, weil React.lazy nur default-Exporte versteht.
export const WIDGETS: Record<string, ComponentType<{ lang: Lang }>> = {
  'vlan-switch': lazy(() => import('@/widgets/VlanSwitch').then((m) => ({ default: m.VlanSwitch }))),
  'frame-builder': lazy(() => import('@/widgets/FrameBuilder').then((m) => ({ default: m.FrameBuilder }))),
  'osi-model': lazy(() => import('@/widgets/osi/OsiWidget').then((m) => ({ default: m.OsiModel }))),
  'mac-learning': lazy(() => import('@/widgets/switch/MacLearningWidget').then((m) => ({ default: m.MacLearning }))),
  'subnet-calc': lazy(() => import('@/widgets/subnet/SubnetWidget').then((m) => ({ default: m.Subnet }))),
  'arp-demo': lazy(() => import('@/widgets/arp/ArpWidget').then((m) => ({ default: m.Arp }))),
  'routing-demo': lazy(() => import('@/widgets/router/RoutingWidget').then((m) => ({ default: m.Routing }))),
  'nat-demo': lazy(() => import('@/widgets/nat/NatWidget').then((m) => ({ default: m.Nat }))),
  'dns-demo': lazy(() => import('@/widgets/dns/DnsWidget').then((m) => ({ default: m.Dns }))),
  'dhcp-demo': lazy(() => import('@/widgets/dhcp/DhcpWidget').then((m) => ({ default: m.Dhcp }))),
  'ports-demo': lazy(() => import('@/widgets/ports/PortsWidget').then((m) => ({ default: m.Ports }))),
  'icmp-demo': lazy(() => import('@/widgets/icmp/IcmpWidget').then((m) => ({ default: m.Icmp }))),
  'firewall-demo': lazy(() => import('@/widgets/firewall/FirewallWidget').then((m) => ({ default: m.Firewall }))),
  'ipv6-demo': lazy(() => import('@/widgets/ipv6/Ipv6Widget').then((m) => ({ default: m.Ipv6 }))),
  'wlan-demo': lazy(() => import('@/widgets/wlan/WlanWidget').then((m) => ({ default: m.Wlan }))),
  'vpn-demo': lazy(() => import('@/widgets/vpn/VpnWidget').then((m) => ({ default: m.Vpn }))),
}
