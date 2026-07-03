{% extends "base.html" %}
{% block title %}WashTrack - Create Account{% endblock %}

{% block content %}
<div class="max-w-md mx-auto mt-6">
    <div class="bg-white rounded-xl2 shadow-md border border-slate-100 p-7 sm:p-8">
        <div class="text-center mb-6">
            <div class="inline-flex bg-gradient-to-r from-teal-100 to-indigo-100 rounded-full p-3 mb-3">
                <svg class="h-7 w-7 text-indigo-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
            </div>
            <h2 class="text-xl font-extrabold text-slate-800">Create your student account</h2>
            <p class="text-slate-500 text-sm mt-1">One-time signup — only hostel residents need apply.</p>
        </div>

        <form action="{{ url_for('register') }}" method="POST" class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-slate-600 mb-1">Full Name</label>
                <input type="text" name="full_name" required placeholder="e.g. Aditi Sharma"
                       class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition" />
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-slate-600 mb-1">Room No.</label>
                    <input type="text" name="room_number" required placeholder="e.g. B-204"
                           class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition" />
                </div>
                <div>
                    <label class="block text-sm font-semibold text-slate-600 mb-1">Phone</label>
                    <input type="tel" name="phone" required placeholder="10-digit number"
                           class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition" />
                </div>
            </div>

            <div>
                <label class="block text-sm font-semibold text-slate-600 mb-1">Choose a Username</label>
                <input type="text" name="username" required placeholder="e.g. aditi.s"
                       class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition" />
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-slate-600 mb-1">Password</label>
                    <input type="password" name="password" required placeholder="min. 4 characters"
                           class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition" />
                </div>
                <div>
                    <label class="block text-sm font-semibold text-slate-600 mb-1">Confirm Password</label>
                    <input type="password" name="confirm_password" required placeholder="repeat password"
                           class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition" />
                </div>
            </div>

            <button type="submit"
                    class="w-full mt-2 bg-gradient-to-r from-teal-600 to-indigo-600 hover:from-teal-700 hover:to-indigo-700 text-white font-semibold rounded-xl py-3 text-sm shadow-md shadow-teal-200 transition">
                Create Account
            </button>
        </form>

        <p class="text-center text-sm text-slate-500 mt-5">
            Already have an account? <a href="{{ url_for('login') }}" class="text-teal-700 font-semibold hover:underline">Log in</a>
        </p>
    </div>
</div>
{% endblock %}
