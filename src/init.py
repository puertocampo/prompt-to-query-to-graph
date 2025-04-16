import generate_sql_query
import exec_sql_query
import generate_plot_code
import execute_plot_code
import upload_image_to_s3

prompt = "教員が担当している学生数の分布を表示してください。"
query = generate_sql_query.generate_sql_query(prompt)
exec_results = exec_sql_query.execute_sql_query(query)
plot_code = generate_plot_code.generate_plot_code(exec_results, "教員が担当している学生数の分布")
image_base64 = execute_plot_code.execute_plot_code(plot_code)
print(image_base64)
image_url = upload_image_to_s3.upload_image_to_s3(image_base64)
print(image_url)