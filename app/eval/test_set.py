# app/eval/test_set.py
sample_queries = [
    "Theo bài viết, phụ nữ thường xem trọng điều gì nhất khi chọn bạn đời?",
    "Theo chuyên gia Maggie Martinez, có những yếu tố nào khác ngoài địa vị kinh tế xã hội thu hút phụ nữ?",
    "Tại sao phụ nữ muốn đàn ông biết cách biểu lộ tình yêu?",
    "Đáng tin cậy trong mối quan hệ có nghĩa là gì theo bài viết?",
    "Vì sao phụ nữ muốn đàn ông lo được cho tương lai?",
    "Điều gì giúp nam giới giao tiếp tốt hơn với bạn đời?",
    "Tại sao tự chăm sóc bản thân lại là điều phụ nữ mong muốn ở đàn ông?",
    "Phụ nữ mong đợi gì ở sự ủng hộ từ người chồng?",
    "Theo bài viết, vì sao đàn ông nên dám yếu đuối?",
    "Điều gì khiến một người đàn ông trở nên hấp dẫn trong mắt phụ nữ?",
    "Khiếu hài hước có vai trò gì trong mối quan hệ?",
    "Sự trưởng thành khác gì với tuổi tác theo quan điểm bài viết?",
    "Phụ nữ mong muốn gì ở đàn ông trong đời sống tình dục?",
    "Vì sao khả năng thích nghi được đánh giá cao ở người đàn ông?"
]

expected_responses = [
    "Phụ nữ thường xem trọng địa vị kinh tế xã hội của đàn ông hơn là ngoại hình khi chọn bạn đời.",
    "Ngoài địa vị kinh tế, phụ nữ còn bị thu hút bởi những yếu tố như biết biểu lộ tình yêu, đáng tin cậy, giao tiếp tốt, tự chăm sóc bản thân, hài hước và trưởng thành.",
    "Vì phụ nữ giàu cảm xúc và muốn cảm nhận được tình yêu, nên họ mong đàn ông biết bày tỏ tình cảm bằng lời nói và hành động nhỏ như tặng quà hay bữa tối lãng mạn.",
    "Đáng tin cậy nghĩa là hai người có thể chia sẻ quá khứ, tin tưởng và cởi mở với nhau thay vì giấu giếm hoặc lảng tránh.",
    "Phụ nữ muốn đàn ông lo được cho tương lai vì họ tìm kiếm sự an toàn, ổn định và tài chính vững chắc cho gia đình và con cái.",
    "Nam giới nên trò chuyện thật sự với bạn đời để hiểu nhu cầu và mong muốn của họ, thay vì chỉ tập trung vào công việc.",
    "Phụ nữ mong đàn ông biết tự chăm sóc bản thân vì điều đó thể hiện trách nhiệm và giúp duy trì sức khỏe cho hạnh phúc lâu dài.",
    "Phụ nữ mong chồng ủng hộ và chia sẻ cùng họ trong cả niềm vui lẫn khó khăn, tạo cảm giác đồng hành và gắn kết.",
    "Phụ nữ muốn đàn ông cởi mở về cảm xúc vì sự yếu đuối đúng mực giúp họ cảm thấy gần gũi và thấu hiểu hơn.",
    "Sự tự tin khiến đàn ông hấp dẫn hơn vì nó thể hiện qua cách cư xử, nói chuyện và phong thái tổng thể.",
    "Khiếu hài hước giúp giải tỏa căng thẳng, khiến phụ nữ cảm thấy thoải mái và gắn bó hơn với chồng.",
    "Sự trưởng thành thể hiện ở khả năng nhìn nhận vấn đề sáng suốt và ứng xử hợp lý, chứ không chỉ do tuổi tác.",
    "Phụ nữ mong đàn ông quan tâm, chu đáo và thấu hiểu cảm xúc của họ trong đời sống tình dục.",
    "Khả năng thích nghi giúp đàn ông linh hoạt, dễ hòa hợp và khiến cuộc sống chung trở nên thú vị hơn."
]
