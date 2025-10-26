# RAG Frontend

Frontend cho hệ thống RAG (Retrieval-Augmented Generation) với HybridRAG architecture.

## Tính năng

- 💬 **Chat Interface**: Giao diện chat với RAG system
- 📁 **Document Upload**: Tải lên và xử lý tài liệu
- 🗂️ **Collections Management**: Quản lý bộ sưu tập tài liệu
- 🕸️ **Knowledge Graph Visualization**: Hiển thị đồ thị tri thức
- ⚙️ **Settings**: Cấu hình hệ thống

## Công nghệ sử dụng

- React 18 + TypeScript
- Vite (Build tool)
- Tailwind CSS (Styling)
- Lucide React (Icons)
- Axios (HTTP client)
- React Query (Data fetching)

## Cài đặt

```bash
# Cài đặt dependencies
npm install

# Chạy development server
npm run dev

# Build cho production
npm run build
```

## Cấu trúc dự án

```
src/
├── components/          # React components
│   ├── ChatInterface.tsx
│   ├── DocumentUpload.tsx
│   ├── CollectionsView.tsx
│   ├── GraphVisualization.tsx
│   └── Sidebar.tsx
├── services/           # API services
│   └── api.ts
├── types/              # TypeScript types
│   └── index.ts
├── hooks/              # Custom hooks
├── App.tsx             # Main app component
└── main.tsx            # Entry point
```

## API Endpoints

Frontend kết nối với backend API tại `http://localhost:8000`:

- `POST /chat` - Gửi tin nhắn đến RAG system
- `POST /upload` - Tải lên tài liệu
- `GET /collections` - Lấy danh sách collections
- `POST /search` - Tìm kiếm tài liệu

## HybridRAG Features

- **Vector Search**: Tìm kiếm dựa trên semantic similarity
- **Graph Search**: Tìm kiếm dựa trên knowledge graph
- **Hybrid Search**: Kết hợp cả hai phương pháp
- **Knowledge Graph Visualization**: Hiển thị relationships giữa entities
