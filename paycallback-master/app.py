import streamlit as st
import sqlite3
import json
from pathlib import Path

# Konfigurasi halaman
st.set_page_config(
    page_title="Counter App",
    page_icon="🔢",
    layout="centered"
)

DB_NAME = "counter.db"

# ======================
# Database Functions
# ======================
def init_db():
    """Inisialisasi database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_count():
    """Ambil jumlah count dari database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM counter")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def increment_count():
    """Tambah 1 ke counter"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO counter DEFAULT VALUES")
    conn.commit()
    conn.close()

def clear_count():
    """Reset counter ke 0"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM counter")
    conn.commit()
    conn.close()

# ======================
# Streamlit UI
# ======================
def main():
    # Inisialisasi database
    init_db()
    
    # Header
    st.title("🔢 Counter App")
    st.markdown("---")
    
    # Ambil count saat ini
    current_count = get_count()
    
    # Display counter dengan style
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #f0f2f6; border-radius: 10px;'>
            <h1 style='font-size: 72px; margin: 0; color: #1f77b4;'>{current_count}</h1>
            <p style='font-size: 18px; color: #666; margin: 10px 0 0 0;'>Total Count</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tombol kontrol
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Increment", use_container_width=True, type="primary"):
            increment_count()
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear", use_container_width=True, type="secondary"):
            clear_count()
            st.rerun()
    
    # Info tambahan
    st.markdown("---")
    with st.expander("ℹ️ Informasi"):
        st.markdown("""
        **Cara Penggunaan:**
        - **Increment**: Tambah counter +1
        - **Refresh**: Perbarui tampilan counter
        - **Clear**: Reset counter ke 0
        
        Data disimpan di SQLite database lokal.
        """)
    
    # Footer
    st.markdown("---")
    st.caption("Counter App • Powered by Streamlit")

# ======================
# API Endpoints (Optional)
# ======================
# Jika ingin menambahkan API endpoints, gunakan st.experimental_get_query_params()
# dan st.experimental_set_query_params() untuk routing sederhana

if __name__ == "__main__":
    main()
