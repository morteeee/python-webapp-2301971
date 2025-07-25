from flask import Flask, render_template, request, redirect, url_for, flash
import re
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_secret_key'

# Basic detection patterns (not exhaustive — for demonstration only)
XSS_PATTERNS = [
    re.compile(r"<script.*?>.*?</script.*?>", re.IGNORECASE),
    re.compile(r"on\w+\s*=", re.IGNORECASE),
    re.compile(r"javascript:", re.IGNORECASE),
]

SQLI_PATTERNS = [
    re.compile(r"(?i)\b(OR|AND)\b\s+['\"]?\w+['\"]?\s*=\s*['\"]?\w+['\"]?"),
    re.compile(r"(--|#|/\*)"),
    re.compile(r"\b(SELECT|INSERT|DELETE|UPDATE|DROP|UNION|SLEEP)\b", re.IGNORECASE)
]

def is_xss_attack(user_input):
    return any(pattern.search(user_input) for pattern in XSS_PATTERNS)

def is_sql_injection(user_input):
    return any(pattern.search(user_input) for pattern in SQLI_PATTERNS)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')

        if is_xss_attack(search_term):
            flash("Potential XSS attack detected. Please try again.")
            return redirect(url_for('home'))

        if is_sql_injection(search_term):
            flash("Potential SQL Injection attack detected. Please try again.")
            return redirect(url_for('home'))

        return redirect(url_for('result', term=escape(search_term)))

    return render_template('home.html')

@app.route('/result')
def result():
    term = request.args.get('term', '')
    return render_template('result.html', term=term)
