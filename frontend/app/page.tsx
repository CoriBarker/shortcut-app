import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-8">Welcome to Shortcut App</h1>
      <p className="text-xl mb-8 text-center">
        Your personal shortcut management solution
      </p>
      <Link 
        href="/signup" 
        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
      >
        Get Started
      </Link>
    </main>
  );
} 