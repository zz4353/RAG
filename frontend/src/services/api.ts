const BASE_URL = 'http://localhost:8000';

type QueryType = 'vector' | 'graph' | 'hybrid';

function mapPointToDocument(p: any, idx: number) {
  const payload = p?.payload ?? {};
  return {
    id: p?.id?.toString?.() ?? String(idx),
    title: payload.source ?? 'Document chunk',
    content: payload.content ?? '',
    score: p?.score,
    source: payload.source,
  };
}

export const chatAPI = {
  // Send message -> use /ask-rag; map docs to sources
  sendMessage: async (message: string, queryType: QueryType = 'hybrid') => {
    const res = await fetch(`${BASE_URL}/ask-rag`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: message, docs: [] }),
    });
    if (!res.ok) throw new Error(`ask-rag failed: ${res.status}`);
    const data = await res.json(); // { question, docs, answer }
    const sources = Array.isArray(data?.docs)
      ? data.docs.map(mapPointToDocument)
      : [];
    return {
      answer: data?.answer ?? '',
      sources,
      query_type: queryType,
    };
  },

  // // Upload documents (multipart) -> map to existing UploadResponse shape
  // uploadDocuments: async (files: File[]) => {
  //   const form = new FormData();
  //   files.forEach((f) => form.append('files', f));
  //   const res = await fetch(`${BASE_URL}/upload`, {
  //     method: 'POST',
  //     body: form,
  //   });
  //   if (!res.ok) throw new Error(`upload failed: ${res.status}`);
  //   const data = await res.json(); // { status, files_processed, saved }
  //   return {
  //     message: `Đã xử lý ${data?.files_processed ?? 0} tài liệu thành công!`,
  //     documents_processed: data?.files_processed ?? 0,
  //     collection_name: 'books',
  //   };
  // },

  // Get collections -> map names to UI structure
  getCollections: async () => {
    const res = await fetch(`${BASE_URL}/collections`);
    if (!res.ok) throw new Error(`collections failed: ${res.status}`);
    const data = await res.json(); // { collections: Array<{name, count, status}> }
    return Array.isArray(data?.collections) ? data.collections : [];
  },

//   // Search documents in a collection
//   searchDocuments: async (query: string, collection: string) => {
//     const res = await fetch(`${BASE_URL}/search`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({
//         collection_name: collection,
//         query,
//         top_k: 5,
//         threshold: 0.3,
//       }),
//     });
//     if (!res.ok) throw new Error(`search failed: ${res.status}`);
//     const data = await res.json(); // { query, result }
//     const results = Array.isArray(data?.result) ? data.result.map(mapPointToDocument) : [];
//     return { results };
//   },
};


















// import { mockMessages, mockCollections, mockGraphNodes, mockGraphEdges, mockSearchResults } from './mockData';

// // Mock API functions cho demo
// export const chatAPI = {
//   // Mock send message
//   sendMessage: async (message: string, queryType: 'vector' | 'graph' | 'hybrid' = 'hybrid') => {
//     // Simulate API delay
//     await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
//     // Mock responses based on query type
//     let answer = '';
//     let sources = [];
    
//     if (message.toLowerCase().includes('phụ nữ') || message.toLowerCase().includes('đàn ông')) {
//       answer = `Dựa trên tài liệu "Phụ nữ muốn gì ở đàn ông", phụ nữ thường tìm kiếm những phẩm chất sau ở đàn ông:

// 1. **Sự chân thành và trung thực** - Phụ nữ đánh giá cao những người đàn ông biết thể hiện bản thân một cách chân thật

// 2. **Khả năng lắng nghe** - Biết lắng nghe và thấu hiểu cảm xúc của phụ nữ

// 3. **Sự ổn định về tài chính** - Không nhất thiết phải giàu có nhưng cần có khả năng đảm bảo cuộc sống ổn định

// 4. **Tính cách hài hước** - Biết cách làm phụ nữ cười và tạo không khí vui vẻ

// 5. **Sự tôn trọng** - Tôn trọng ý kiến, quyết định và không gian riêng tư của phụ nữ

// ${queryType === 'hybrid' ? '\n\n*Kết quả từ HybridRAG (Vector + Graph Search)*' : 
//   queryType === 'vector' ? '\n\n*Kết quả từ Vector Search*' : 
//   '\n\n*Kết quả từ Graph Search*'}`;
      
//       sources = mockSearchResults;
//     } else if (message.toLowerCase().includes('xin chào') || message.toLowerCase().includes('hello')) {
//       answer = 'Xin chào! Tôi là RAG Assistant, có thể giúp bạn tìm hiểu thông tin từ tài liệu. Hãy đặt câu hỏi cho tôi!';
//     } else {
//       answer = `Tôi đã tìm thấy thông tin liên quan đến câu hỏi "${message}". Đây là kết quả từ ${queryType === 'hybrid' ? 'HybridRAG' : queryType === 'vector' ? 'Vector Search' : 'Graph Search'}:

// Thông tin này được trích xuất từ các tài liệu trong hệ thống. Bạn có thể hỏi thêm chi tiết về bất kỳ phần nào.`;
//       sources = mockSearchResults.slice(0, 2);
//     }
    
//     return {
//       answer,
//       sources,
//       query_type: queryType
//     };
//   },

//   // Mock upload documents
//   uploadDocuments: async (files: File[]) => {
//     await new Promise(resolve => setTimeout(resolve, 2000));
    
//     return {
//       message: `Đã xử lý ${files.length} tài liệu thành công!`,
//       documents_processed: files.length,
//       collection_name: 'books_collection'
//     };
//   },

//   // Mock get collections
//   getCollections: async () => {
//     await new Promise(resolve => setTimeout(resolve, 500));
//     return mockCollections;
//   },

//   // Mock search documents
//   searchDocuments: async (query: string, collection: string) => {
//     await new Promise(resolve => setTimeout(resolve, 800));
//     return {
//       results: mockSearchResults.filter(result => 
//         result.content.toLowerCase().includes(query.toLowerCase()) ||
//         result.title.toLowerCase().includes(query.toLowerCase())
//       )
//     };
//   }
// };
