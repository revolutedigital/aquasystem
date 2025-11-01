"use client"

import { motion } from 'framer-motion'

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'full' | 'icon' | 'text'
  animated?: boolean
  className?: string
}

const sizes = {
  sm: { width: 32, height: 32, text: 'text-lg' },
  md: { width: 40, height: 40, text: 'text-xl' },
  lg: { width: 56, height: 56, text: 'text-2xl' },
  xl: { width: 80, height: 80, text: 'text-4xl' }
}

export function Logo({ size = 'md', variant = 'full', animated = false, className = '' }: LogoProps) {
  const { width, height, text } = sizes[size]

  const WaveIcon = () => (
    <svg width={width} height={height} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#0EA5E9" />
          <stop offset="50%" stopColor="#06B6D4" />
          <stop offset="100%" stopColor="#0891B2" />
        </linearGradient>
        <linearGradient id="swimmerGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#0C4A6E" />
          <stop offset="100%" stopColor="#075985" />
        </linearGradient>
      </defs>

      {/* Water waves */}
      <motion.path
        d="M10,50 Q30,40 50,50 T90,50"
        stroke="url(#waveGradient)"
        strokeWidth="8"
        fill="none"
        strokeLinecap="round"
        animate={animated ? {
          d: [
            "M10,50 Q30,40 50,50 T90,50",
            "M10,50 Q30,60 50,50 T90,50",
            "M10,50 Q30,40 50,50 T90,50"
          ]
        } : {}}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.path
        d="M10,65 Q30,55 50,65 T90,65"
        stroke="url(#waveGradient)"
        strokeWidth="6"
        fill="none"
        strokeLinecap="round"
        opacity="0.6"
        animate={animated ? {
          d: [
            "M10,65 Q30,55 50,65 T90,65",
            "M10,65 Q30,75 50,65 T90,65",
            "M10,65 Q30,55 50,65 T90,65"
          ]
        } : {}}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.3 }}
      />
      <motion.path
        d="M10,80 Q30,70 50,80 T90,80"
        stroke="url(#waveGradient)"
        strokeWidth="4"
        fill="none"
        strokeLinecap="round"
        opacity="0.3"
        animate={animated ? {
          d: [
            "M10,80 Q30,70 50,80 T90,80",
            "M10,80 Q30,90 50,80 T90,80",
            "M10,80 Q30,70 50,80 T90,80"
          ]
        } : {}}
        transition={{ duration: 2, repeat: Infinity, ease: "easeInOut", delay: 0.6 }}
      />

      {/* Swimmer silhouette */}
      <motion.g
        animate={animated ? { x: [0, 40, 0] } : {}}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
      >
        {/* Head */}
        <circle
          cx="30"
          cy="35"
          r="6"
          fill="url(#swimmerGradient)"
        />
        {/* Body */}
        <ellipse
          cx="30"
          cy="48"
          rx="8"
          ry="12"
          fill="url(#swimmerGradient)"
        />
        {/* Arms */}
        <motion.path
          d="M22,45 Q18,48 15,45 M38,45 Q42,48 45,45"
          stroke="url(#swimmerGradient)"
          strokeWidth="3"
          strokeLinecap="round"
          fill="none"
          animate={animated ? {
            d: [
              "M22,45 Q18,48 15,45 M38,45 Q42,48 45,45",
              "M22,45 Q18,42 15,45 M38,45 Q42,42 45,45",
              "M22,45 Q18,48 15,45 M38,45 Q42,48 45,45"
            ]
          } : {}}
          transition={{ duration: 1, repeat: Infinity, ease: "easeInOut" }}
        />
      </motion.g>
    </svg>
  )

  if (variant === 'icon') {
    return (
      <div className={className}>
        <WaveIcon />
      </div>
    )
  }

  if (variant === 'text') {
    return (
      <span className={`font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent ${text} ${className}`}>
        AquaFlow Pro
      </span>
    )
  }

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <WaveIcon />
      <div className="flex flex-col">
        <span className={`font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent ${text}`}>
          AquaFlow Pro
        </span>
        <span className="text-xs text-muted-foreground">Sistema de Gestão Aquática</span>
      </div>
    </div>
  )
}