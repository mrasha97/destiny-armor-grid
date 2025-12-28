"""
Improved routes with better error handling and logging.
Demonstrates best practices for Flask route handlers.
"""
import os
import tempfile
from flask import Blueprint, render_template, request, jsonify, send_file, session, current_app

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


def cleanup_temp_file(file_path: str) -> None:
    """
    Safely remove a temporary file with error handling.

    Args:
        file_path: Path to the temporary file to remove
    """
    if file_path and os.path.exists(file_path):
        try:
            os.unlink(file_path)
            current_app.logger.debug(f'Cleaned up temp file: {file_path}')
        except (OSError, PermissionError) as e:
            current_app.logger.warning(f'Failed to clean up file {file_path}: {e}')


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
    temp_csv_path = None
    temp_excel_path = None

    try:
        # Validate file presence
        if 'file' not in request.files:
            current_app.logger.warning('Upload attempt with no file')
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            current_app.logger.warning('Upload attempt with empty filename')
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            current_app.logger.warning(f'Invalid file type attempted: {file.filename}')
            return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

        current_app.logger.info(f'Processing file: {file.filename}')

        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as temp_csv:
            file.save(temp_csv.name)
            temp_csv_path = temp_csv.name

        # Parse and validate CSV
        df = parse_csv(temp_csv_path)
        current_app.logger.info(f'Parsed CSV with {len(df)} rows')

        # Process armor data
        processed_df, metrics = process_armor_data(df)
        current_app.logger.info(f'Processed armor data: {metrics}')

        # Generate Excel file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as temp_excel:
            temp_excel_path = temp_excel.name

        export_to_excel(processed_df, temp_excel_path)
        current_app.logger.info('Generated Excel file')

        # Store paths in session for download
        session['excel_path'] = temp_excel_path
        session['csv_path'] = temp_csv_path

        # Prepare preview data
        preview_data = processed_df.to_dict('records')
        preview_columns = list(processed_df.columns)

        # Clean up CSV (Excel kept for download)
        cleanup_temp_file(temp_csv_path)

        return jsonify({
            'success': True,
            'metrics': metrics,
            'preview': {
                'columns': preview_columns,
                'data': preview_data
            }
        })

    except CSVParserError as e:
        current_app.logger.error(f'CSV parsing error: {e}')
        cleanup_temp_file(temp_csv_path)
        cleanup_temp_file(temp_excel_path)
        return jsonify({'error': str(e)}), 400

    except ValueError as e:
        current_app.logger.error(f'Value error during processing: {e}')
        cleanup_temp_file(temp_csv_path)
        cleanup_temp_file(temp_excel_path)
        return jsonify({'error': f'Data validation error: {str(e)}'}), 400

    except Exception as e:
        current_app.logger.error(f'Unexpected error during upload: {e}', exc_info=True)
        cleanup_temp_file(temp_csv_path)
        cleanup_temp_file(temp_excel_path)
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@main_bp.route('/download')
def download_file():
    """
    Download the processed Excel file.

    Returns:
        Excel file as attachment or error response
    """
    excel_path = session.get('excel_path')

    if not excel_path or not os.path.exists(excel_path):
        current_app.logger.warning('Download attempt with no file available')
        return jsonify({'error': 'No file available for download'}), 404

    try:
        current_app.logger.info(f'Sending file for download: {excel_path}')
        return send_file(
            excel_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='destiny2_armor_sorted.xlsx'
        )
    except Exception as e:
        current_app.logger.error(f'Error sending file: {e}', exc_info=True)
        return jsonify({'error': 'Failed to download file'}), 500
    finally:
        # Clean up after download
        cleanup_temp_file(excel_path)
        session.pop('excel_path', None)


@main_bp.route('/health')
def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        JSON response indicating service health
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Destiny 2 Armor Sorter',
        'version': '1.0.0'
    }), 200

