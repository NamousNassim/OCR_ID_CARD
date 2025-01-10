"use client";
import { useState, useEffect } from 'react';
import { Menu, X, User, Search, Moon, Sun } from 'lucide-react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { title: 'Home', href: '/' },
    { title: 'About', href: '/about' },
    { title: 'Contact', href: '/contact' },
    { title: 'Register', href: '/register' },
    { title: 'Login', href: '/login' },
  ];

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white/80 backdrop-blur-md shadow-md' : 'bg-white'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <a href="/" className="flex items-center">
              <span className="text-2xl font-bold text-indigo-600">Logo</span>
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-4">
              {navLinks.map((link) => (
                <a
                  key={link.title}
                  href={link.href}
                  className="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200"
                >
                  {link.title}
                </a>
              ))}
            </div>
          </div>

          {/* Right side buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Search Bar */}
            <div className="relative">
              <div
                className={`absolute right-0 top-0 transition-all duration-300 ${
                  isSearchOpen ? 'w-64 opacity-100' : 'w-0 opacity-0'
                }`}
              >
                <input
                  type="text"
                  placeholder="Search..."
                  className="w-full px-4 py-1 border border-gray-300 rounded-full focus:outline-none focus:border-indigo-500"
                />
              </div>
              <button
                onClick={() => setIsSearchOpen(!isSearchOpen)}
                className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-200"
              >
                <Search size={20} className="text-gray-600" />
              </button>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-200"
            >
              {isDarkMode ? (
                <Sun size={20} className="text-gray-600" />
              ) : (
                <Moon size={20} className="text-gray-600" />
              )}
            </button>

            {/* User Profile */}
            <button className="p-2 rounded-full hover:bg-gray-100 transition-colors duration-200">
              <User size={20} className="text-gray-600" />
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className={`md:hidden transition-all duration-300 ease-in-out ${
        isOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
      } overflow-hidden`}>
        <div className="px-2 pt-2 pb-3 space-y-1 bg-white shadow-lg rounded-b-lg">
          {navLinks.map((link) => (
            <a
              key={link.title}
              href={link.href}
              className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 transition-all duration-200"
            >
              {link.title}
            </a>
          ))}
          <div className="flex items-center space-x-2 px-3 py-2">
            <button className="p-2 rounded-full hover:bg-gray-100">
              <Search size={20} className="text-gray-600" />
            </button>
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className="p-2 rounded-full hover:bg-gray-100"
            >
              {isDarkMode ? (
                <Sun size={20} className="text-gray-600" />
              ) : (
                <Moon size={20} className="text-gray-600" />
              )}
            </button>
            <button className="p-2 rounded-full hover:bg-gray-100">
              <User size={20} className="text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}