import React, { useState, useEffect } from 'react';
import { Database, Search, FileText, BarChart3 } from 'lucide-react';
import { chatAPI } from '../services/api';

interface Collection {
  name: string;
  count: number;
  status: string;
}

const CollectionsView: React.FC = () => {
  const [collections, setCollections] = useState<Collection[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadCollections();
  }, []);

  const loadCollections = async () => {
    try {
      setIsLoading(true);
      const data = await chatAPI.getCollections();
      setCollections(data);
    } catch (error) {
      console.error('Error loading collections:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    try {
      setIsLoading(true);
      // Implement search functionality
      console.log('Searching for:', searchQuery);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">Bộ sưu tập tài liệu</h2>
        <p className="text-gray-600 dark:text-gray-300">Quản lý và tìm kiếm trong các bộ sưu tập tài liệu</p>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <div className="flex space-x-2">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 dark:text-gray-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Tìm kiếm trong tài liệu..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={!searchQuery.trim() || isLoading}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
          >
            {isLoading ? 'Đang tìm...' : 'Tìm kiếm'}
          </button>
        </div>
      </div>

      {/* Collections Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {collections.map((collection) => (
          <div
            key={collection.name}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <Database className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-800 dark:text-white">{collection.name}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">{collection.status}</p>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-300">Số lượng tài liệu:</span>
                <span className="font-medium dark:text-white">{collection.count}</span>
              </div>
              
              <div className="flex space-x-2">
                <button className="flex-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 py-2 px-3 rounded-md text-sm hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
                  <FileText className="h-4 w-4 inline mr-1" />
                  Xem chi tiết
                </button>
                <button className="flex-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 py-2 px-3 rounded-md text-sm hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors">
                  <BarChart3 className="h-4 w-4 inline mr-1" />
                  Phân tích
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {collections.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <Database className="mx-auto h-12 w-12 text-gray-300 dark:text-gray-600 mb-4" />
          <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-2">Chưa có bộ sưu tập nào</h3>
          <p className="text-gray-600 dark:text-gray-300">Hãy tải lên tài liệu để tạo bộ sưu tập đầu tiên</p>
        </div>
      )}

      {isLoading && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải...</p>
        </div>
      )}
    </div>
  );
};

export default CollectionsView;
