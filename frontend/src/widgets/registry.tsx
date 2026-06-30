import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'
import { FrameBuilder } from '@/widgets/FrameBuilder'
import { OsiModel } from '@/widgets/osi/OsiWidget'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
  'frame-builder': FrameBuilder,
  'osi-model': OsiModel,
}
