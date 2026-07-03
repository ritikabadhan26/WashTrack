<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}WashTrack - Hostel Laundry Portal{% endblock %}</title>

    <!-- Tailwind CSS via CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        teal: {
                            50: '#f0fdfa', 100: '#ccfbf1', 200: '#99f6e4', 300: '#5eead4',
                            400: '#2dd4bf', 500: '#14b8a6', 600: '#0d9488', 700: '#0f766e',
                        },
                        indigo: {
                            50: '#eef2ff', 100: '#e0e7ff', 200: '#c7d2fe', 300: '#a5b4fc',
                            400: '#818cf8', 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca',
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
                    },
                    borderRadius: {
                        'xl2': '1.25rem',
                    }
                }
            }
        }
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', ui-sans-serif, system-ui, sans-serif; }
    </style>
    {% block head %}{% endblock %}
</head>
<body class="bg-gradient-to-br from-teal-50 via-white to-indigo-50 min-h-screen text-slate-800">

    <!-- Header Banner -->
    <header class="bg-gradient-to-r from-teal-600 to-indigo-600 shadow-lg">
        <div class="max-w-6xl mx-auto px-4 sm:px-6 py-5 flex items-center justify-between">
            <a href="{{ url_for('index') }}" class="flex items-center gap-3">
                <div class="bg-white/20 backdrop-blur rounded-2xl p-2.5 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                </div>
                <div>
                    <h1 class="text-white text-xl sm:text-2xl font-extrabold tracking-tight leading-none">WashTrack</h1>
                    <p class="text-teal-50/90 text-xs sm:text-sm font-medium">Hostel Laundry Portal</p>
                </div>
            </a>
            <nav class="flex items-center gap-2 sm:gap-3">
                {% if current_user %}
                    {% if current_user.role == 'student' %}
                    <a href="{{ url_for('index') }}"
                       class="px-3 sm:px-4 py-2 rounded-full text-sm font-semibold text-white/90 hover:text-white hover:bg-white/15 transition {% if request.endpoint == 'index' %}bg-white/20 text-white{% endif %}">
                       My Dashboard
                    </a>
                    {% else %}
                    <a href="{{ url_for('admin') }}"
                       class="px-3 sm:px-4 py-2 rounded-full text-sm font-semibold text-white/90 hover:text-white hover:bg-white/15 transition {% if request.endpoint == 'admin' %}bg-white/20 text-white{% endif %}">
                       Staff Dashboard
                    </a>
                    {% endif %}
                    <span class="hidden sm:inline text-teal-50/80 text-sm px-1">Hi, {{ current_user.full_name.split(' ')[0] }}</span>
                    <a href="{{ url_for('logout') }}"
                       class="px-3 sm:px-4 py-2 rounded-full text-sm font-semibold text-white/90 hover:text-white hover:bg-white/15 transition">
                       Logout
                    </a>
                {% else %}
                    <a href="{{ url_for('login') }}"
                       class="px-3 sm:px-4 py-2 rounded-full text-sm font-semibold text-white/90 hover:text-white hover:bg-white/15 transition {% if request.endpoint == 'login' %}bg-white/20 text-white{% endif %}">
                       Login
                    </a>
                    <a href="{{ url_for('register') }}"
                       class="px-3 sm:px-4 py-2 rounded-full text-sm font-semibold bg-white text-teal-700 hover:bg-teal-50 transition {% if request.endpoint == 'register' %}ring-2 ring-white/60{% endif %}">
                       Sign Up
                    </a>
                {% endif %}
            </nav>
        </div>
    </header>

    <!-- Flash messages -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 mt-5">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="mb-3 rounded-xl2 px-4 py-3 text-sm font-medium shadow-sm border
                        {% if category == 'success' %} bg-teal-50 text-teal-800 border-teal-200
                        {% else %} bg-rose-50 text-rose-700 border-rose-200 {% endif %}">
                        <div class="flex items-center gap-2">
                            {% if category == 'success' %}
                            <svg class="h-5 w-5 text-teal-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                            {% else %}
                            <svg class="h-5 w-5 text-rose-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                            {% endif %}
                            <span>{{ message }}</span>
                        </div>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    <!-- Main content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        {% block content %}{% endblock %}
    </main>

    <footer class="max-w-6xl mx-auto px-4 sm:px-6 py-8 text-center text-slate-400 text-xs">
        WashTrack &middot; Free laundry service for hostel residents &middot; Made for the hostel community 🧺
    </footer>

</body>
</html>
