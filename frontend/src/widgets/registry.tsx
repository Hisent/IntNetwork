import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'
import { FrameBuilder } from '@/widgets/FrameBuilder'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
  'frame-builder': FrameBuilder,
}
