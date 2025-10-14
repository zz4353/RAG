from app.graph_rag.indexer import extract_entities_and_relations, summarize_text
from app.graph_rag.retriever import extract_entities

# t = extract_entities_and_relations("Máy tính bảng Samsung được đánh giá cao nhờ thiết kế mỏng nhẹ, hiệu năng mạnh mẽ và thời lượng pin ấn tượng. Nhiều người dùng yêu thích màn hình lớn và khả năng kết nối đa dạng của sản phẩm này. Bên cạnh đó, tai nghe không dây Samsung mới hỗ trợ chống ồn chủ động và dễ dàng kết nối với nhiều thiết bị khác nhau.")

t = extract_entities("Điện thoại Samsung mới ra mắt năm nay có thiết kế hiện đại, màu sắc trẻ trung, và được trang bị nhiều tính năng nổi bật như camera sắc nét, pin lâu và hỗ trợ sạc nhanh. Theo một số người dùng trên mạng, thiết bị này cầm rất vừa tay và giao diện khá dễ sử dụng, tuy nhiên mức giá hiện tại vẫn còn hơi cao so với các sản phẩm cùng phân khúc. Ngoài ra, hãng cũng giới thiệu mẫu tai nghe không dây mới với khả năng chống ồn và kết nối Bluetooth ổn định. Tôi nghĩ màu xanh mới rất đẹp, nhưng mỗi người sẽ có sở thích riêng.")

print(t)