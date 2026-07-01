import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'
import { FrameBuilder } from '@/widgets/FrameBuilder'
import { OsiModel } from '@/widgets/osi/OsiWidget'
import { MacLearning } from '@/widgets/switch/MacLearningWidget'
import { Subnet } from '@/widgets/subnet/SubnetWidget'
import { Routing } from '@/widgets/router/RoutingWidget'
import { Nat } from '@/widgets/nat/NatWidget'
import { Dns } from '@/widgets/dns/DnsWidget'
import { Arp } from '@/widgets/arp/ArpWidget'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
  'frame-builder': FrameBuilder,
  'osi-model': OsiModel,
  'mac-learning': MacLearning,
  'subnet-calc': Subnet,
  'arp-demo': Arp,
  'routing-demo': Routing,
  'nat-demo': Nat,
  'dns-demo': Dns,
}
