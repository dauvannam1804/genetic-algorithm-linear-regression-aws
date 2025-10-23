# genetic-algorithm-linear-regression-aws
This project builds a training and deployment pipeline for a Linear Regression model optimized by Genetic Algorithm using a small Advertising dataset.

Code ML pipeline: tải data → train model → lưu model → deploy EC2 cùng Gradio

Mỗi lần push code/hyperparameter → trigger CI/CD train lại.

Sau khi train → model được deploy tự động (hoặc manual).



# Tạo tài khoản AWS

- Đăng kí tài khoản AWS miễn phí tại [đây](https://signin.aws.amazon.com/signup?request_type=register)
![AWS Register](images/AWS_Register.png)

# IAM
- IAM (Identity and Access Management) cho phép bạn quản lý quyền truy cập vào các dịch vụ và tài nguyên AWS một cách an toàn. Bạn có thể sử dụng IAM để kiểm soát ai được xác thực (đăng nhập) và được phép (có quyền) sử dụng tài nguyên AWS. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html
![IAM](images/find_IAM.png)

- Sau khi chọn IAM, click chọn `User` và tạo user mới
![CreateUsser](images/CreateUser.png)
- Tạo Group `aio_conquer26` và thêm `AdministratorAccess` Provides full access to AWS services and resources cho group này.

- Thêm user vào group.

- Tạo access key
![AccessKey](images/IAM_CreateAccessKey.png)
- Lưu access key để sau này có thể test gọi các service
- Access key mẫu:   
![IAM Access Key](images/IAM_AccessKey.png)

# Tạo S3 (Simple Storage Service)
- Tạo Bucket để lưu data cho việc training cũng như lưu trọng số mô hình sau khi training
- Thử upload data từ local với file `upload_s3.py`
![TestUploadData](images/S3_uploaded_data.png)

- Thử tải data về máy local     
![TestFetchData](images/S3_fetchDataLocal.png)



# Thử train và infer ở máy local
- Train và lưu weight thử ở local và đẩy lên s3
![Train Local Result](images/Local_train_result.png)

- Infer ở local
![Train Result](images/Local_infer.png)


# Thử deploy ở máy local
- Nhập thông tin 3 giá trị TV Advertising, Radio Advertising, Newspaper Advertising và predict kết quả Sales
![Train Result](images/Local_Deploy.png)


# Tạo Instance EC2
- Tìm EC2 trên thanh tìm kiêm
![Find EC2](images/find_EC2.png)

- Chọn Launch Instance 
![Launch Instance ](images/EC2_Launch_Instance.png)

- Đặt tên `aio_conquer26_ec2`
- Chọn instance type `c7i-flex.large (2 vCPU, 4GB RAM)` vì hiệu năng ổn định, chi phí thấp, đủ cho training Genetic Algorithm + Linear Regression và dễ tích hợp với S3, và deploy trên AWS
- Tạo key pair và tải về để có thể ssh từ máy local hoặc dùng cho CI/CD Github Actions sau này
- Chọn:     
Allow SSH traffic from: My IP → để chỉ bạn truy cập được qua SSH (bảo mật).     
Allow HTTPS traffic from the internet: để sau này truy cập API qua cổng 443 (nếu có SSL).   
Allow HTTP traffic from the internet: để truy cập ứng dụng Gradio demo UI (port 80 hoặc 8000). 
- Cuối cùng chọn Launch Instance 
- Instance đã được tạo
![Created Instance ](images/EC2_CreatedInstance.png)

- Thử vào Instance đã được tạo trên Web
![Created Instance ](images/EC2_ConnectOnWeb.png)
- Connect vào Instance
![Connect Instance](images/EC2_ConnectOnWeb1.png)
- Bên trong Instance đã tạo
![Connect Instance](images/EC2_InAnInstance.png)
- Kiểm tra thử Instance thì hiện tại trống, chỉ có vài file cài sẵn để đăng nhập và chạy lệnh cơ bản
![Connect Instance](images/EC2_CheckInstance.png)



Train và deploy trên Instance EC2

training_script.sh

kiểm tra data đã có trong folder `data/` hay chưa
- chưa có thì tải từ s3 về  `data/` dùng `fetch_dataset_s3.py`
- nếu trên s3 cũng chưa có thì chạy `upload_dataset_s3.py` để tải data từ url về s3 sau đó tải về  `data/` dùng `fetch_dataset_s3.py`

train model dùng script `model/train.py`
