export type Screen = 'home' | 'dives' | 'alldives' | 'sensors' | 'media' | 'network' | 'notifications' | 'help' | 'location' | 'viewmedia' | 'artemis'

export interface Module {
  id: number
  name: string
  status: 'connected' | 'disconnected'
  moduleStatus: string
}

export interface Network {
  ssid: string
  signal: number
  frequency: '2.4GHz' | '5GHz'
  security: 'WPA2' | 'WPA3' | 'Open'
  saved: boolean
}

export interface SensorModule {
  id: number
  name: string
  type: 'camera' | 'sensor' | 'light' | 'communication'
  connected: boolean
  power: number
  sampleRate?: number
  calibrationFile?: string
  moduleStatus: string
}

export interface Mission {
  id: number
  name: string
  configuration: string
  date: string
  duration: string
  location: string
  maxDepth: number
  images: number
  videos: number
  status: string
  calibrationFiles: {
    camera: string
    depthSensor: string
    temperature: string
    conductivity: string
    imu: string
  }
}

export interface MediaFile {
  id: number
  fileName: string
  type: 'video' | 'image' | 'sensor' | 'log'
  diveName: string
  date: string
  size: string
  timestamp: string
  thumbnailUrl?: string
}

export interface MissionData {
  id: number
  name: string
  date: string
  files: number
  totalSize: string
  gpsPosition: string
  duration: string
}

export interface Notification {
  id: number
  type: 'success' | 'warning' | 'info'
  title: string
  message: string
  timestamp: string
  read: boolean
  linkTo?: Screen
}

export interface Tutorial {
  id: number
  title: string
  description: string
  duration: string
  category: 'setup' | 'operation' | 'troubleshooting'
  downloaded: boolean
}

export interface DiveData {
  name: string
  date: string
  duration: string
  maxDepth: string
  location: string
  gpsPosition?: string
  operator?: string
  images?: number
  videos?: number
}
