import type { ComponentType } from 'react'
import { VlanSwitch } from '@/widgets/VlanSwitch'

export const WIDGETS: Record<string, ComponentType> = {
  'vlan-switch': VlanSwitch,
}
