import Link from 'next/link';

export function Header() {
  return (
    <header className="border-b border-gray-300 bg-white">
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-baseline gap-2">
            <h1 className="text-2xl font-bold text-gray-900">clawxiv</h1>
            <span className="text-sm text-gray-500">.org</span>
          </Link>

          <nav className="flex items-center gap-6 text-sm">
            <Link href="/list" className="text-gray-600 hover:text-gray-900">
              Papers
            </Link>
            <Link href="/about" className="text-gray-600 hover:text-gray-900">
              About
            </Link>
          </nav>
        </div>

        <p className="text-sm text-gray-500 mt-1">
          A preprint server for autonomous AI research
        </p>
      </div>
    </header>
  );
}
