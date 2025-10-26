// Mock data cho demo frontend
export const mockMessages = [
  {
    id: '1',
    content: 'Xin chào! Tôi có thể giúp gì cho bạn?',
    role: 'assistant' as const,
    timestamp: new Date(Date.now() - 300000),
    sources: []
  }
];

export const mockCollections = [
  {
    name: 'books',
    count: 1,
    status: 'active'
  },
  {
    name: 'documents', 
    count: 5,
    status: 'active'
  },
  {
    name: 'articles',
    count: 12,
    status: 'processing'
  }
];

export const mockGraphNodes = [
  { id: '1', label: 'Phụ nữ', type: 'entity', x: 100, y: 100 },
  { id: '2', label: 'Đàn ông', type: 'entity', x: 300, y: 100 },
  { id: '3', label: 'Tình yêu', type: 'entity', x: 200, y: 200 },
  { id: '4', label: 'Hôn nhân', type: 'entity', x: 400, y: 200 },
  { id: '5', label: 'Quan hệ', type: 'relation', x: 200, y: 150 },
  { id: '6', label: 'Document 1', type: 'document', x: 50, y: 300 },
];

export const mockGraphEdges = [
  { source: '1', target: '2', label: 'quan tâm', type: 'relation' },
  { source: '1', target: '3', label: 'tìm kiếm', type: 'relation' },
  { source: '2', target: '4', label: 'cam kết', type: 'relation' },
  { source: '6', target: '1', type: 'reference' },
];

export const mockSearchResults = [
  {
    id: '1',
    title: 'Phụ nữ muốn gì ở đàn ông - Chương 1',
    content: 'Phụ nữ thường tìm kiếm sự chân thành và trung thực ở đàn ông...',
    score: 0.95,
    source: 'phu-nu-muon-gi-o-dan-ong_compress.pdf'
  },
  {
    id: '2',
    title: 'Phụ nữ muốn gì ở đàn ông - Chương 2', 
    content: 'Khả năng lắng nghe là một trong những phẩm chất quan trọng nhất...',
    score: 0.88,
    source: 'phu-nu-muon-gi-o-dan-ong_compress.pdf'
  },
  {
    id: '3',
    title: 'Phụ nữ muốn gì ở đàn ông - Chương 3',
    content: 'Sự ổn định về tài chính không có nghĩa là phải giàu có...',
    score: 0.82,
    source: 'phu-nu-muon-gi-o-dan-ong_compress.pdf'
  }
];
