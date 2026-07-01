import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'
import { FrameBuilder } from '@/widgets/FrameBuilder'
import { OsiModel } from '@/widgets/osi/OsiWidget'
import { MacLearning } from '@/widgets/switch/MacLearningWidget'
import { Subnet } from '@/widgets/subnet/SubnetWidget'
import { Routing } from '@/widgets/router/RoutingWidget'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
  'frame-builder': FrameBuilder,
  'osi-model': OsiModel,
  'mac-learning': MacLearning,
  'subnet-calc': Subnet,
  'routing-demo': Routing,
}
