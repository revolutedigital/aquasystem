"use client"

import { motion } from 'framer-motion'
import { LucideIcon } from 'lucide-react'
import CountUp from 'react-countup'
import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface StatCardProps {
  title: string
  value: number
  subtitle?: string
  icon: LucideIcon
  trend?: {
    value: number
    isPositive: boolean
  }
  prefix?: string
  suffix?: string
  decimals?: number
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info'
  delay?: number
  className?: string
}

const colorClasses = {
  primary: 'from-cyan-500 to-blue-500',
  success: 'from-green-500 to-emerald-500',
  warning: 'from-orange-500 to-amber-500',
  error: 'from-red-500 to-rose-500',
  info: 'from-blue-500 to-indigo-500',
}

export function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  prefix = '',
  suffix = '',
  decimals = 0,
  color = 'primary',
  delay = 0,
  className,
}: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
    >
      <Card className={cn("relative overflow-hidden hover:shadow-lg transition-all", className)}>
        <CardContent className="p-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-muted-foreground mb-2">
                {title}
              </p>
              <div className="flex items-baseline gap-2">
                <h3 className="text-3xl font-bold tracking-tight">
                  {prefix}
                  <CountUp
                    end={value}
                    duration={2}
                    decimals={decimals}
                    separator="."
                    decimal=","
                    delay={delay}
                  />
                  {suffix}
                </h3>
                {trend && (
                  <motion.span
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: delay + 0.5 }}
                    className={cn(
                      "text-sm font-medium flex items-center gap-1",
                      trend.isPositive ? "text-success" : "text-error"
                    )}
                  >
                    {trend.isPositive ? '↑' : '↓'}
                    {Math.abs(trend.value)}%
                  </motion.span>
                )}
              </div>
              {subtitle && (
                <p className="text-xs text-muted-foreground mt-1">
                  {subtitle}
                </p>
              )}
            </div>

            <motion.div
              className={cn(
                "h-12 w-12 rounded-xl bg-gradient-to-br flex items-center justify-center shadow-lg",
                colorClasses[color]
              )}
              whileHover={{ scale: 1.1, rotate: 5 }}
              transition={{ type: "spring", stiffness: 400 }}
            >
              <Icon className="h-6 w-6 text-white" />
            </motion.div>
          </div>
        </CardContent>

        {/* Decorative gradient overlay */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-transparent via-transparent to-primary/5 pointer-events-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: delay + 0.3 }}
        />
      </Card>
    </motion.div>
  )
}