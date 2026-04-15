import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="gradient-primary text-light shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-2xl">☕</span>
            <span className="font-bold text-xl text-accent">NeoCafeIA</span>
          </div>
          <ul className="flex gap-8 list-none">
            <li>
              <a href="#inicio" className="hover:text-accent transition-colors">
                Inicio
              </a>
            </li>
            <li>
              <a href="#caracteristicas" className="hover:text-accent transition-colors">
                Características
              </a>
            </li>
            <li>
              <Link href="/chat" className="hover:text-accent transition-colors">
                Chat
              </Link>
            </li>
          </ul>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="inicio" className="gradient-hero text-white py-20 text-center relative overflow-hidden">
        <div className="max-w-4xl mx-auto px-4 relative z-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">Bienvenido a NeoCafeIA</h1>
          <p className="text-xl md:text-2xl mb-8 text-accent-light">
            Tu asistente inteligente de cafetería impulsado por IA
          </p>
          <p className="text-lg mb-12 leading-relaxed max-w-2xl mx-auto">
            Descubre nuestro menú completo, obtén recomendaciones personalizadas y disfruta de una experiencia de compra única con la ayuda de nuestro asistente de IA.
          </p>
          <Link
            href="/chat"
            className="btn-secondary inline-block text-lg font-bold hover:scale-105 transition-transform"
          >
            Comenzar a Chatear →
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section id="caracteristicas" className="py-20 bg-white">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12 text-dark">Características</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="card">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold mb-3 text-primary">IA Inteligente</h3>
              <p className="text-gray-600">
                Potenciada por múltiples proveedores de IA incluyendo Gemini, OpenAI y Claude para respuestas precisas.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="card">
              <div className="text-4xl mb-4">📋</div>
              <h3 className="text-xl font-bold mb-3 text-primary">Menú Completo</h3>
              <p className="text-gray-600">
                Explora nuestras bebidas, postres, promociones y combos especiales, todo en un solo lugar.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="card">
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-xl font-bold mb-3 text-primary">Recomendaciones</h3>
              <p className="text-gray-600">
                Obtén sugerencias personalizadas basadas en tus preferencias y el historial de conversación.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="gradient-primary text-light py-8 text-center">
        <p>&copy; 2025 NeoCafeIA. Todos los derechos reservados.</p>
      </footer>
    </div>
  );
}
