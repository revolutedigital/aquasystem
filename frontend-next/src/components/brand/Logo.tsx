"use client"

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'full' | 'icon' | 'text'
  animated?: boolean
  className?: string
}

const sizes = {
  sm: { width: 32, height: 32, text: 'text-lg', tagline: 'text-[8px]' },
  md: { width: 44, height: 44, text: 'text-xl', tagline: 'text-[10px]' },
  lg: { width: 60, height: 60, text: 'text-2xl', tagline: 'text-xs' },
  xl: { width: 88, height: 88, text: 'text-4xl', tagline: 'text-sm' }
}

export function Logo({ size = 'md', variant = 'full', animated = false, className = '' }: LogoProps) {
  const { width, height, text, tagline } = sizes[size]
  const uniqueId = `logo-${size}-${variant}`

  const AquaFlowIcon = () => (
    <svg
      width={width}
      height={height}
      viewBox="0 0 120 120"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="AquaFlow Pro Logo"
      className={animated ? 'animate-pulse-subtle' : ''}
    >
      <defs>
        {/* Premium gradient - Deep ocean to crystal blue */}
        <linearGradient id={`${uniqueId}-primary`} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#0369A1" />
          <stop offset="35%" stopColor="#0891B2" />
          <stop offset="70%" stopColor="#06B6D4" />
          <stop offset="100%" stopColor="#22D3EE" />
        </linearGradient>

        {/* Accent gradient for highlights */}
        <linearGradient id={`${uniqueId}-accent`} x1="50%" y1="0%" x2="50%" y2="100%">
          <stop offset="0%" stopColor="#67E8F9" />
          <stop offset="100%" stopColor="#06B6D4" />
        </linearGradient>

        {/* Radial glow effect */}
        <radialGradient id={`${uniqueId}-glow`} cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#22D3EE" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#0891B2" stopOpacity="0" />
        </radialGradient>

        {/* Drop shadow filter */}
        <filter id={`${uniqueId}-shadow`} x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#0369A1" floodOpacity="0.25"/>
        </filter>

        {/* Clip path for the droplet shape */}
        <clipPath id={`${uniqueId}-dropletClip`}>
          <path d="M60 8 C60 8 95 45 95 70 C95 89.33 79.33 105 60 105 C40.67 105 25 89.33 25 70 C25 45 60 8 60 8 Z"/>
        </clipPath>
      </defs>

      {/* Background glow */}
      <circle
        cx="60"
        cy="65"
        r="45"
        fill={`url(#${uniqueId}-glow)`}
        opacity="0.6"
      />

      {/* Main droplet shape - represents water/aqua */}
      <path
        d="M60 12 C60 12 92 47 92 70 C92 87.67 77.67 102 60 102 C42.33 102 28 87.67 28 70 C28 47 60 12 60 12 Z"
        fill={`url(#${uniqueId}-primary)`}
        filter={`url(#${uniqueId}-shadow)`}
      />

      {/* Inner highlight - glass effect */}
      <ellipse
        cx="48"
        cy="50"
        rx="12"
        ry="18"
        fill="white"
        opacity="0.15"
        transform="rotate(-20 48 50)"
      />

      {/* Wave lines inside droplet */}
      <g clipPath={`url(#${uniqueId}-dropletClip)`}>
        <path
          d="M20 65 Q40 55 60 65 T100 65"
          stroke="white"
          strokeWidth="2.5"
          fill="none"
          strokeLinecap="round"
          opacity="0.4"
          className={animated ? 'animate-wave' : ''}
        />
        <path
          d="M20 75 Q40 65 60 75 T100 75"
          stroke="white"
          strokeWidth="2"
          fill="none"
          strokeLinecap="round"
          opacity="0.25"
          className={animated ? 'animate-wave-delay-1' : ''}
        />
        <path
          d="M20 85 Q40 75 60 85 T100 85"
          stroke="white"
          strokeWidth="1.5"
          fill="none"
          strokeLinecap="round"
          opacity="0.15"
          className={animated ? 'animate-wave-delay-2' : ''}
        />
      </g>

      {/* Stylized "A" letter for AquaFlow */}
      <path
        d="M60 38 L45 72 L51 72 L54 64 L66 64 L69 72 L75 72 L60 38 Z M56 59 L60 48 L64 59 L56 59 Z"
        fill="white"
        opacity="0.95"
      />

      {/* Floating bubbles */}
      <circle cx="75" cy="85" r="3" fill="white" opacity="0.3" className={animated ? 'animate-bubble' : ''} />
      <circle cx="45" cy="90" r="2" fill="white" opacity="0.25" className={animated ? 'animate-bubble-delay' : ''} />
      <circle cx="68" cy="92" r="2.5" fill="white" opacity="0.2" className={animated ? 'animate-bubble-delay-2' : ''} />

      {/* Outer ring - premium badge effect */}
      <circle
        cx="60"
        cy="60"
        r="56"
        stroke={`url(#${uniqueId}-accent)`}
        strokeWidth="1.5"
        fill="none"
        opacity="0.3"
        strokeDasharray="8 4"
        className={animated ? 'animate-spin-slow' : ''}
        style={{ transformOrigin: '60px 60px' }}
      />
    </svg>
  )

  if (variant === 'icon') {
    return (
      <div className={className}>
        <AquaFlowIcon />
      </div>
    )
  }

  if (variant === 'text') {
    return (
      <span className={`font-bold tracking-tight bg-gradient-to-r from-sky-700 via-cyan-600 to-teal-500 bg-clip-text text-transparent ${text} ${className}`}>
        AquaFlow<span className="font-extrabold">Pro</span>
      </span>
    )
  }

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <AquaFlowIcon />
      <div className="flex flex-col justify-center">
        <span className={`font-bold tracking-tight leading-none bg-gradient-to-r from-sky-700 via-cyan-600 to-teal-500 bg-clip-text text-transparent ${text}`}>
          AquaFlow<span className="font-extrabold">Pro</span>
        </span>
        <span className={`${tagline} text-muted-foreground/80 tracking-wider uppercase mt-0.5`}>
          Gestão Aquática Inteligente
        </span>
      </div>
    </div>
  )
}
