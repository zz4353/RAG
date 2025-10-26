import React, { createContext, useEffect, useState } from 'react';

interface ThemeContextType {
  isDark: boolean;
  toggleTheme: () => void;
}

export const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [isDark, setIsDark] = useState(false);

  // Khởi tạo theme từ localStorage sau khi component mount
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    let initialTheme = false;
    
    // Kiểm tra localStorage
    try {
      const saved = localStorage.getItem('rag-theme');
      if (saved) {
        initialTheme = saved === 'dark';
      } else {
        // Nếu chưa có setting, dùng system preference
        try {
          initialTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        } catch (error) {
          console.warn('Cannot access matchMedia:', error);
        }
      }
    } catch (error) {
      console.warn('Cannot access localStorage:', error);
    }
    
    setIsDark(initialTheme);
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    const root = window.document.documentElement;
    
    if (isDark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    
    // Lưu vào localStorage
    try {
      localStorage.setItem('rag-theme', isDark ? 'dark' : 'light');
    } catch (error) {
      console.warn('Cannot save to localStorage:', error);
    }
  }, [isDark]);

  const toggleTheme = () => {
    setIsDark(prev => !prev);
  };

  return (
    <ThemeContext.Provider value={{ isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}