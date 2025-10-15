from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'my_database.db'
TABLE_NAME = 'search_data'
KEY_COLUMN_NAME = 'CCCD' # PHẢI KHỚP VỚI TÊN CỘT VÀ TÊN TRONG prepare_db.py

# Cho phép Front-end (index.html) truy cập (CORS)
@app.after_request
def add_cors_headers(response):
    # Cho phép truy cập từ mọi nguồn (khi chạy index.html cục bộ)
    response.headers['Access-Control-Allow-Origin'] = '*' 
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

@app.route('/search', methods=['GET'])
def search_key():
    search_key = request.args.get('key', '').strip()

    if not search_key:
        return jsonify({
            "status": "error",
            "message": "Tham số 'key' không được trống."
        }), 400
    
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row # Cho phép lấy kết quả bằng tên cột
        cursor = conn.cursor()
        
        # Truy vấn CSDL. LOWER() giúp tìm kiếm không phân biệt hoa/thường.
        sql_query = f"SELECT * FROM {TABLE_NAME} WHERE LOWER({KEY_COLUMN_NAME}) = LOWER(?)"
        
        cursor.execute(sql_query, (search_key,))
        
        # *** QUAN TRỌNG: Dùng fetchall() để lấy TẤT CẢ các kết quả ***
        rows = cursor.fetchall()
        
        conn.close()

        if rows:
            # Chuyển tất cả các hàng thành danh sách các dictionary (JSON objects)
            results_list = [dict(row) for row in rows] 
            
            return jsonify({
                "status": "success",
                "data": results_list # Trả về MẢNG các kết quả
            })
        else:
            return jsonify({
                "status": "not_found",
                "message": f"Không tìm thấy dữ liệu với Key: {search_key}"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "fatal_error",
            "message": "Lỗi nội bộ máy chủ: " + str(e)
        }), 500

if __name__ == '__main__':
    # Chạy Server trên cổng 5000
    app.run(debug=True, port=5000)