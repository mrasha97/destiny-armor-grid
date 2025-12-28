import os
import tempfile
from flask import Blueprint, render_template, request, jsonify, send_file, session

from app.services.csv_parser import parse_csv, CSVParserError
from app.services.data_processor import process_armor_data
from app.services.excel_exporter import export_to_excel

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename: Name of the uploaded file

    Returns:
        True if file extension is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route('/')
def index():
    """
    Render the main upload page.

    Returns:
        Rendered index template
    """
    return render_template('index.html')


@main_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle CSV file upload and processing.

    Returns:
        JSON response with processing results or error message
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

    try:
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as temp_csv:
            file.save(temp_csv.name)
            temp_csv_path = temp_csv.name

        df = parse_csv(temp_csv_path)

        processed_df, metrics = process_armor_data(df)

        with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as temp_excel:
            temp_excel_path = temp_excel.name

        export_to_excel(processed_df, temp_excel_path)

        session['excel_path'] = temp_excel_path
        session['csv_path'] = temp_csv_path

        preview_data = processed_df.to_dict('records')
        preview_columns = list(processed_df.columns)

        os.unlink(temp_csv_path)

        return jsonify({
            'success': True,
            'metrics': metrics,
            'preview': {
                'columns': preview_columns,
                'data': preview_data
            }
        })

    except CSVParserError as e:
        if 'temp_csv_path' in locals() and os.path.exists(temp_csv_path):
            os.unlink(temp_csv_path)
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        if 'temp_csv_path' in locals() and os.path.exists(temp_csv_path):
            os.unlink(temp_csv_path)
        if 'temp_excel_path' in locals() and os.path.exists(temp_excel_path):
            os.unlink(temp_excel_path)
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@main_bp.route('/download')
def download_file():
    """
    Download the processed Excel file.

    Returns:
        Excel file as attachment
    """
    excel_path = session.get('excel_path')

    if not excel_path or not os.path.exists(excel_path):
        return jsonify({'error': 'No file available for download'}), 404

    try:
        return send_file(
            excel_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='destiny2_armor_sorted.xlsx'
        )
    finally:
        if os.path.exists(excel_path):
            try:
                os.unlink(excel_path)
            except:
                pass
        session.pop('excel_path', None)

