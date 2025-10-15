# app.py (Code đã chỉnh sửa)

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'my_database.db'
TABLE_NAME = 'search_data'
KEY_CCCD_COLUMN_NAME = 'Ma_Key_Tim_Kiem'  # Tên cột CCCD (Giả định từ trước)
KEY_MST_COLUMN_NAME = 'Ma_So_Thue'      # TÊN CỘT MỚI: Mã số thuế (BẠN PHẢI KIỂM TRA CHÍNH XÁC)

# Cho phép Front-end (index.html) truy cập (CORS)
# ... (Giữ nguyên hàm add_cors_headers) ...
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*' 
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

# ENDPOINT GỐC: TÌM KIẾM THEO CCCD
@app.route('/search/cccd', methods=['GET'])
def search_cccd():
    search_key = request.args.get('key', '').strip()
    return perform_search(search_key, KEY_CCCD_COLUMN_NAME)

# ENDPOINT MỚI: TÌM KIẾM THEO MÃ SỐ THUẾ
@app.route('/search/mst', methods=['GET'])
def search_mst():
    search_key = request.args.get('key', '').strip()
    return perform_search(search_key, KEY_MST_COLUMN_NAME)


def perform_search(search_key, column_name):
    """Hàm lõi để thực hiện tìm kiếm CSDL"""
    
    if not search_key:
        return jsonify({
            "status": "error",
            "message": "Tham số tìm kiếm không được trống."
        }), 400
    
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        # Truy vấn CSDL, dùng tên cột động
        sql_query = f"SELECT * FROM {TABLE_NAME} WHERE LOWER({column_name}) = LOWER(?)"
        
        cursor.execute(sql_query, (search_key,))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            results_list = [dict(row) for row in rows] 
            return jsonify({
                "status": "success",
                "data": results_list
            })
        else:
            return jsonify({
                "status": "not_found",
                "message": f"Không tìm thấy dữ liệu với Key: {search_key}"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "fatal_error",
            "message": "Lỗi truy vấn CSDL: " + str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)