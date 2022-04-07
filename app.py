
import numpy as np
import pickle
from flask import Flask, render_template, request
import os

# app = Flask(__name__)

# TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

# app = Flask(__name__) # to make the app run without any
# app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app = Flask(__name__, static_folder=STATIC_DIR)

# model = pickle.load(open('rf_model.pkl', 'rb'))
model = pickle.load(open('rf_model2.pkl', 'rb'))

@app.route('/')
# '/home/'
# @app.route('/booking/')
def index():
    return render_template('index.html')
# booking
    # return render_template('booking.html')
    
@app.route('/index.html', methods=["GET", "POST"])
def index2():
    return render_template("index.html")
    
@app.route('/about.html', methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route('/blog.html', methods=["GET", "POST"])
def blog():
    return render_template("blog.html")

@app.route('/contact.html', methods=["GET", "POST"])
def contact():
    return render_template("contact.html")

@app.route('/price.html', methods=["GET", "POST"])
def price():
    return render_template("price.html")

@app.route('/service.html', methods=["GET", "POST"])
def service():
    return render_template("service.html")

@app.route('/single.html', methods=["GET", "POST"])
def single():
    return render_template("single.html")

@app.route('/booking.html', methods=["GET", "POST"])
def booking():
    return render_template("booking.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    
    # size_bytes, price, rating_count_tot, rating_count_ver, user_rating_ver, 
    # sup_devices.num, Major, ipadSc_urls.num, lang.num, Education, Entertainment, Games, 
    # Others, Shopping
    
    app_prime_genre = np.zeros(5)

 
    app_size_bytes = np.array([float(request.form['size_bytes'])/(1024**2)])
    app_price = np.array([float(request.form['price'])])
    app_rating_count_tot = np.array([int(request.form['rating_count_tot'])])
    app_rating_count_ver = np.array([int(request.form['rating_count_ver'])])
    app_user_rating_ver = np.array([float(request.form['user_rating_ver'])])
    app_sup_devices_num = np.array([int(request.form['sup_devices_num'])])
    app_Major = np.array([int(request.form['Major'])])
    app_ipadSc_urls_num = np.array([int(request.form['ipadSc_urls_num'])])
    app_lang_num = np.array([int(request.form['lang_num'])])
    
    prime_genre = request.form['prime_genre']
    if prime_genre == 'Education':
        app_prime_genre[0] = 1
    elif prime_genre == 'Entertainment':
        app_prime_genre[1] = 1
    elif prime_genre == 'Games':
        app_prime_genre[2] = 1
    elif prime_genre == 'Others':
        app_prime_genre[3] = 1
    elif prime_genre == 'Shopping':
        app_prime_genre[4] = 1
    
    int_features = np.concatenate([app_size_bytes, app_price, app_rating_count_tot, app_rating_count_ver, 
                    app_user_rating_ver, app_sup_devices_num, app_Major, 
                    app_ipadSc_urls_num, app_lang_num, app_prime_genre])
    
    # final_features = [np.array(int_features)]
    prediction = model.predict([int_features])

    
    # prediction = model.predict([[request.form['type','large_bags','date_new','x4046',
    # 'month_ex','x4225','region','small_bags','total_volume','year','x4770','xlarge_bags')]])
    # prediction = model.predict([[100788224, 3.99, 21292, 26, 4.5, 38, 6, 5, 10, 'Games']])
    
    output = round(prediction[0],2)
    # print(output)
    # return render_template('index.html', prediction_text = f'Predicted average user rating: {output}' )                            
                            
    return render_template('booking.html', prediction_text = f'Predicted average user rating: {output}' )

if __name__ == '__main__':
    app.run(debug=True)