from flask import Flask, render_template, redirect, url_for, request, session, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import cv2
import datetime
from ultralytics import YOLO
import supervision as sv
import numpy as np
from waitress import serve
import os
from functools import wraps
import json
from collections import defaultdict
from flask import jsonify
from datetime import datetime, timedelta
import onnx
import onnxruntime
import multiprocessing

app = Flask(__name__)
app.secret_key = 'BGH0$112233'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
capturing = False

# Configuración global
global_config = {
    'model_confidence': 0.5,
    'model_choice': 'model/best.onnx',
    'model_frames': 6
}

# Definir el polígono de la región de interés (ROI)
ROI_POLYGON = np.array([[750, 350], [1330, 350], [1330, 850], [750, 850]])

label_counts = defaultdict(int)  # Diccionario para almacenar el conteo de etiquetas

# Modelo y configuración
color_palette = sv.ColorPalette.from_hex(['#00ff00', '#ff0000', '#ffff00'])
box_annotator = sv.BoxAnnotator(color=color_palette, thickness=2)
label_annotator = sv.LabelAnnotator(color=color_palette, text_thickness=2, text_scale=1, text_color=sv.Color.BLACK)

CONFIG_FILE = 'config.json'

# Modelo de Usuario
class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Modelo para Log de IA
class IALog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    result = db.Column(db.String(150))
    confidences = db.Column(db.String(300))
    model_confidence = db.Column(db.Float, nullable=True)
    model_choice = db.Column(db.String(200), nullable=True)
    model_frames = db.Column(db.Integer, nullable=True)

# Crear una máscara de la región de interés (ROI)
def apply_roi(frame, roi_polygon):
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [roi_polygon], (255, 255, 255))  # Rellenar el polígono con color blanco

    # Aplicar la máscara al frame
    masked_frame = cv2.bitwise_and(frame, mask)
    return masked_frame

# Cargar configuración desde archivo JSON
def load_config():
    global global_config
    try:
        with open('config.json', 'r') as f:
            global_config.update(json.load(f))
    except FileNotFoundError:
        save_config(global_config)  # Guardar configuración predeterminada si no existe el archivo

# Guardar configuración en archivo JSON
def save_config(config):
    global global_config
    global_config.update(config)  # Actualizar el diccionario global
    with open('config.json', 'w') as f:
        json.dump(global_config, f, indent=4)

def generate_frames():
    global capturing, global_config
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('videos/tercerLote.mp4')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    frame_skip = global_config['model_frames']  # Procesar un cuadro cada X cuadros
    frame_count = 0

    # Procesar solo la parte de la imagen dentro del ROI
    model = YOLO(global_config['model_choice'], task="detect")    

    while True:
        if not capturing:  # Si la captura está detenida, sal del bucle
            break
        
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue
        
        # Aplicar la región de interés (ROI) al frame
        roi_frame = apply_roi(frame, ROI_POLYGON)

        result = model(roi_frame, conf=global_config['model_confidence'])[0]
        detections = sv.Detections.from_ultralytics(result)

        # Reiniciar los conteos para el frame actual
        local_counts = defaultdict(int)
        labels = detections.data.get('class_name', [])
        confidences = detections.confidence.tolist()

        for label in labels:
            local_counts[label] += 1

        # Actualizar el conteo global
        label_counts.clear()
        label_counts.update(local_counts)

        # Guardar en base de datos si se cumplen las condiciones
        if all(conf > global_config['model_confidence'] for conf in confidences):  # Verificar condición de confianza
            if sum(local_counts.values()) == 10 and local_counts.get('SP', 0) < 2:
                result_string = ", ".join(labels)
                confidence_string = ", ".join(f"{conf:.2f}" for conf in confidences)
                with app.app_context():
                    log = IALog(
                        timestamp=datetime.now(),
                        result=result_string,
                        confidences=confidence_string,
                        model_confidence=global_config['model_confidence'],
                        model_choice=global_config['model_choice'],
                        model_frames=global_config['model_frames']
                    )
                    db.session.add(log)
                    db.session.commit()

        # Anotar las detecciones dentro del ROI
        frame = box_annotator.annotate(scene=frame, detections=detections)
        frame = label_annotator.annotate(scene=frame, detections=detections)
        
        # Dibuja la zona de interés en el frame
        frame = sv.draw_polygon(scene=frame, polygon=ROI_POLYGON, color=sv.Color.GREEN)

        # Convertir el frame a JPEG
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión primero', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta para configuración
@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    if request.method == 'POST':
        model_confidence = float(request.form.get('model_confidence'))
        model_choice = request.form.get('model_choice')
        model_frames = int(request.form.get('model_frames'))
        
        # Actualizar configuración global y archivo JSON
        save_config({
            'model_confidence': model_confidence,
            'model_choice': model_choice,
            'model_frames': model_frames
        })
        flash('Configuración actualizada correctamente', 'success')
        return redirect(url_for('config'))
    
    return render_template('config.html', config=global_config)

@app.route('/start_capture')
def start_capture():
    global capturing
    capturing = True
    flash('Captura iniciada', 'success')
    return redirect(url_for('index'))

@app.route('/stop_capture')
def stop_capture():
    global capturing
    capturing = False
    flash('Captura finalizada', 'warning')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password'])
        if bcrypt.check_password_hash(password, request.form['confirm_password']):
            if Usuarios.query.filter_by(username=username).first():
                flash('El usuario ya existe', 'danger')
                return redirect(url_for('register'))
            new_user = Usuarios(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('login'))
        
        else:
            flash('La clave conoincide', 'danger')
            return redirect(url_for('register'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuarios.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario/Clave incorrecta', 'danger')
    
    return render_template('login.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Rutas y vistas
@app.route('/get_counts', methods=['GET'])
def get_counts():
    global label_counts
    return jsonify({label: count for label, count in label_counts.items()})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Cierre de sesión exitoso', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', config=global_config)

@app.route('/logs', methods=['GET', 'POST'])
@login_required
def logs():
    date = request.args.get('date')  # Obtener la fecha del parámetro GET
    if date:
        logs = IALog.query.filter(db.func.date(IALog.timestamp) == date).all()
    else:
        logs = IALog.query.order_by(IALog.timestamp.desc()).all()

    # Serializar los logs para pasarlos al template
    serialized_logs = [
        {
            'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'result': log.result,
            'confidences': log.confidences,
            'model_confidence': log.model_confidence,
            'model_choice': log.model_choice,
            'model_frames': log.model_frames
        }
        for log in logs
    ]

    return render_template('logs.html', logs=serialized_logs)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard_data', methods=['GET'])
def dashboard_data():
    ten_days_ago = datetime.now() - timedelta(days=30)
    
    # Obtener registros de los últimos 10 días
    logs = (
        db.session.query(
            db.func.date(IALog.timestamp).label("date"),
            IALog.result,
            IALog.model_confidence
        )
        .filter(IALog.timestamp >= ten_days_ago)
        .order_by(IALog.timestamp.asc())  # Ordenar por fecha ascendente
        .all()
    )

    # Inicializar variables
    results_by_date = {}
    total_counts = {'SP': 0, 'OK': 0, 'NC': 0}
    total_confidence = []
    total_predictions = 0
    max_ok = 0
    most_ok_date = None

    # Procesar registros
    for log_date, result, model_confidence in logs:
        if log_date not in results_by_date:
            results_by_date[log_date] = {'SP': 0, 'OK': 0, 'NC': 0, 'model_confidence': []}
        
        # Sumar resultados por fecha
        for label in result.split(', '):
            if label in results_by_date[log_date]:
                results_by_date[log_date][label] += 1
                total_counts[label] += 1
        
        # Sumar confianza del modelo
        results_by_date[log_date]['model_confidence'].append(model_confidence)
        total_confidence.append(model_confidence)
        total_predictions += 1

        # Encontrar el día con más OK
        if results_by_date[log_date]['OK'] > max_ok:
            max_ok = results_by_date[log_date]['OK']
            most_ok_date = log_date

        # Asegurar consistencia
    total_predictions = sum(total_counts.values())

    # Calcular métricas
    dates = list(results_by_date.keys())
    sp_counts = [results_by_date[date]['SP'] for date in dates]
    ok_counts = [results_by_date[date]['OK'] for date in dates]
    nc_counts = [results_by_date[date]['NC'] for date in dates]
    model_confidence_avg = [np.mean(results_by_date[date]['model_confidence']) for date in dates]
    total_confidence_avg = round(np.mean(total_confidence) * 100, 2) if total_confidence else 0
    percentage_ok = round((total_counts['OK'] / total_predictions * 100), 2) if total_predictions else 0

    # Respuesta al frontend
    return jsonify({
        "dates": dates,
        "sp": sp_counts,
        "ok": ok_counts,
        "nc": nc_counts,
        "model_confidence": model_confidence_avg,
        "total_counts": total_counts,
        "stats": {
            "total_predictions": total_predictions,
            "total_ok": total_counts['OK'],
            "percentage_ok": percentage_ok,
            "most_ok_date": most_ok_date.strftime('%Y-%m-%d') if isinstance(most_ok_date, datetime) else most_ok_date,
            "model_confidence_avg": total_confidence_avg
        }
    })


@app.route('/capture_image', methods=['POST'])
def capture_image():
    capture_type = request.form.get('type', 'positive')
    
    # Verificar si la imagen fue enviada en el formulario
    if 'image' not in request.files:
        return jsonify({"message": "No se recibió imagen"}), 400

    image_file = request.files['image']
    
    try:
        # Guardar la imagen en el directorio adecuado
        folder = os.path.join('capturas', capture_type)
        os.makedirs(folder, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{capture_type}_{timestamp}.png"
        filepath = os.path.join(folder, filename)

        # Guardar la imagen
        image_file.save(filepath)

        return jsonify({"message": f"Imagen {capture_type} guardada con éxito en {filepath}"})
    except Exception as e:
        return jsonify({"message": f"Error al procesar la imagen: {str(e)}"}), 500

if __name__ == '__main__':
    load_config()  # Cargar configuración inicial
    num_threads = max(2, multiprocessing.cpu_count() // 2)  # Ajusta según la carga
    with app.app_context():
        db.create_all()  # Crear las tablas
    serve(app, host='0.0.0.0', port=5000, threads=num_threads, channel_timeout=300) # Waitress servirá la aplicación