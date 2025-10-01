import React, { useState, useEffect } from 'react';
import { GitBranch, Network, Search, Filter } from 'lucide-react';

interface GraphNode {
  id: string;
  label: string;
  type: 'entity' | 'relation' | 'document';
  x?: number;
  y?: number;
}

interface GraphEdge {
  source: string;
  target: string;
  label?: string;
  type: 'relation' | 'reference';
}

const GraphVisualization: React.FC = () => {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'entity' | 'relation' | 'document'>('all');

  // Mock data for demonstration
  useEffect(() => {
    const mockNodes: GraphNode[] = [
      { id: '1', label: 'Phụ nữ', type: 'entity', x: 100, y: 100 },
      { id: '2', label: 'Đàn ông', type: 'entity', x: 300, y: 100 },
      { id: '3', label: 'Tình yêu', type: 'entity', x: 200, y: 200 },
      { id: '4', label: 'Hôn nhân', type: 'entity', x: 400, y: 200 },
      { id: '5', label: 'Quan hệ', type: 'relation', x: 200, y: 150 },
      { id: '6', label: 'Document 1', type: 'document', x: 50, y: 300 },
    ];

    const mockEdges: GraphEdge[] = [
      { source: '1', target: '2', label: 'quan tâm', type: 'relation' },
      { source: '1', target: '3', label: 'tìm kiếm', type: 'relation' },
      { source: '2', target: '4', label: 'cam kết', type: 'relation' },
      { source: '6', target: '1', type: 'reference' },
    ];

    setNodes(mockNodes);
    setEdges(mockEdges);
  }, []);

  const filteredNodes = nodes.filter(node => {
    const matchesSearch = node.label.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || node.type === filterType;
    return matchesSearch && matchesFilter;
  });

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'entity': return 'bg-blue-500';
      case 'relation': return 'bg-green-500';
      case 'document': return 'bg-purple-500';
      default: return 'bg-gray-500';
    }
  };

  const getNodeSize = (type: string) => {
    switch (type) {
      case 'entity': return 'w-8 h-8';
      case 'relation': return 'w-6 h-6';
      case 'document': return 'w-10 h-10';
      default: return 'w-6 h-6';
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <GitBranch className="h-5 w-5 text-blue-500" />
            <h2 className="text-xl font-semibold text-gray-800">Knowledge Graph</h2>
          </div>
          <div className="flex items-center space-x-2">
            <Network className="h-4 w-4 text-gray-500" />
            <span className="text-sm text-gray-600">{nodes.length} nodes, {edges.length} edges</span>
          </div>
        </div>

        {/* Controls */}
        <div className="flex space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Tìm kiếm nodes..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value as any)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Tất cả</option>
            <option value="entity">Entities</option>
            <option value="relation">Relations</option>
            <option value="document">Documents</option>
          </select>
        </div>
      </div>

      {/* Graph Visualization */}
      <div className="flex-1 relative bg-gray-50 overflow-hidden">
        <svg className="w-full h-full">
          {/* Render edges */}
          {edges.map((edge, index) => {
            const sourceNode = nodes.find(n => n.id === edge.source);
            const targetNode = nodes.find(n => n.id === edge.target);
            if (!sourceNode || !targetNode) return null;

            return (
              <line
                key={index}
                x1={sourceNode.x || 0}
                y1={sourceNode.y || 0}
                x2={targetNode.x || 0}
                y2={targetNode.y || 0}
                stroke={edge.type === 'relation' ? '#3b82f6' : '#10b981'}
                strokeWidth={edge.type === 'relation' ? 2 : 1}
                strokeDasharray={edge.type === 'reference' ? '5,5' : '0'}
              />
            );
          })}

          {/* Render nodes */}
          {filteredNodes.map((node) => (
            <g key={node.id}>
              <circle
                cx={node.x || 0}
                cy={node.y || 0}
                r={node.type === 'entity' ? 16 : node.type === 'document' ? 20 : 12}
                fill={node.type === 'entity' ? '#3b82f6' : node.type === 'relation' ? '#10b981' : '#8b5cf6'}
                stroke={selectedNode?.id === node.id ? '#f59e0b' : 'white'}
                strokeWidth={selectedNode?.id === node.id ? 3 : 2}
                className="cursor-pointer hover:opacity-80"
                onClick={() => setSelectedNode(node)}
              />
              <text
                x={node.x || 0}
                y={(node.y || 0) + 5}
                textAnchor="middle"
                className="text-xs fill-white font-medium pointer-events-none"
              >
                {node.label.length > 8 ? node.label.substring(0, 8) + '...' : node.label}
              </text>
            </g>
          ))}
        </svg>

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-white rounded-lg shadow-sm border border-gray-200 p-3">
          <h4 className="text-sm font-medium text-gray-800 mb-2">Legend</h4>
          <div className="space-y-1 text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
              <span>Entities</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span>Relations</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
              <span>Documents</span>
            </div>
          </div>
        </div>
      </div>

      {/* Node Details Panel */}
      {selectedNode && (
        <div className="absolute bottom-4 left-4 right-4 bg-white rounded-lg shadow-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-gray-800">{selectedNode.label}</h3>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>
          <div className="text-sm text-gray-600">
            <p><strong>Type:</strong> {selectedNode.type}</p>
            <p><strong>ID:</strong> {selectedNode.id}</p>
            <p><strong>Connections:</strong> {edges.filter(e => e.source === selectedNode.id || e.target === selectedNode.id).length}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default GraphVisualization;
