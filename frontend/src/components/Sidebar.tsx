import React from 'react';
import { MessageSquare, Upload, Settings, Database, GitBranch, Moon, Sun } from 'lucide-react';
import { useTheme } from '../hooks/useTheme';

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange }) => {
  const { isDark, toggleTheme } = useTheme();
  
  const tabs = [
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    // { id: 'upload', label: 'Tải lên', icon: Upload },
    { id: 'collections', label: 'Bộ sưu tập', icon: Database },
    // { id: 'graph', label: 'Knowledge Graph', icon: GitBranch },
    { id: 'settings', label: 'Cài đặt', icon: Settings },
  ];

  return (
    <div className="w-64 bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-colors">
      {/* Logo/Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-800 dark:text-white">RAG System</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">Hybrid RAG với Knowledge Graph</p>
          </div>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title={isDark ? 'Chuyển sang chế độ sáng' : 'Chuyển sang chế độ tối'}
          >
            {isDark ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <li key={tab.id}>
                <button
                  onClick={() => onTabChange(tab.id)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-primary-500 text-white'
                      : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{tab.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <div className="text-xs text-gray-500 dark:text-gray-400">
          <p>Phiên bản: 1.0.0</p>
          <p>Powered by HybridRAG</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
