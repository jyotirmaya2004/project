from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='E:/project/PlantLeafDisease/templates')
with app.app_context():
    html = render_template('index.html', class_count=38, preview=None, result=None, top_predictions=[], error=None)
    print('bootstrap@5.3.3:', 'bootstrap@5.3.3' in html)
    print('styles.css:', 'styles.css' in html)
    print('preview-card:', 'preview-card' in html)
    print('d-none on preview card:', 'preview-card' in html and 'd-none' in html)
