# Crawl Data App

## Mô tả dự án

Dự án này sử dụng Docker Compose để triển khai hệ thống crawl, xử lý và lưu trữ dữ liệu với các thành phần chính:
- **PostgreSQL**: Lưu trữ dữ liệu
- **RabbitMQ**: Message broker cho các service giao tiếp
- **Kafka & Zookeeper**: Hệ thống message streaming
- **Producer**: Service gửi dữ liệu vào Kafka
- **Consumer**: Service nhận và xử lý dữ liệu từ Kafka
- **Kafka Streams**: Xử lý dữ liệu streaming

---

## Hướng dẫn khởi động hệ thống

1. **Cài đặt Docker và Docker Compose**  
   [Hướng dẫn cài đặt Docker](https://docs.docker.com/get-docker/)

2. **Clone repository và chuyển vào thư mục dự án**
   ```sh
   git clone <repo-url>
   cd crawl-data-app
   ```

3. **Khởi động toàn bộ hệ thống**
   ```sh
   docker-compose up --build
   ```
   - Thêm `-d` nếu muốn chạy ở chế độ nền:  
     `docker-compose up -d --build`

4. **Dừng và xóa toàn bộ container, network, volume**
   ```sh
   docker-compose down -v
   ```

---

## Mô tả từng service

### 1. db (PostgreSQL)
- **Chức năng:** Lưu trữ dữ liệu cho các service.
- **Cấu hình:**  
  - User: `huydz2k1`
  - Password: `huydz2k1`
  - Database mặc định: `crawl_data`
  - Tự động tạo thêm database `data` nhờ script `init-db.sh`
- **Port:** 5435 (bên ngoài) → 5432 (trong container)

### 2. rabbitmq
- **Chức năng:** Message broker cho các service giao tiếp.
- **Cấu hình:**  
  - User: `admin`
  - Password: `admin123`
  - Vhost: `/`
- **Port:**  
  - 5672: Cổng AMQP
  - 15672: Web UI (truy cập tại [http://localhost:15672](http://localhost:15672))

### 3. zookeeper
- **Chức năng:** Quản lý cluster cho Kafka.
- **Port:** 2181

### 4. kafka
- **Chức năng:** Hệ thống message streaming, nhận và phân phối message.
- **Port:**  
  - 9092: Kết nối nội bộ
  - 29092: Kết nối từ bên ngoài

### 5. producer
- **Chức năng:** Service gửi dữ liệu vào Kafka.
- **Build từ:** Thư mục `./producer`
- **Biến môi trường:**  
  - `KAFKA_BROKER_HOST=kafka`
  - `KAFKA_BROKER_PORT=9092`
- **Phụ thuộc:** Kafka (chỉ khởi động khi Kafka healthy)

### 6. consumer
- **Chức năng:** Service nhận và xử lý dữ liệu từ Kafka, lưu vào database.
- **Build từ:** Thư mục `./consumer`
- **Biến môi trường:**  
  - `DATABASE_URL=postgresql://huydz2k1:huydz2k1@db:5432/data`
  - `KAFKA_BROKER_HOST=kafka`
  - `KAFKA_BROKER_PORT=9092`
- **Phụ thuộc:** Kafka (chỉ khởi động khi Kafka healthy)

### 7. kafka-streams
- **Chức năng:** Xử lý dữ liệu streaming từ Kafka.
- **Build từ:** Thư mục `./stream_app`
- **Phụ thuộc:** Kafka (chỉ khởi động khi Kafka healthy)

---

## Lưu ý khi phát triển

- Nếu thay đổi script khởi tạo database (`init-db.sh`), cần xóa volume cũ để script được chạy lại:
  ```sh
  docker-compose down -v
  docker-compose up
  ```
- Có thể kiểm tra log của từng service bằng:
  ```sh
  docker-compose logs <service-name>
  ```

---

## Liên hệ
Nếu có vấn đề hoặc cần hỗ trợ, vui lòng liên hệ nhóm phát triển.