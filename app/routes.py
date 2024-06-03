from app import app
from flask import request, jsonify, render_template, session
from datetime import datetime
import os
import shutil
import base64
import logging
from app.database import create_connection, create_employee_table, image_storer
from app.email_utils import send_otp
import face_recognition
from mysql.connector import Error

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def signup_page():
    return render_template('frontend.html')

@app.route('/punch_in', methods=['POST'])
def punch_in():
    employee_id = request.form['employee_id']
    punch_in_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connec = create_connection()
    conn = connec.cursor()
    conn.execute('INSERT INTO history (emp_id, punch_in) VALUES (%s, %s)', (employee_id, punch_in_time))
    connec.commit()
    conn.close()

    return jsonify({'message': 'Punch in time recorded successfully'}), 200

@app.route('/punch_out', methods=['POST'])
def punch_out():
    employee_id = request.form['employee_id']
    punch_out_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    connec = create_connection()
    conn = connec.cursor()
    conn.execute('UPDATE history SET punch_out = %s WHERE emp_id = %s AND punch_out IS NULL', (punch_out_time, employee_id))
    connec.commit()
    conn.close()

    return jsonify({'message': 'Punch out time recorded successfully'}), 200

#OTP sending route starts here
@app.route('/send_otp', methods=['GET'])
def send_otp_route():
    email = request.args.get('email')
    if email:
        success, otp = send_otp(email)
        if success:
            return jsonify({ 'message': 'OTP sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send OTP. Please try again.'}), 500
    else:
        return jsonify({'error': 'Email not provided'}), 400

#Signup Route Starts Here
@app.route('/signup', methods=['POST'])
def signup():
    try:
        employee_id = request.form['employee_id']
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        person_name = request.form['person_name']
        otp = request.form['otp']
        if not (employee_id and name and mobile_number and email and person_name and otp):
            return jsonify({'error': 'Please provide all required fields'}), 400
        logging.debug(f"Received OTP: {otp}, Session OTP: {session.get('otp')}, Session Email: {session.get('otp_email')}, Received Email: {email}")
        if otp == session.get('otp') and email == session.get('otp_email'):
            person_dir = os.path.join("captured_images", person_name)
            os.makedirs(person_dir, exist_ok=True)

            connection = create_connection()
            if connection is not None:
                cursor = connection.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO employee (emp_id, emp_name, mobile_num, email)
                        VALUES (%s, %s, %s, %s)
                    """, (employee_id, name, mobile_number, email))
                    connection.commit()
                    photos = []
                    for i in range(1, 16):
                        photo_data = request.form.get(f'photo_{i}')
                        if photo_data:
                            photo_data = photo_data.split(',')[1]
                            photo_bytes = base64.b64decode(photo_data)
                            photos.append(photo_bytes)
                            with open(os.path.join(person_dir, f"captured_image_{i}.png"), "wb") as file:
                                file.write(photo_bytes)
                        else:
                            photos.append(None)
                    cursor.execute("""
                                   INSERT INTO employee_photos (
                            emp_id, photo_1, photo_2, photo_3, photo_4, photo_5,
                            photo_6, photo_7, photo_8, photo_9, photo_10,
                            photo_11, photo_12, photo_13, photo_14, photo_15
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            photo_1 = VALUES(photo_1),
                            photo_2 = VALUES(photo_2),
                            photo_3 = VALUES(photo_3),
                            photo_4 = VALUES(photo_4),
                            photo_5 = VALUES(photo_5),
                            photo_6 = VALUES(photo_6),
                            photo_7 = VALUES(photo_7),
                            photo_8 = VALUES(photo_8),
                            photo_9 = VALUES(photo_9),
                            photo_10 = VALUES(photo_10),
                            photo_11 = VALUES(photo_11),
                            photo_12 = VALUES(photo_12),
                            photo_13 = VALUES(photo_13),
                            photo_14 = VALUES(photo_14),
                            photo_15 = VALUES(photo_15)
                    """, (employee_id, *photos))
                    connection.commit()
                    session.pop('otp', None)
                    session.pop('otp_email', None)
                    shutil.rmtree(person_dir)
                    shutil.rmtree('captured_images')
                    return jsonify({'message': 'Employee signed up successfully'}), 201
                except Error as e:
                    logging.error(f"Error inserting data: {e}")
                    return jsonify({'error': 'Failed to sign up employee. Please try again.'}), 500
                finally:
                    cursor.close()
                    connection.close()
            else:
                logging.error("Failed to connect to the database")
                return jsonify({'error': 'Database connection failed'}), 500
        else:
            return jsonify({'error': 'Invalid OTP. Please try again.'}), 400
    except Exception as e:
        logging.error(f"Exception in signup route: {e}")
        return jsonify({'error': 'An error occurred. Please try again.'}), 500

@app.route('/verify_face', methods=['POST'])
def verify_face():
    try:
        logging.debug("Received request to verify face")
        data = request.form
        emp_id = data.get('emp_id_verify_face')
        image_data = data.get('photo')
        if not (emp_id and image_data):
            logging.error("Employee ID or image data not provided")
            return jsonify({'error': 'Employee ID or image data not provided'}), 400

        image_bytes = base64.b64decode(image_data.split(',')[1])
        person_dir = os.path.join("verify_image_", emp_id)
        os.makedirs(person_dir, exist_ok=True)
        
        with open(os.path.join(person_dir, "captured_image.png"), "wb") as file:
            file.write(image_bytes)

        captured_image_path = os.path.join(person_dir, "captured_image.png")

        image_storer(emp_id)
        got_image = face_recognition.load_image_file(captured_image_path)
        existing_image_path = f"stored_images/{emp_id}_photo_1.png"
        if not os.path.exists(existing_image_path):
            logging.error("No stored images found for this employee")
            return jsonify({'message': 'No stored images found for this employee'}), 400
        
        existing_image = face_recognition.load_image_file(existing_image_path)
        got_image_facialfeatures = face_recognition.face_encodings(got_image)
        existing_image_facialfeatures = face_recognition.face_encodings(existing_image)
        if not got_image_facialfeatures or not existing_image_facialfeatures:
            logging.error("No face detected in one or both images")
            return jsonify({'message': 'No face detected in one or both images'}), 400
        got_image_facialfeatures = got_image_facialfeatures[0]
        existing_image_facialfeatures = existing_image_facialfeatures[0]
        results = face_recognition.compare_faces([existing_image_facialfeatures], got_image_facialfeatures)
        logging.debug(results)
        if (results[0] == True):
            logging.info("Face verified successfully")
            shutil.rmtree(person_dir)
            shutil.rmtree('stored_images')
            shutil.rmtree('verify_image_')
            return jsonify({'message': 'Face verified successfully'}), 201
        else:
            logging.info("Face verification failed")
            return jsonify({'message': 'Face verification failed'}), 201

    except Exception as e:
        logging.error(f"Exception in verify_face route: {e}")
        return jsonify({'error': 'An error occurred. Please try again.'}), 500