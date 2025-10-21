# genetic-algorithm-linear-regression-aws
This project builds a training and deployment pipeline for a Linear Regression model optimized by Genetic Algorithm using a small Advertising dataset.

Code ML pipeline: tải data → train model → lưu model + log MLflow → deploy inference API.

Mỗi lần push code/hyperparameter → trigger CI/CD train lại.

Sau khi train → model được deploy tự động (hoặc manual).

MLflow quản lý toàn bộ lịch sử training, metrics, artifacts.



# Tạo tài khoản AWS


# Tạo IAM
- IAM (Identity and Access Management) cho phép bạn quản lý quyền truy cập vào các dịch vụ và tài nguyên AWS một cách an toàn. Bạn có thể sử dụng IAM để kiểm soát ai được xác thực (đăng nhập) và được phép (có quyền) sử dụng tài nguyên AWS. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html
![IAM](images/find_IAM.png)

- Tạo user
Tạo Group aio_conquer26 và thêm AdministratorAccess cho group này.

Thêm user vào group đó.

- Tạo access key

![AccessKey](images/IAM_CreateAccessKey.png)

Step 1
Access key best practices & alternatives chọn Local Code



# Tạo S3
- Tạo Bucket để lưu data cho việc training cũng như lưu trọng số mô hình sau khi training


# TODO
- viết hàm tải data từ s3 vào folder data [x].    
- viết lại code training, infer [ ]   

