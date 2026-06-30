import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'
import { FrameBuilder } from '@/widgets/FrameBuilder'
import { OsiModel } from '@/widgets/osi/OsiWidget'
import { MacLearning } from '@/widgets/switch/MacLearningWidget'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
  'frame-builder': FrameBuilder,
  'osi-model': OsiModel,
  'mac-learning': MacLearning,
}
