from flask import Flask, render_template_string, request, send_file
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = Flask(__name__)

# --- FRONTEND TEMPLATE (Cyberpunk / Dark Futuristic UI with Tailwind CSS v4) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Futuristic ATS-Compliant Resume Builder</title>
    <!-- Tailwind CSS v4 CDN -->
    <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
    <style>
        body {
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
        }
        .glass-panel {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(56, 189, 248, 0.2);
        }
        .neon-input:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
        }
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 15px rgba(37, 99, 235, 0.6); }
            50% { box-shadow: 0 0 25px rgba(56, 189, 248, 0.9); }
        }
        .pulse-btn {
            animation: pulse-glow 2s infinite;
        }
    </style>
</head>
<body class="min-h-screen text-slate-100 flex items-center justify-center p-4">
    <div class="w-full max-w-2xl glass-panel rounded-2xl p-6 md:p-8 shadow-2xl">
        <div class="text-center mb-8">
            <h1 class="text-2xl md:text-3xl font-extrabold tracking-wider text-cyan-400 uppercase">
                ⚡ ATS Resume Builder
            </h1>
            <p class="text-slate-400 text-sm mt-1">Generate a clean, text-searchable, corporate-ready PDF</p>
        </div>

        <form action="/generate" method="POST" class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-xs font-semibold uppercase text-cyan-300 mb-1">Full Name</label>
                    <input type="text" name="name" required placeholder="Raj Gautam" 
                           class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 neon-input outline-none transition">
                </div>
                <div>
                    <label class="block text-xs font-semibold uppercase text-cyan-300 mb-1">Email Address</label>
                    <input type="email" name="email" required placeholder="raj@example.com" 
                           class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 neon-input outline-none transition">
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-xs font-semibold uppercase text-cyan-300 mb-1">Phone Number</label>
                    <input type="text" name="phone" required placeholder="+91 9876543210" 
                           class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 neon-input outline-none transition">
                </div>
                <div>
                    <label class="block text-xs font-semibold uppercase text-cyan-300 mb-1">Professional Target Title</label>
                    <input type="text" name="title" required placeholder="Full Stack Developer / BCA Student" 
                           class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 neon-input outline-none transition">
                </div>
            </div>

            <div>
                <label class="block text-xs font-semibold uppercase text-cyan-300 mb-1">Executive Summary</label>
                <textarea name="summary" rows="3" required placeholder="Motivated computer application student with expertise in Python, Flask, and web technologies..." 
                          class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 neon-input outline-none transition resize-none"></textarea>
            </div>

            <div>
                <label class="block text-xs font-semibold uppercase text-cyan-300 mb-1">Technical Expertise (Comma Separated)</label>
                <textarea name="skills" rows="2" required placeholder="Python, JavaScript, HTML5, CSS3, Flask, SQLite, Git, Linux" 
                          class="w-full bg-slate-900/50 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-200 neon-input outline-none transition resize-none"></textarea>
            </div>

            <button type="submit" class="w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 font-bold text-white rounded-lg transition duration-200 pulse-btn cursor-pointer uppercase tracking-wider text-sm mt-2">
                🚀 Generate ATS PDF Resume
            </button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_pdf():
    # Fetching Form Data
    name = request.form.get('name', 'Professional')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    title = request.form.get('title', '')
    summary = request.form.get('summary', '')
    skills = request.form.get('skills', '')

    # In-memory byte buffer for PDF generation
    buffer = io.BytesIO()

    # Document setup (A4/Letter safe margins: 40pt)
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom ATS-Optimized Safe Styles (Dark Corporate Palette using Standard Fonts)
    name_style = ParagraphStyle(
        'ResumeName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        alignment=0
    )

    title_style = ParagraphStyle(
        'ResumeTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=6
    )

    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    # --- BUILD THE STORY (ATS Single-Column Flow) ---
    story.append(Paragraph(name, name_style))
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(f"{email} &nbsp;|&nbsp; {phone}", contact_style))
    
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

    # Executive Summary Section
    story.append(Paragraph("EXECUTIVE SUMMARY", section_heading))
    story.append(Paragraph(summary, body_style))

    # Technical Expertise Section
    story.append(Paragraph("TECHNICAL EXPERTISE", section_heading))
    story.append(Paragraph(skills, body_style))

    # Compile PDF
    doc.build(story)
    buffer.seek(0)

    # Clean file name for download
    safe_filename = f"{name.replace(' ', '_')}_Resume.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=safe_filename,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
