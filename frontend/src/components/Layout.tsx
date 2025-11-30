import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Dog, 
  Activity, 
  Calendar, 
  LogOut, 
  Menu,
  X
} from 'lucide-react';

import ThemeToggle from './ThemeToggle';

export default function Layout() {
  const { logout } = useAuth();
  // ... lines 15-17 ...
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  // ... lines 20-28 ...

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col md:flex-row text-gray-900 dark:text-gray-100">
      {/* Mobile Header */}
      <div className="md:hidden bg-white dark:bg-gray-800 p-4 shadow-sm flex justify-between items-center">
        <h1 className="font-bold text-xl text-blue-600 dark:text-blue-400">DogManager</h1>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-gray-600 dark:text-gray-300">
            {isMobileMenuOpen ? <X /> : <Menu />}
          </button>
        </div>
      </div>

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 shadow-lg transform transition-transform duration-200 ease-in-out
        md:translate-x-0 md:relative md:shadow-none md:border-r dark:border-gray-700
        ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="p-6 flex justify-between items-center">
          <h1 className="font-bold text-2xl text-blue-600 dark:text-blue-400 flex items-center gap-2">
            <Dog /> DogManager
          </h1>
        </div>
        
        <nav className="px-4 space-y-2 mt-4">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => setIsMobileMenuOpen(false)}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                location.pathname === item.path 
                  ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 font-medium' 
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              {item.icon}
              {item.label}
            </Link>
          ))}
          
          <div className="hidden md:block px-4 py-2 mt-2">
             <div className="flex items-center gap-3 px-4 py-2 rounded-lg text-gray-600 dark:text-gray-400">
                <ThemeToggle />
                <span className="text-sm">Theme</span>
             </div>
          </div>

          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-red-50 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400 transition-colors mt-8"
          >
            <LogOut size={20} />
            Logout
          </button>
        </nav>
      </div>
      
      {/* ... Rest of component ... */}

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <main className="p-4 md:p-8 max-w-7xl mx-auto">
          <Outlet />
        </main>
      </div>
      
      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/20 z-40 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </div>
  );
}

