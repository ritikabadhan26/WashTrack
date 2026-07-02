"""
database.py
WashTrack - SQLite helper module.

Provides connection management, initialization, and all data-access
functions used by the Flask app (app.py).
"""

import sqlite3
from datetime import datetime

DATABASE = "washtrack.db"

# Order lifecycle, in order. Used for sorting "urgency".
STATUS_FLOW = ["Pending Pickup", "Washing", "Ready for Collection", "Collected"]

# Pickup slots offered to students, in chronological order.
PICKUP_SLOTS = [
    "Morning 8-10 AM",
    "Afternoon 12-2 PM",
    "Evening 5-7 PM",
]


def get_db_connection():
    """Create a new SQLite connection with row factory + FK support."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database using schema.sql (drops & recreates tables)."""
    conn = get_db_connection()
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def ensure_db_exists():
    """Create the DB with proper schema only if it doesn't already exist."""
    import os
    if not os.path.exists(DATABASE):
        init_db()


def create_order(student_name, room_number, phone, pickup_slot, items):
    """
    Insert a new order and its item counts in a single transaction.

    items: list of tuples -> [(item_type, quantity), ...]
           Only items with quantity > 0 should be passed in.

    Returns the new order's id.
    """
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO orders (student_name, room_number, phone, pickup_slot, status)
               VALUES (?, ?, ?, ?, ?)""",
            (student_name, room_number, phone, pickup_slot, "Pending Pickup"),
        )
        order_id = cur.lastrowid

        item_rows = [
            (order_id, item_type, quantity)
            for item_type, quantity in items
            if quantity and quantity > 0
        ]
        if item_rows:
            cur.executemany(
                """INSERT INTO order_items (order_id, item_type, quantity)
                   VALUES (?, ?, ?)""",
                item_rows,
            )

        conn.commit()
        return order_id
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_order_status(order_id, new_status):
    """Update the status of a single order."""
    if new_status not in STATUS_FLOW:
        raise ValueError(f"Invalid status: {new_status}")

    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (new_status, order_id),
        )
        conn.commit()
    finally:
        conn.close()


def _attach_items(conn, orders):
    """Given a list of order Row objects, attach an 'items' list to each (as dicts)."""
    result = []
    for order in orders:
        order_dict = dict(order)
        items = conn.execute(
            "SELECT item_type, quantity FROM order_items WHERE order_id = ? ORDER BY item_type",
            (order_dict["id"],),
        ).fetchall()
        order_dict["clothes"] = [dict(i) for i in items]
        order_dict["total_items"] = sum(i["quantity"] for i in order_dict["clothes"])
        result.append(order_dict)
    return result


def get_active_orders():
    """
    Fetch all orders that are NOT yet 'Collected', sorted by pickup slot
    urgency (order of PICKUP_SLOTS) and then by creation time.
    Each order dict includes its list of items.
    """
    conn = get_db_connection()
    try:
        orders = conn.execute(
            """SELECT * FROM orders
               WHERE status != 'Collected'
               ORDER BY created_at ASC"""
        ).fetchall()

        orders_with_items = _attach_items(conn, orders)

        # Sort by pickup slot order (urgency), then by created_at
        def slot_rank(o):
            try:
                return PICKUP_SLOTS.index(o["pickup_slot"])
            except ValueError:
                return len(PICKUP_SLOTS)

        orders_with_items.sort(key=lambda o: (slot_rank(o), o["created_at"]))
        return orders_with_items
    finally:
        conn.close()


def get_all_orders():
    """Fetch ALL orders (including Collected), newest first, with items attached."""
    conn = get_db_connection()
    try:
        orders = conn.execute(
            "SELECT * FROM orders ORDER BY created_at DESC"
        ).fetchall()
        return _attach_items(conn, orders)
    finally:
        conn.close()


def get_orders_grouped_by_slot():
    """
    Fetch all non-collected orders grouped by pickup slot.
    Returns an ordered dict-like list of (slot_name, [orders...]) tuples,
    following PICKUP_SLOTS order, followed by any custom/unknown slots.
    """
    orders = get_active_orders()
    grouped = {slot: [] for slot in PICKUP_SLOTS}

    for order in orders:
        slot = order["pickup_slot"]
        grouped.setdefault(slot, [])
        grouped[slot].append(order)

    # Preserve PICKUP_SLOTS order first, then any extra slots
    ordered_keys = PICKUP_SLOTS + [k for k in grouped.keys() if k not in PICKUP_SLOTS]
    return [(slot, grouped[slot]) for slot in ordered_keys if grouped[slot]]


def get_dashboard_stats():
    """Return quick counts for the admin dashboard metric cards."""
    conn = get_db_connection()
    try:
        stats = {}
        for status in STATUS_FLOW:
            row = conn.execute(
                "SELECT COUNT(*) as c FROM orders WHERE status = ?", (status,)
            ).fetchone()
            stats[status] = row["c"]

        today = datetime.now().strftime("%Y-%m-%d")
        row = conn.execute(
            "SELECT COUNT(*) as c FROM orders WHERE date(created_at) = ?", (today,)
        ).fetchone()
        stats["today_total"] = row["c"]
        return stats
    finally:
        conn.close()


def get_order_by_id(order_id):
    """Fetch a single order (with items) by id."""
    conn = get_db_connection()
    try:
        order = conn.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        if order is None:
            return None
        return _attach_items(conn, [order])[0]
    finally:
        conn.close()
