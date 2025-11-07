"use client"

import { motion } from 'framer-motion'
import { useState } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import {
  Check,
  ArrowRight,
  Users,
  DollarSign,
  Calendar,
  TrendingUp,
  Clock,
  Shield,
  BarChart3,
  Zap,
  Star,
  MessageCircle,
  Award,
  X
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'

export default function LandingPage() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const features = [
    {
      icon: Users,
      title: "Gestão Completa de Alunos",
      description: "Cadastro detalhado, histórico de pagamentos e controle de frequência em poucos cliques.",
      color: "from-cyan-500 to-blue-500"
    },
    {
      icon: DollarSign,
      title: "Financeiro Inteligente",
      description: "Dashboard financeiro em tempo real, controle de inadimplência e relatórios automáticos.",
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: Calendar,
      title: "Grade de Horários Dinâmica",
      description: "Visualização semanal, controle de vagas, fila de espera e alocação de professores.",
      color: "from-purple-500 to-pink-500"
    },
    {
      icon: MessageCircle,
      title: "WhatsApp Integrado",
      description: "Envie lembretes de pagamento e avisos importantes direto para o WhatsApp dos alunos.",
      color: "from-green-400 to-emerald-600"
    },
    {
      icon: Award,
      title: "Gestão de Professores",
      description: "Cadastro de instrutores, atribuição de turmas e controle de especialidades.",
      color: "from-orange-500 to-red-500"
    },
    {
      icon: BarChart3,
      title: "Relatórios e Métricas",
      description: "Acompanhe ocupação, receita, inadimplência e crescimento com gráficos visuais.",
      color: "from-indigo-500 to-purple-500"
    }
  ]

  const benefits = [
    "Economize 15+ horas por semana em tarefas administrativas",
    "Reduza inadimplência em até 40% com lembretes automáticos",
    "Acabe com planilhas e papelada bagunçada",
    "Acesse de qualquer lugar, qualquer dispositivo",
    "Dados seguros com backup automático na nuvem",
    "Suporte dedicado em português",
    "Atualizações e melhorias constantes incluídas",
    "Sem custos escondidos ou taxas surpresa"
  ]

  const testimonials = [
    {
      name: "Marina Silva",
      role: "Proprietária - Aqua Sports",
      image: "MS",
      quote: "Antes do AquaFlow, eu perdia horas organizando horários e correndo atrás de pagamentos. Agora tudo está automatizado e centralizado. Melhor investimento que já fiz!",
      rating: 5
    },
    {
      name: "Roberto Costa",
      role: "Gestor - Natação Total",
      image: "RC",
      quote: "A inadimplência caiu drasticamente depois que começamos a usar os lembretes automáticos. O sistema paga por si só em economia de tempo.",
      rating: 5
    },
    {
      name: "Ana Paula",
      role: "Diretora - Centro Aquático Vida",
      image: "AP",
      quote: "Interface super intuitiva, minha equipe aprendeu em menos de 30 minutos. O suporte é excelente e sempre disponível quando precisamos.",
      rating: 5
    }
  ]

  const faqs = [
    {
      q: "Preciso instalar alguma coisa?",
      a: "Não! O AquaFlow Pro funciona 100% na nuvem. Basta acessar pelo navegador de qualquer computador, tablet ou celular."
    },
    {
      q: "Meus dados estão seguros?",
      a: "Sim! Utilizamos criptografia de ponta a ponta e backup automático diário. Seus dados estão mais seguros do que em planilhas locais."
    },
    {
      q: "Consigo importar meus dados atuais?",
      a: "Sim! Nossa equipe te auxilia na migração dos seus dados atuais sem custo adicional."
    },
    {
      q: "E se eu não gostar?",
      a: "Oferecemos garantia de 7 dias. Se não ficar satisfeito, devolvemos 100% do valor sem perguntas."
    },
    {
      q: "Tem limite de alunos?",
      a: "Não! Você pode cadastrar quantos alunos, professores e turmas precisar. Sem limites."
    },
    {
      q: "Preciso de conhecimento técnico?",
      a: "Zero! O sistema foi feito para ser simples. Se você usa WhatsApp, vai usar o AquaFlow tranquilamente."
    }
  ]

  const handleGetStarted = () => {
    const element = document.getElementById('pricing')
    element?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header/Nav */}
      <nav className="fixed w-full bg-white/90 backdrop-blur-md z-50 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
                <svg width="20" height="20" viewBox="0 0 100 100" fill="none">
                  <path d="M10,50 Q30,40 50,50 T90,50" stroke="white" strokeWidth="8" fill="none" strokeLinecap="round"/>
                </svg>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
                AquaFlow Pro
              </span>
            </div>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-gray-600 hover:text-cyan-600 transition-colors">Recursos</a>
              <a href="#benefits" className="text-gray-600 hover:text-cyan-600 transition-colors">Benefícios</a>
              <a href="#pricing" className="text-gray-600 hover:text-cyan-600 transition-colors">Preços</a>
              <a href="#faq" className="text-gray-600 hover:text-cyan-600 transition-colors">FAQ</a>
              <Link href="/login">
                <Button variant="ghost">Entrar</Button>
              </Link>
              <Button onClick={handleGetStarted} className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700">
                Começar Agora
              </Button>
            </div>

            {/* Mobile Menu Button */}
            <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              {isMenuOpen ? <X className="h-6 w-6" /> : <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-100 bg-white">
            <div className="px-4 py-6 space-y-4">
              <a href="#features" className="block text-gray-600 hover:text-cyan-600">Recursos</a>
              <a href="#benefits" className="block text-gray-600 hover:text-cyan-600">Benefícios</a>
              <a href="#pricing" className="block text-gray-600 hover:text-cyan-600">Preços</a>
              <a href="#faq" className="block text-gray-600 hover:text-cyan-600">FAQ</a>
              <Link href="/login">
                <Button variant="ghost" className="w-full">Entrar</Button>
              </Link>
              <Button onClick={handleGetStarted} className="w-full bg-gradient-to-r from-cyan-500 to-blue-600">
                Começar Agora
              </Button>
            </div>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-cyan-50 via-blue-50 to-white">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="inline-block mb-4 px-4 py-2 bg-cyan-100 rounded-full">
                <span className="text-cyan-700 font-semibold text-sm">🚀 Sistema Completo de Gestão Aquática</span>
              </div>

              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
                Pare de Perder Tempo com{' '}
                <span className="bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
                  Planilhas
                </span>
              </h1>

              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Gerencie sua academia de natação com <strong>profissionalismo</strong>.
                Controle financeiro, horários, alunos e professores em um só lugar.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <Button
                  size="lg"
                  onClick={handleGetStarted}
                  className="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-lg px-8 py-6"
                >
                  Comece Grátis por 7 Dias
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </div>

              <div className="flex items-center gap-8 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Check className="h-5 w-5 text-green-600" />
                  <span>Sem cartão de crédito</span>
                </div>
                <div className="flex items-center gap-2">
                  <Check className="h-5 w-5 text-green-600" />
                  <span>Cancelamento fácil</span>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="relative rounded-2xl overflow-hidden shadow-2xl border-8 border-white">
                <Image
                  src="/api/placeholder/800/600"
                  alt="Dashboard AquaFlow Pro"
                  width={800}
                  height={600}
                  className="w-full h-auto"
                />
                {/* Floating Stats */}
                <div className="absolute top-4 right-4 bg-white rounded-xl p-4 shadow-lg">
                  <div className="flex items-center gap-2 text-sm">
                    <TrendingUp className="h-4 w-4 text-green-600" />
                    <span className="font-semibold text-green-600">+32% Receita</span>
                  </div>
                </div>
                <div className="absolute bottom-4 left-4 bg-white rounded-xl p-4 shadow-lg">
                  <div className="flex items-center gap-2 text-sm">
                    <Users className="h-4 w-4 text-cyan-600" />
                    <span className="font-semibold">156 Alunos Ativos</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Social Proof */}
      <section className="py-12 bg-white border-y border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="text-center md:text-left">
              <p className="text-gray-500 mb-2">Confiado por academias em todo Brasil</p>
            </div>
            <div className="flex items-center gap-12 opacity-50">
              <div className="text-2xl font-bold text-gray-400">Academia+</div>
              <div className="text-2xl font-bold text-gray-400">AquaFit</div>
              <div className="text-2xl font-bold text-gray-400">NataTotal</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Tudo que Você Precisa em Um Só Lugar
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Chega de usar 10 ferramentas diferentes. Centralize toda gestão da sua academia.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="h-full hover:shadow-xl transition-shadow border-0 bg-gradient-to-br from-white to-gray-50">
                  <CardContent className="p-6">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.color} p-2.5 mb-4`}>
                      <feature.icon className="h-full w-full text-white" />
                    </div>
                    <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-cyan-50 to-blue-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Por Que Escolher o AquaFlow Pro?
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Não é só um sistema. É a solução completa que vai transformar
                a forma como você administra sua academia.
              </p>

              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.05 }}
                    className="flex items-start gap-3"
                  >
                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center mt-0.5">
                      <Check className="h-4 w-4 text-white" />
                    </div>
                    <span className="text-gray-700">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </div>

            <div className="relative">
              <div className="grid grid-cols-2 gap-4">
                <Card className="p-6 text-center border-0 bg-white shadow-lg">
                  <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <div className="text-3xl font-bold text-gray-900">40%</div>
                  <div className="text-sm text-gray-600">Redução de Inadimplência</div>
                </Card>
                <Card className="p-6 text-center border-0 bg-white shadow-lg mt-8">
                  <Clock className="h-8 w-8 text-cyan-600 mx-auto mb-2" />
                  <div className="text-3xl font-bold text-gray-900">15h</div>
                  <div className="text-sm text-gray-600">Economizadas por Semana</div>
                </Card>
                <Card className="p-6 text-center border-0 bg-white shadow-lg">
                  <Users className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <div className="text-3xl font-bold text-gray-900">98%</div>
                  <div className="text-sm text-gray-600">Satisfação dos Clientes</div>
                </Card>
                <Card className="p-6 text-center border-0 bg-white shadow-lg mt-8">
                  <Zap className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                  <div className="text-3xl font-bold text-gray-900">24/7</div>
                  <div className="text-sm text-gray-600">Sistema Sempre Online</div>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              O Que Nossos Clientes Dizem
            </h2>
            <p className="text-xl text-gray-600">
              Centenas de academias já transformaram sua gestão
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="h-full border-0 shadow-lg hover:shadow-xl transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex gap-1 mb-4">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                      ))}
                    </div>
                    <p className="text-gray-700 mb-6 italic">&ldquo;{testimonial.quote}&rdquo;</p>
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold">
                        {testimonial.image}
                      </div>
                      <div>
                        <div className="font-semibold text-gray-900">{testimonial.name}</div>
                        <div className="text-sm text-gray-600">{testimonial.role}</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-900 to-gray-800 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-4">
            Preço Simples e Transparente
          </h2>
          <p className="text-xl text-gray-300 mb-12">
            Um único plano com tudo incluído. Sem surpresas.
          </p>

          <Card className="max-w-lg mx-auto border-0 bg-white text-gray-900 shadow-2xl">
            <CardContent className="p-8">
              <div className="text-center mb-8">
                <div className="text-5xl font-bold mb-2">
                  R$ 197
                  <span className="text-2xl text-gray-600 font-normal">/mês</span>
                </div>
                <p className="text-gray-600">Cancele quando quiser</p>
              </div>

              <div className="space-y-4 mb-8 text-left">
                {[
                  "Alunos e professores ilimitados",
                  "Gestão financeira completa",
                  "Grade de horários dinâmica",
                  "WhatsApp integrado",
                  "Relatórios e dashboards",
                  "Backup automático diário",
                  "Suporte prioritário",
                  "Atualizações gratuitas",
                  "7 dias de teste grátis",
                  "Garantia de 7 dias"
                ].map((item, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <Check className="h-5 w-5 text-green-600 flex-shrink-0" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>

              <Button
                size="lg"
                className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-lg py-6"
              >
                Começar Teste Grátis
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>

              <p className="text-sm text-gray-600 text-center mt-4">
                Não é necessário cartão de crédito para o teste
              </p>
            </CardContent>
          </Card>

          <div className="mt-12 flex items-center justify-center gap-8 text-sm text-gray-400">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              <span>Pagamento Seguro</span>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="h-5 w-5" />
              <span>Dados Protegidos</span>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Perguntas Frequentes
            </h2>
            <p className="text-xl text-gray-600">
              Tudo que você precisa saber sobre o AquaFlow Pro
            </p>
          </div>

          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <Card key={index} className="border-0 shadow-md">
                <CardContent className="p-6">
                  <h3 className="font-semibold text-lg mb-2 text-gray-900">{faq.q}</h3>
                  <p className="text-gray-600">{faq.a}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-cyan-600 to-blue-700 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-6">
            Pronto para Transformar sua Academia?
          </h2>
          <p className="text-xl mb-8 text-cyan-50">
            Junte-se a centenas de academias que já economizam tempo e aumentam receita com o AquaFlow Pro
          </p>
          <Button
            size="lg"
            className="bg-white text-cyan-600 hover:bg-gray-100 text-lg px-8 py-6"
          >
            Começar Teste Grátis por 7 Dias
            <ArrowRight className="ml-2 h-5 w-5" />
          </Button>
          <p className="text-sm text-cyan-100 mt-4">
            Não precisa cadastrar cartão de crédito • Cancele quando quiser
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center">
                  <svg width="20" height="20" viewBox="0 0 100 100" fill="none">
                    <path d="M10,50 Q30,40 50,50 T90,50" stroke="white" strokeWidth="8" fill="none" strokeLinecap="round"/>
                  </svg>
                </div>
                <span className="text-white font-bold">AquaFlow Pro</span>
              </div>
              <p className="text-sm">
                Sistema profissional de gestão para academias de natação e centros aquáticos.
              </p>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Produto</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#features" className="hover:text-white">Recursos</a></li>
                <li><a href="#pricing" className="hover:text-white">Preços</a></li>
                <li><a href="#" className="hover:text-white">Demo</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">Sobre</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Contato</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">Privacidade</a></li>
                <li><a href="#" className="hover:text-white">Termos de Uso</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-8 text-sm text-center">
            <p>© 2025 AquaFlow Pro. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

function Lock({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
    </svg>
  )
}
