from flask import Flask, render_template_string, request, jsonify
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

# ====== مقداردهی دیتابیس ======
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cooperations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL,
            telegram_id TEXT NOT NULL,
            description TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ====== HTML کامل (نسخه خفن) ======
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEVELOPERS TEAM | خفن‌ترین تیم توسعه</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700;900&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
            background: #0a0e1a;
            color: #e0e6f0;
            line-height: 1.6;
            padding: 20px;
            overflow-x: hidden;
        }

        /* ===== انیمیشن پس‌زمینه ===== */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(ellipse at 20% 50%, rgba(13, 71, 161, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 50%, rgba(79, 195, 247, 0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 100%, rgba(13, 71, 161, 0.05) 0%, transparent 50%);
            z-index: -1;
            animation: pulseBg 8s ease-in-out infinite alternate;
        }

        @keyframes pulseBg {
            0% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
            background: rgba(17, 22, 37, 0.95);
            border-radius: 32px;
            padding: 30px 25px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), 0 0 80px rgba(79, 195, 247, 0.05);
            border: 1px solid rgba(42, 52, 80, 0.5);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(from 0deg, transparent, rgba(79, 195, 247, 0.03), transparent, rgba(13, 71, 161, 0.03), transparent);
            animation: rotateBg 20s linear infinite;
            z-index: 0;
        }

        @keyframes rotateBg {
            100% { transform: rotate(360deg); }
        }

        .container > * {
            position: relative;
            z-index: 1;
        }

        /* ===== HEADER ===== */
        .team-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .team-header h1 {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #4fc3f7 0%, #0d47a1 50%, #4fc3f7 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientMove 3s ease-in-out infinite alternate;
            letter-spacing: 3px;
            text-shadow: 0 0 40px rgba(79, 195, 247, 0.2);
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }

        .team-header p {
            color: #94a3c7;
            font-size: 1.4rem;
            margin-top: 5px;
            letter-spacing: 2px;
        }

        .team-header .badge {
            display: inline-block;
            background: linear-gradient(135deg, #0d47a1, #1976d2);
            padding: 8px 25px;
            border-radius: 60px;
            font-size: 0.9rem;
            color: white;
            margin-top: 10px;
            border: 1px solid #4fc3f7;
            box-shadow: 0 0 30px rgba(79, 195, 247, 0.2);
        }

        /* ===== آمار خفن ===== */
        .stats-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
            padding: 20px;
            background: linear-gradient(135deg, rgba(13, 71, 161, 0.1), rgba(79, 195, 247, 0.05));
            border-radius: 28px;
            border: 1px solid rgba(79, 195, 247, 0.1);
        }

        .stat-item {
            text-align: center;
            padding: 15px;
        }

        .stat-item .number {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #4fc3f7, #0d47a1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
        }

        .stat-item .number .plus {
            font-size: 2rem;
        }

        .stat-item .label {
            color: #94a3c7;
            font-size: 1rem;
            margin-top: 5px;
        }

        .stat-item .sub-label {
            color: #4fc3f7;
            font-size: 0.8rem;
            opacity: 0.7;
        }

        /* ===== تصویر بزرگ ===== */
        .hero-image {
            width: 100%;
            max-height: 450px;
            object-fit: contain;
            border-radius: 28px;
            margin: 15px 0 25px 0;
            border: 2px solid rgba(79, 195, 247, 0.3);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.7), 0 0 60px rgba(79, 195, 247, 0.05);
            background: #0d1220;
            padding: 10px;
            transition: 0.5s;
            animation: floatImage 6s ease-in-out infinite;
        }

        @keyframes floatImage {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .hero-image:hover {
            border-color: #4fc3f7;
            box-shadow: 0 0 60px rgba(79, 195, 247, 0.2);
            transform: scale(1.01);
        }

        /* ===== ویژگی‌ها ===== */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin: 30px 0 40px 0;
        }

        .feature-card {
            background: rgba(24, 31, 50, 0.8);
            border-radius: 24px;
            padding: 25px 15px;
            text-align: center;
            border: 1px solid rgba(43, 54, 87, 0.5);
            transition: 0.4s;
            backdrop-filter: blur(5px);
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(79, 195, 247, 0.1), transparent);
            transition: 0.5s;
        }

        .feature-card:hover::before {
            left: 100%;
        }

        .feature-card i {
            font-size: 3rem;
            color: #4fc3f7;
            margin-bottom: 12px;
            transition: 0.3s;
        }

        .feature-card:hover i {
            transform: scale(1.2) rotate(5deg);
            text-shadow: 0 0 30px rgba(79, 195, 247, 0.3);
        }

        .feature-card h3 {
            font-size: 1.2rem;
            color: #c8d6f0;
            margin-bottom: 6px;
        }

        .feature-card p {
            font-size: 0.9rem;
            color: #8895bb;
        }

        .feature-card:hover {
            transform: translateY(-10px) scale(1.02);
            border-color: #4fc3f7;
            background: rgba(28, 37, 64, 0.9);
            box-shadow: 0 15px 40px rgba(79, 195, 247, 0.1);
        }

        /* ===== درباره ما ===== */
        .about-section {
            background: linear-gradient(135deg, rgba(20, 28, 43, 0.9), rgba(13, 22, 37, 0.9));
            border-radius: 28px;
            padding: 35px 30px;
            margin: 30px 0 35px 0;
            border-left: 6px solid #4fc3f7;
            border-right: 6px solid #0d47a1;
            position: relative;
            overflow: hidden;
        }

        .about-section::after {
            content: '</>';
            position: absolute;
            bottom: -20px;
            right: -20px;
            font-size: 8rem;
            opacity: 0.03;
            font-weight: 900;
            color: #4fc3f7;
        }

        .about-section h2 {
            font-size: 2.2rem;
            color: #eef4ff;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .about-section h2 i {
            color: #4fc3f7;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .about-section p {
            font-size: 1.1rem;
            color: #b7c3e3;
            margin-bottom: 18px;
        }

        .about-section .highlight {
            color: #4fc3f7;
            font-weight: 700;
        }

        /* ===== همکاری ===== */
        .cooperation-section {
            background: linear-gradient(135deg, rgba(14, 22, 41, 0.95), rgba(10, 18, 35, 0.95));
            border-radius: 28px;
            padding: 30px;
            margin: 30px 0;
            border: 1px solid rgba(42, 58, 96, 0.5);
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .cooperation-section::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(79, 195, 247, 0.03), transparent 70%);
            animation: rotateBg 30s linear infinite;
        }

        .cooperation-section h2 {
            font-size: 2.2rem;
            color: #e0eaff;
            margin-bottom: 20px;
        }

        .cooperation-section h2 i {
            color: #4fc3f7;
            margin-left: 10px;
        }

        .cooperation-btn {
            background: linear-gradient(145deg, #0d47a1, #1976d2);
            border: none;
            padding: 22px 60px;
            border-radius: 60px;
            font-size: 1.6rem;
            font-weight: 700;
            color: white;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 8px 30px rgba(25, 118, 210, 0.5);
            border: 1px solid #4fc3f7;
            display: inline-flex;
            align-items: center;
            gap: 20px;
            position: relative;
            overflow: hidden;
        }

        .cooperation-btn::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #4fc3f7, #0d47a1, #4fc3f7);
            background-size: 300% 300%;
            border-radius: 60px;
            z-index: -1;
            animation: borderGlow 3s ease-in-out infinite;
        }

        @keyframes borderGlow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .cooperation-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 60px rgba(79, 195, 247, 0.4);
        }

        .cooperation-btn:active {
            transform: scale(0.95);
        }

        .cooperation-btn i {
            font-size: 2rem;
        }

        /* ===== فرم ===== */
        .cooperation-form {
            background: rgba(26, 35, 64, 0.95);
            padding: 30px 25px;
            border-radius: 28px;
            margin: 20px 0 10px 0;
            display: none;
            border: 1px solid #4fc3f7;
            text-align: right;
            transition: 0.5s;
            box-shadow: 0 0 50px rgba(79, 195, 247, 0.05);
        }

        .cooperation-form.active {
            display: block;
            animation: slideDown 0.5s ease-out;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .cooperation-form h3 {
            color: #c8dcff;
            margin-bottom: 25px;
            font-size: 2rem;
            text-align: center;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            color: #b3c6f0;
            margin-bottom: 8px;
            font-weight: 500;
            font-size: 1rem;
        }

        .form-group label i {
            color: #4fc3f7;
            margin-left: 8px;
        }

        .form-group input, .form-group textarea {
            width: 100%;
            padding: 16px 20px;
            border-radius: 18px;
            border: 1px solid rgba(43, 61, 107, 0.6);
            background: rgba(13, 20, 40, 0.8);
            color: #eaf0ff;
            font-size: 1rem;
            transition: 0.3s;
            font-family: 'Vazirmatn', sans-serif;
        }

        .form-group input:focus, .form-group textarea:focus {
            outline: none;
            border-color: #4fc3f7;
            box-shadow: 0 0 30px rgba(79, 195, 247, 0.1);
            background: rgba(13, 20, 40, 1);
        }

        .form-group textarea {
            height: 120px;
            resize: vertical;
        }

        .submit-form-btn {
            background: linear-gradient(145deg, #0d47a1, #1976d2);
            border: none;
            padding: 18px 30px;
            border-radius: 60px;
            color: white;
            font-weight: 700;
            font-size: 1.3rem;
            cursor: pointer;
            width: 100%;
            transition: 0.3s;
            border: 1px solid #4fc3f7;
            box-shadow: 0 8px 30px rgba(25, 118, 210, 0.3);
        }

        .submit-form-btn:hover {
            transform: scale(1.02);
            box-shadow: 0 0 50px rgba(79, 195, 247, 0.3);
        }

        /* ===== پشتیبانی ===== */
        .support-section {
            background: linear-gradient(135deg, rgba(16, 24, 38, 0.95), rgba(10, 16, 30, 0.95));
            border-radius: 28px;
            padding: 30px;
            margin: 30px 0 20px 0;
            border: 1px solid rgba(47, 64, 106, 0.5);
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }

        .support-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 50%, rgba(79, 195, 247, 0.05), transparent 70%);
        }

        .support-section .support-text {
            display: flex;
            align-items: center;
            gap: 20px;
            position: relative;
            z-index: 1;
        }

        .support-section .support-text i {
            font-size: 3.5rem;
            color: #4fc3f7;
            animation: pulse 2s ease-in-out infinite;
        }

        .support-section .support-text h3 {
            font-size: 1.8rem;
            color: #d6e4ff;
        }

        .support-section .support-text p {
            color: #8ba0cf;
            font-size: 1.1rem;
        }

        .support-badge {
            background: linear-gradient(145deg, #0d47a1, #1976d2);
            padding: 15px 30px;
            border-radius: 60px;
            font-weight: 700;
            color: white;
            border: 1px solid #4fc3f7;
            box-shadow: 0 0 40px rgba(79, 195, 247, 0.15);
            cursor: pointer;
            transition: 0.3s;
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .support-badge:hover {
            transform: scale(1.05);
            box-shadow: 0 0 60px rgba(79, 195, 247, 0.3);
        }

        /* ===== فوتر ===== */
        .footer-team {
            text-align: center;
            margin-top: 35px;
            padding-top: 25px;
            border-top: 1px solid rgba(36, 48, 79, 0.5);
            color: #6b7da3;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 30px 50px;
            font-size: 1rem;
        }

        .footer-team span {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .footer-team i {
            color: #4fc3f7;
        }

        /* ===== واکنش‌گرایی ===== */
        @media (max-width: 700px) {
            .container { padding: 15px; }
            .team-header h1 { font-size: 2.5rem; }
            .features-grid { grid-template-columns: 1fr 1fr; }
            .support-section { flex-direction: column; align-items: flex-start; gap: 15px; }
            .cooperation-btn { width: 100%; justify-content: center; font-size: 1.2rem; padding: 18px 30px; }
            .hero-image { max-height: 200px; }
            .stats-section { grid-template-columns: 1fr 1fr; gap: 10px; }
            .stat-item .number { font-size: 2.2rem; }
            .cooperation-form { padding: 20px 15px; }
        }

        @media (max-width: 450px) {
            .features-grid { grid-template-columns: 1fr; }
            .team-header h1 { font-size: 2rem; }
            .stats-section { grid-template-columns: 1fr; }
            .cooperation-btn { font-size: 1rem; padding: 15px 20px; gap: 10px; }
            .cooperation-btn i { font-size: 1.5rem; }
        }

        html {
            scroll-behavior: smooth;
        }

        /* ===== افکت تایپ ===== */
        .typewriter {
            overflow: hidden;
            white-space: nowrap;
            border-left: 3px solid #4fc3f7;
            animation: typewriter 3s steps(30) 1s forwards, blink 0.8s step-end infinite;
            display: inline-block;
            padding-left: 5px;
        }

        @keyframes typewriter {
            from { width: 0; }
            to { width: 100%; }
        }

        @keyframes blink {
            0%, 100% { border-color: transparent; }
            50% { border-color: #4fc3f7; }
        }

        /* ===== اسکرول بار ===== */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #0a0e1a;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #0d47a1, #4fc3f7);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #4fc3f7;
        }
    </style>
</head>
<body>

<div class="container">

    <!-- HEADER -->
    <div class="team-header">
        <h1><i class="fas fa-code"></i> DEVELOPERS TEAM</h1>
        <p>⚡ امنیت · سرعت · زیبایی · تجربه‌ای اعتمادبخش</p>
        <div class="badge">
            <i class="fas fa-rocket"></i> بیش از ۱۰ تیم حرفه‌ای
        </div>
    </div>

    <!-- آمار خفن -->
    <div class="stats-section">
        <div class="stat-item">
            <div class="number">
                <span id="userCount">10,400</span><span class="plus">+</span>
            </div>
            <div class="label">کاربر آنلاین</div>
            <div class="sub-label"><i class="fas fa-circle" style="color: #4fc3f7; font-size: 0.5rem;"></i> همیشه فعال</div>
        </div>
        <div class="stat-item">
            <div class="number">
                <span>۱۰</span><span class="plus">+</span>
            </div>
            <div class="label">تیم همکار</div>
            <div class="sub-label"><i class="fas fa-users" style="color: #4fc3f7;"></i> حرفه‌ای و متخصص</div>
        </div>
        <div class="stat-item">
            <div class="number">
                <span>۱۲</span><span class="plus">×</span><span>۷</span>
            </div>
            <div class="label">پشتیبانی</div>
            <div class="sub-label"><i class="fas fa-headset" style="color: #4fc3f7;"></i> همیشه در دسترس</div>
        </div>
        <div class="stat-item">
            <div class="number">
                <span>۱۰۰</span><span class="plus">%</span>
            </div>
            <div class="label">رضایت مشتری</div>
            <div class="sub-label"><i class="fas fa-star" style="color: #ffd700;"></i> کیفیت تضمینی</div>
        </div>
    </div>

    <!-- تصویر بزرگ -->
    <img class="hero-image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='300' viewBox='0 0 800 300'%3E%3Crect width='800' height='300' fill='%23111625'/%3E%3Ctext x='50' y='80' font-family='Segoe UI, sans-serif' font-size='32' fill='%234fc3f7' font-weight='bold'%3E🚀 DEVELOPERS TEAM%3C/text%3E%3Ctext x='50' y='130' font-family='Segoe UI, sans-serif' font-size='24' fill='%23b7c3e3'%3E🔐 امنیت سایت · بررسی و تقویت امنیت%3C/text%3E%3Ctext x='50' y='175' font-family='Segoe UI, sans-serif' font-size='24' fill='%23b7c3e3'%3E💻 توسعه وب اپلیکیشن با جدیدترین تکنولوژی‌ها%3C/text%3E%3Ctext x='50' y='220' font-family='Segoe UI, sans-serif' font-size='24' fill='%23b7c3e3'%3E⚡ سرعت و عملکرد · بهینه‌سازی حرفه‌ای%3C/text%3E%3Ctext x='50' y='265' font-family='Segoe UI, sans-serif' font-size='20' fill='%234fc3f7'%3E👥 ۱۰,۴۰۰+ کاربر آنلاین · ۱۰+ تیم همکار%3C/text%3E%3C/svg%3E"
         alt="DEVELOPERS TEAM - خفن‌ترین تیم توسعه">

    <!-- ویژگی‌ها -->
    <div class="features-grid">
        <div class="feature-card"><i class="fas fa-shield-alt"></i><h3>امنیت سایت</h3><p>بررسی و تقویت امنیت و رفع آسیب‌پذیری</p></div>
        <div class="feature-card"><i class="fas fa-globe"></i><h3>توسعه وب</h3><p>سایت و وب اپلیکیشن با جدیدترین تکنولوژی‌ها</p></div>
        <div class="feature-card"><i class="fas fa-tachometer-alt"></i><h3>سرعت و عملکرد</h3><p>بهینه‌سازی سرعت و افزایش عملکرد سایت</p></div>
        <div class="feature-card"><i class="fas fa-mobile-alt"></i><h3>سازگار با همه دستگاه‌ها</h3><p>طراحی ریسپانسیو برای موبایل و دسکتاپ</p></div>
        <div class="feature-card"><i class="fas fa-check-circle"></i><h3>تست و بررسی</h3><p>تست کامل و بررسی کیفیت قبل از انتشار</p></div>
    </div>

    <!-- درباره ما -->
    <div class="about-section">
        <h2><i class="fas fa-users"></i> درباره ما</h2>
        <p>
            <span class="highlight">تیم توسعه‌دهندگان</span> با افتخار از سال ۲۰۱۲ فعالیت خود را آغاز کرده است. 
            ما متشکل از <span class="highlight">۱۰+ تیم حرفه‌ای</span> در زمینه امنیت، توسعه فول‌استک و طراحی خلاق هستیم که 
            <span class="highlight">کیفیت بالا، امنیت کامل و پشتیبانی همیشگی</span> را سرلوحه کار خود قرار داده‌ایم.
        </p>
        <p>
            ماموریت ما <span class="highlight">ساخت وب بهتر، امن‌تر و سریع‌تر برای همه</span> است. 
            با جدیدترین تکنولوژی‌ها مانند Django، React، و معماری مدرن، پروژه‌های شما را به سطح بعدی می‌بریم.
        </p>
        <p style="margin-top: 15px;">
            <i class="fas fa-check-circle" style="color:#4fc3f7;"></i> ۱۲×۷ پشتیبانی · 
            <i class="fas fa-lock" style="color:#4fc3f7;"></i> گواهی‌های امنیتی · 
            <i class="fas fa-rocket" style="color:#4fc3f7;"></i> تحویل سریع · 
            <i class="fas fa-users" style="color:#4fc3f7;"></i> ۱۰+ تیم همکار
        </p>
    </div>

    <!-- ثبت همکاری -->
    <div class="cooperation-section">
        <h2><i class="fas fa-handshake"></i> ثبت همکاری</h2>
        <button class="cooperation-btn" id="toggleCooperationBtn">
            <i class="fas fa-plus-circle"></i> ثبت همکاری با تیم قوی ما
        </button>

        <!-- فرم همکاری -->
        <div class="cooperation-form" id="cooperationForm">
            <h3>📋 فرم درخواست همکاری</h3>
            <form id="coopForm">
                <div class="form-group">
                    <label><i class="fas fa-user"></i> نام و نام خانوادگی</label>
                    <input type="text" id="fullname" placeholder="نام کامل خود را وارد کنید..." required>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-envelope"></i> ایمیل</label>
                    <input type="email" id="email" placeholder="ایمیل معتبر..." required>
                </div>
                <div class="form-group">
                    <label><i class="fab fa-telegram"></i> آیدی تلگرام</label>
                    <input type="text" id="telegram_id" placeholder="@your_telegram_id" required>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-comment"></i> توضیحات همکاری</label>
                    <textarea id="description" placeholder="چه همکاری مد نظر دارید؟"></textarea>
                </div>
                <button type="submit" class="submit-form-btn"><i class="fas fa-paper-plane"></i> ارسال درخواست</button>
            </form>
            <p style="color: #6b7da3; margin-top: 16px; font-size:0.9rem;">
                <i class="fas fa-check-circle" style="color:#4fc3f7;"></i> پس از ارسال، تیم ما در اسرع وقت با شما تماس می‌گیرد.
            </p>
        </div>
    </div>

    <!-- پشتیبانی -->
    <div class="support-section" id="support">
        <div class="support-text">
            <i class="fas fa-headset"></i>
            <div>
                <h3>پشتیبانی ۲۴/۷</h3>
                <p>همیشه در کنار شما هستیم — <i class="fas fa-comment-dots" style="color:#4fc3f7;"></i> گفتینو فعال</p>
            </div>
        </div>
        <div class="support-badge" onclick="document.getElementById('support').scrollIntoView({behavior:'smooth'})">
            <i class="fas fa-shield-alt"></i> ۱۲×۷ · امنیت کامل
        </div>
    </div>

    <!-- فوتر -->
    <div class="footer-team">
        <span><i class="fas fa-code"></i> توسعه | امنیت | طراحی | عملکرد</span>
        <span><i class="fas fa-calendar-alt"></i> ۲۰۱۲–۲۰۲۶</span>
        <span><i class="fas fa-check-circle"></i> کیفیت بالا، پشتیبانی همیشگی</span>
        <span><i class="fas fa-users"></i> ۱۰+ تیم همکار</span>
        <span><i class="fas fa-globe"></i> DEVELOPERS TEAM</span>
    </div>

</div>

<!-- ===== اسکریپت گفتینو ===== -->
<script type="text/javascript">
    !function(){var i="mPcd5D",d=document,g=d.createElement("script"),s="https://www.goftino.com/widget/"+i,l=localStorage.getItem("goftino_"+i);g.type="text/javascript",g.async=!0,g.src=l?s+"?o="+l:s;d.getElementsByTagName("head")[0].appendChild(g);}();
</script>

<!-- ===== اسکریپت داخلی ===== -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // ===== انیمیشن شمارنده =====
        function animateCounter(element, target, duration) {
            let start = 0;
            const step = Math.max(1, Math.floor(target / 60));
            const interval = duration / 60;
            
            const timer = setInterval(() => {
                start += step;
                if (start >= target) {
                    start = target;
                    clearInterval(timer);
                }
                element.textContent = start.toLocaleString();
            }, interval);
        }

        const userCountEl = document.getElementById('userCount');
        if (userCountEl) {
            setTimeout(() => {
                animateCounter(userCountEl, 10400, 2000);
            }, 500);
        }

        // ===== فرم همکاری =====
        const toggleBtn = document.getElementById('toggleCooperationBtn');
        const formContainer = document.getElementById('cooperationForm');
        const form = document.getElementById('coopForm');

        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            formContainer.classList.toggle('active');
            const icon = this.querySelector('i');
            if (formContainer.classList.contains('active')) {
                icon.className = 'fas fa-minus-circle';
                this.style.background = 'linear-gradient(145deg, #0a3a7a, #0d47a1)';
            } else {
                icon.className = 'fas fa-plus-circle';
                this.style.background = 'linear-gradient(145deg, #0d47a1, #1976d2)';
            }
        });

        // ارسال فرم
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const data = {
                fullname: document.getElementById('fullname').value,
                email: document.getElementById('email').value,
                telegram_id: document.getElementById('telegram_id').value,
                description: document.getElementById('description').value
            };

            fetch('/submit-cooperation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                if (result.status === 'success') {
                    form.reset();
                    formContainer.classList.remove('active');
                    const icon = toggleBtn.querySelector('i');
                    icon.className = 'fas fa-plus-circle';
                    toggleBtn.style.background = 'linear-gradient(145deg, #0d47a1, #1976d2)';
                }
            })
            .catch(error => {
                alert('❌ خطا در ارسال فرم. لطفاً دوباره تلاش کنید.');
                console.error('Error:', error);
            });
        });
    });
</script>

</body>
</html>
'''

# ====== صفحه اصلی ======
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# ====== دریافت فرم همکاری ======
@app.route('/submit-cooperation', methods=['POST'])
def submit_cooperation():
    try:
        data = request.get_json()
        fullname = data.get('fullname')
        email = data.get('email')
        telegram_id = data.get('telegram_id')
        description = data.get('description')
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO cooperations (fullname, email, telegram_id, description, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (fullname, email, telegram_id, description, created_at))
        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'message': '✅ درخواست همکاری شما با موفقیت ثبت شد'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'❌ خطا: {str(e)}'}), 400

# ====== اجرا ======
if __name__ == '__main__':
    print("=" * 60)
    print("🚀 DEVELOPERS TEAM - خفن‌ترین تیم توسعه")
    print("📱 ۱۰,۴۰۰+ کاربر آنلاین | ۱۰+ تیم همکار")
    print("=" * 60)
    print("🌐 سرور در آدرس: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)