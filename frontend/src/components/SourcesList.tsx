import React, { useState } from 'react';
import { FileText, ExternalLink, ChevronDown, ChevronRight } from 'lucide-react';

interface Document {
  id: string;
  title: string;
  content: string;
  score?: number;
  source?: string;
}

interface SourcesListProps {
  sources: Document[];
  title?: string;
}

const SourcesList: React.FC<SourcesListProps> = ({ sources, title = "Nguồn tham khảo" }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 border-t border-gray-200 pt-4">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
      >
        {isExpanded ? (
          <ChevronDown className="h-4 w-4" />
        ) : (
          <ChevronRight className="h-4 w-4" />
        )}
        <span>{title} ({sources.length})</span>
      </button>

      {isExpanded && (
        <div className="mt-2 space-y-2">
          {sources.map((source, index) => (
            <div
              key={source.id || index}
              className="bg-gray-50 rounded-lg p-3 border border-gray-200"
            >
              <div className="flex items-start space-x-3">
                <FileText className="h-4 w-4 text-gray-500 mt-0.5 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-gray-800 truncate">
                    {source.title || `Tài liệu ${index + 1}`}
                  </h4>
                  {source.source && (
                    <p className="text-xs text-gray-500 mt-1">{source.source}</p>
                  )}
                  {source.score && (
                    <div className="flex items-center space-x-2 mt-2">
                      <span className="text-xs text-gray-500">Độ liên quan:</span>
                      <div className="flex-1 bg-gray-200 rounded-full h-1.5">
                        <div
                          className="bg-blue-500 h-1.5 rounded-full"
                          style={{ width: `${Math.min(source.score * 100, 100)}%` }}
                        />
                      </div>
                      <span className="text-xs text-gray-500">
                        {Math.round(source.score * 100)}%
                      </span>
                    </div>
                  )}
                  <p className="text-xs text-gray-600 mt-2 line-clamp-2">
                    {source.content}
                  </p>
                </div>
                {source.source && (
                  <ExternalLink className="h-3 w-3 text-gray-400 flex-shrink-0" />
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SourcesList;
