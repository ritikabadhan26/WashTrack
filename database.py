{% extends "base.html" %}
{% block title %}WashTrack - Place an Order{% endblock %}

{% block content %}

<!-- Hero -->
<div class="mb-8 text-center">
    <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-800">Free Laundry, Zero Hassle 🧺</h2>
    <p class="text-slate-500 mt-1 text-sm sm:text-base">Drop your order, pick a slot, and track your clothes until they're back in your hands.</p>
</div>

<div class="grid grid-cols-1 lg:grid-cols-5 gap-6">

    <!-- Order Form -->
    <div class="lg:col-span-2">
        <div class="bg-white rounded-xl2 shadow-md border border-slate-100 p-6 sm:p-7 sticky top-6">
            <div class="flex items-center gap-2 mb-5">
                <div class="bg-teal-100 text-teal-700 rounded-full p-2">
                    <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
                </div>
                <h3 class="text-lg font-bold text-slate-800">New Laundry Order</h3>
            </div>

            <form action="{{ url_for('new_order') }}" method="POST" class="space-y-4">

                <div class="grid grid-cols-2 gap-4">
                    <div class="col-span-2">
                        <label class="block text-sm font-semibold text-slate-600 mb-1">Full Name</label>
                        <input type="text" name="student_name" required placeholder="e.g. Aditi Sharma"
                               class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition" />
                    </div>
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
                    <label class="block text-sm font-semibold text-slate-600 mb-1">Pickup Slot</label>
                    <select name="pickup_slot" required
                            class="w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400 focus:border-transparent transition bg-white">
                        <option value="" disabled selected>Choose a slot...</option>
                        {% for slot in pickup_slots %}
                        <option value="{{ slot }}">{{ slot }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="pt-1">
                    <p class="text-sm font-semibold text-slate-600 mb-2">Item Counts</p>
                    <div class="grid grid-cols-2 gap-3">
                        {% for item in standard_items %}
                        <div class="flex items-center justify-between bg-slate-50 border border-slate-200 rounded-xl px-3 py-2">
                            <label for="qty_{{ item }}" class="text-sm font-medium text-slate-600">{{ item }}</label>
                            <input type="number" min="0" value="0" id="qty_{{ item }}" name="qty_{{ item }}"
                                   class="w-14 text-center rounded-lg border border-slate-200 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400" />
                        </div>
                        {% endfor %}
                    </div>
                    <p class="text-xs text-slate-400 mt-2">Tip: accurate counts help us make sure nothing gets lost!</p>
                </div>

                <button type="submit"
                        class="w-full mt-2 bg-gradient-to-r from-teal-600 to-indigo-600 hover:from-teal-700 hover:to-indigo-700 text-white font-semibold rounded-xl py-3 text-sm shadow-md shadow-teal-200 transition">
                    Submit Pickup Request
                </button>
            </form>
        </div>
    </div>

    <!-- Active Orders Board -->
    <div class="lg:col-span-3">
        <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-slate-800">Active Hostel Orders</h3>
            <span class="text-xs font-semibold bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full">{{ active_orders|length }} live</span>
        </div>

        {% if active_orders %}
        <div class="space-y-3">
            {% for order in active_orders %}
            <div class="bg-white rounded-xl2 shadow-sm border border-slate-100 p-4 sm:p-5 hover:shadow-md transition">
                <div class="flex flex-wrap items-start justify-between gap-2">
                    <div>
                        <p class="font-bold text-slate-800">{{ order.student_name }}
                            <span class="text-slate-400 font-normal text-sm">&middot; Room {{ order.room_number }}</span>
                        </p>
                        <p class="text-xs text-slate-400 mt-0.5">Order #{{ order.id }} &middot; {{ order.pickup_slot }}</p>
                    </div>
                    <span class="text-xs font-semibold px-3 py-1.5 rounded-full whitespace-nowrap {{ status_badges[order.status] }}">
                        {{ order.status }}
                    </span>
                </div>

                <div class="flex flex-wrap gap-2 mt-3">
                    {% for item in order.clothes %}
                    <span class="text-xs bg-slate-50 border border-slate-200 text-slate-600 px-2.5 py-1 rounded-lg font-medium">
                        {{ item.item_type }} &times; {{ item.quantity }}
                    </span>
                    {% endfor %}
                    <span class="text-xs bg-teal-50 border border-teal-200 text-teal-700 px-2.5 py-1 rounded-lg font-semibold">
                        Total: {{ order.total_items }} item(s)
                    </span>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="bg-white rounded-xl2 shadow-sm border border-dashed border-slate-200 p-10 text-center">
            <p class="text-slate-400 text-sm">No active orders right now. Be the first to submit one! 🎉</p>
        </div>
        {% endif %}
    </div>

</div>

{% endblock %}
