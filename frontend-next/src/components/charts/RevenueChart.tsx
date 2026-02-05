"use client"

import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { formatCurrency } from '@/lib/utils'

interface ChartData {
  name: string
  value: number
  previous?: number
}

interface RevenueChartProps {
  data: ChartData[]
  title: string
  type?: 'line' | 'area' | 'bar'
}

interface TooltipPayload {
  value: number
  payload: ChartData
}

interface CustomTooltipProps {
  active?: boolean
  payload?: TooltipPayload[]
}

export function RevenueChart({ data, title, type = 'area' }: RevenueChartProps) {
  // Validação de dados para evitar erros de SVG path
  const chartData = data && data.length > 0 ? data : [{ name: 'Sem dados', value: 0 }]

  const CustomTooltip = ({ active, payload }: CustomTooltipProps) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass rounded-lg p-3 shadow-lg border border-border">
          <p className="font-medium">{payload[0].payload.name}</p>
          <p className="text-sm text-primary font-semibold">
            {formatCurrency(payload[0].value)}
          </p>
          {payload[0].payload.previous && (
            <p className="text-xs text-muted-foreground">
              Anterior: {formatCurrency(payload[0].payload.previous)}
            </p>
          )}
        </div>
      )
    }
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <CardTitle className="text-lg font-semibold">{title}</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            {type === 'area' ? (
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#06B6D4" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorPrevious" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#94A3B8" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#94A3B8" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                <XAxis
                  dataKey="name"
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickFormatter={(value) => `R$ ${(value / 1000).toFixed(0)}k`}
                />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke="#06B6D4"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorValue)"
                  animationDuration={1500}
                />
                {chartData[0]?.previous !== undefined && (
                  <Area
                    type="monotone"
                    dataKey="previous"
                    stroke="#94A3B8"
                    strokeWidth={1}
                    fillOpacity={1}
                    fill="url(#colorPrevious)"
                    strokeDasharray="5 5"
                    animationDuration={1500}
                  />
                )}
              </AreaChart>
            ) : type === 'line' ? (
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                <XAxis
                  dataKey="name"
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickFormatter={(value) => `R$ ${(value / 1000).toFixed(0)}k`}
                />
                <Tooltip content={<CustomTooltip />} />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#06B6D4"
                  strokeWidth={3}
                  dot={{ fill: '#06B6D4', r: 5 }}
                  activeDot={{ r: 7 }}
                  animationDuration={1500}
                />
                {chartData[0]?.previous !== undefined && (
                  <Line
                    type="monotone"
                    dataKey="previous"
                    stroke="#94A3B8"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    dot={{ fill: '#94A3B8', r: 3 }}
                    animationDuration={1500}
                  />
                )}
              </LineChart>
            ) : (
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
                <XAxis
                  dataKey="name"
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                />
                <YAxis
                  stroke="hsl(var(--muted-foreground))"
                  fontSize={12}
                  tickFormatter={(value) => `R$ ${(value / 1000).toFixed(0)}k`}
                />
                <Tooltip content={<CustomTooltip />} />
                <Bar
                  dataKey="value"
                  fill="url(#colorValue)"
                  radius={[8, 8, 0, 0]}
                  animationDuration={1500}
                />
                {chartData[0]?.previous !== undefined && (
                  <Bar
                    dataKey="previous"
                    fill="#94A3B8"
                    opacity={0.5}
                    radius={[8, 8, 0, 0]}
                    animationDuration={1500}
                  />
                )}
              </BarChart>
            )}
          </ResponsiveContainer>

          {/* Legend */}
          <div className="flex items-center justify-center gap-6 mt-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-primary" />
              <span className="text-sm text-muted-foreground">Atual</span>
            </div>
            {chartData[0]?.previous !== undefined && (
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-muted-foreground opacity-50" />
                <span className="text-sm text-muted-foreground">Anterior</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}